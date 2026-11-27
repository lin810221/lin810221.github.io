/* Homepage interaction and storage regressions. DOM QA, not browser layout QA. */
import {readFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {parseHTML,Event} from '../.qa/vendor/linkedom.mjs';
import {parse} from '../.qa/vendor/acorn.mjs';
const root = new URL('../',import.meta.url);
const read = file => readFile(new URL(file,root),'utf8');
const html = await read('index.html');
const dataSource = await read('assets/library-data.js');
const script = await read('assets/library.js');
const VIEW_KEY = 'learning-notes:library:card-view:v1';
parse(script,{ecmaVersion:'latest'});
parse(dataSource,{ecmaVersion:'latest'});

function setup({url='https://example.test/index.html',saved=new Map(),blocked=false,writeBlocked=false,historyBlocked=false}={}) {
  const {window,document} = parseHTML(html);
  const events = new Map();
  const stack = [url]; let index = 0, writes = 0, preferenceWrites = 0;
  const location = {href:url};
  const storage = {
    getItem:key=>{if(blocked)throw Error('Storage blocked');return saved.get(key)??null;},
    setItem:(key,value)=>{
      if(key!==VIEW_KEY){writes++;throw Error('Homepage must never overwrite reader storage');}
      if(blocked || writeBlocked)throw Error('Storage write blocked');
      preferenceWrites++;saved.set(key,value);
    }
  };
  const history = {
    pushState:(_,__,value)=>{if(historyBlocked)throw Error('History blocked');stack.splice(++index);stack.push(value);location.href=value;},
    replaceState:(_,__,value)=>{if(historyBlocked)throw Error('History blocked');stack[index]=value;location.href=value;}
  };
  // A plain window wrapper keeps fixtures isolated from linkedom's global proxy.
  const browser = {document,location,history,localStorage:storage,addEventListener:(name,fn)=>events.set(name,fn)};
  const sandbox = {window:browser,document,URL,console};
  vm.createContext(sandbox);
  vm.runInContext(dataSource,sandbox);
  vm.runInContext(script,sandbox);
  const q = s=>document.querySelector(s);
  const click = s=>{const el=q(s);assert.ok(el,s);el.click();};
  const visible = ()=>[...document.querySelectorAll('[data-course]')].filter(e=>!e.hidden).map(e=>e.dataset.course);
  const input = value=>{q('#course-search').value=value;q('#course-search').dispatchEvent(new Event('input'));};
  return {document,q,click,input,visible,location,saved,data:browser.LEARNING_LIBRARY,writes:()=>writes,preferenceWrites:()=>preferenceWrites,
    back:()=>{location.href=stack[--index];events.get('popstate')();},emit:(name,event={})=>events.get(name)?.(event)};
}

// Static baseline: all subjects and ordinary links work with JavaScript disabled.
const baseline = parseHTML(html).document;
const metadata = JSON.parse(await read('tools/library.json'));
const slugs = Object.keys(metadata.courses);
assert.equal(baseline.querySelectorAll('[data-course]').length,slugs.length);
assert.equal(baseline.querySelectorAll('[data-domain-group]').length,5);
for(const slug of slugs) {
  assert.equal(baseline.querySelectorAll(`a[href="${slug}/index.html"]`).length,1,slug);
  assert.equal(baseline.querySelector(`[data-course="${slug}"]`).hidden,false);
}
assert.ok(baseline.querySelector('.filter-panel').hidden);
assert.ok(baseline.querySelector('.card-view-switch').hidden);
assert.ok(baseline.querySelector('.classic-intro').hidden);
assert.equal(baseline.body.dataset.cardView,'detailed','No-JS fallback preserves the full cards');
assert.equal(baseline.querySelectorAll('a button,a input,a select').length,0,'No nested interactive controls');
assert.equal(new Set([...baseline.querySelectorAll('[id]')].map(e=>e.id)).size,baseline.querySelectorAll('[id]').length,'Unique static element IDs');

const h=setup();
assert.equal(h.document.body.dataset.cardView,'detailed');
assert.equal(h.q('.card-view-switch').hidden,false);
assert.equal(h.q('[data-card-view-option="detailed"]').getAttribute('aria-pressed'),'true');
assert.equal(h.visible().length,slugs.length);
assert.equal(h.q('.filter-panel').hidden,false);
assert.equal(h.q('#continue-learning').hidden,true,'Do not invent reading history');
h.click('.tag-options [data-tag="python"]');
assert.ok(h.visible().includes('django'));
assert.ok(h.visible().includes('applied-statistics'));
assert.ok(h.visible().includes('llm'));
assert.ok(!h.visible().includes('nutrition'));
assert.equal(h.q('.tag-options [data-tag="python"]').getAttribute('aria-pressed'),'true');
h.click('[data-domain="ai"]');
assert.ok(h.visible().every(s=>metadata.courses[s].domain==='ai'));
assert.ok(!h.visible().includes('django'));
h.click('[data-level="advanced"]');
assert.deepEqual(new Set(h.visible()),new Set(['transformer','image-recognition','finetuning','langgraph']));
h.input('LoRA');
assert.deepEqual(h.visible(),['finetuning']);
assert.equal(h.q('[data-tag-count="python"]').textContent,'1','Facet counts respect other dimensions');
h.click('#clear-filters');
assert.equal(h.visible().length,slugs.length);
h.click('[data-course="django"] [data-tag="api"]');
assert.deepEqual(new Set(h.visible()),new Set(['llm','mcp','django']),'Card tags immediately find related courses');
h.click('.tag-options [data-tag="api"]');
assert.equal(h.visible().length,slugs.length,'Click selected tag to deselect');
h.click('[data-domain="health"]');
assert.equal(h.visible().length,10);
h.click('.tag-options [data-tag="python"]');
assert.equal(h.visible().length,0);
assert.equal(h.q('#empty-results').hidden,false);
assert.ok([...h.document.querySelectorAll('[data-domain-group]')].every(s=>s.hidden));
h.click('[data-remove="tag"]');
assert.equal(h.visible().length,10,'Remove one condition without clearing the rest');
h.click('#clear-filters');
h.input('missing course that does not exist');
h.click('#empty-reset');
assert.equal(h.visible().length,slugs.length);
h.input('ＰｙＴｏｒｃｈ');
assert.ok(h.visible().includes('pytorch'),'Search supports width/case normalization');
h.input('LLM 模型訓練');
assert.deepEqual(new Set(h.visible()),new Set(['transformer','finetuning']),'All query words apply');
h.input('<img src=x onerror=alert(1)>');
assert.equal(h.q('#active-filters img'),null,'Search terms are escaped');
h.click('#clear-filters');

// Routes keep deliberate order, including routes that cross domain boundaries.
h.click('[data-route="models"]');
assert.deepEqual(h.visible(),['machine-learning','deep-learning','pytorch','transformer','finetuning']);
assert.equal(h.q('#sort-description').textContent,'依建議路線順序');
h.click('[data-route="evidence"]');
assert.deepEqual(h.visible(),['applied-statistics','evidence-health','public-health']);
h.click('[data-remove="route"]');
assert.equal(h.visible().length,slugs.length);
assert.equal(h.q('[data-domain-group="math"] [data-course="applied-statistics"]').hidden,false,'Restore cards to original groups');
assert.equal(h.q('#route-results').children.length,0);

// URL deep links, history navigation and file:// all use the same behavior.
const linked=setup({url:'https://example.test/?domain=ai&tag=python&level=advanced&q=LoRA'});
assert.deepEqual(linked.visible(),['finetuning']);
linked.click('#clear-filters');linked.back();
assert.deepEqual(linked.visible(),['finetuning']);
assert.equal(linked.q('#course-search').value,'LoRA');
const invalid=setup({url:'https://example.test/?domain=nope&level=nope&tag=__proto__&route=nope'});
assert.equal(invalid.visible().length,slugs.length);
const offline=setup({url:'file:///D:/LearningNote/index.html',historyBlocked:true});
offline.click('.tag-options [data-tag="python"]');
assert.ok(offline.visible().includes('django'));

// Existing progress: deduplicate IDs, ignore deleted IDs, preserve every byte of notes.
const record = JSON.stringify({completed:['001-web-and-django','001-web-and-django','deleted-unit'],notes:{'001-web-and-django':'原有筆記 $x^2$'},last:'007-django-version'});
const saved = new Map([['learning-notes:django:v1',record],['learning-notes:llm:v1','{malformed']]);
const p=setup({saved});
assert.equal(p.writes(),0);
assert.equal(saved.get('learning-notes:django:v1'),record);
assert.equal(p.q('[data-course="django"] progress').value,1);
assert.ok(!p.q('#continue-learning').hidden);
assert.ok(p.q('#continue-courses a').getAttribute('href').startsWith('django/index.html#'));
// A valid last-read id is honored even when no unit is complete.
const first=p.data.courses.find(c=>c.slug==='django').units[2];
saved.set('learning-notes:django:v1',JSON.stringify({completed:[],last:first,notes:{x:'keep'}}));
p.emit('storage',{key:'learning-notes:django:v1'});
assert.equal(p.q('#continue-courses a').getAttribute('href'),'django/index.html#'+first);
saved.delete('learning-notes:django:v1');p.emit('focus');
assert.equal(p.q('#continue-learning').hidden,true);
assert.equal(p.q('[data-course="django"] .course-progress').hidden,true,'Cleared storage must not leave stale progress');
const done=setup({saved:new Map([['learning-notes:django:v1',JSON.stringify({completed:p.data.courses.find(c=>c.slug==='django').units})]])});
assert.equal(done.q('#continue-learning').hidden,true,'Finished courses do not appear as unfinished');
assert.ok(done.q('[data-course="django"] [data-progress-label]').textContent.startsWith('已完成'));
const blocked=setup({blocked:true});
blocked.click('.tag-options [data-tag="evidence"]');
assert.ok(blocked.visible().length>0,'Unavailable storage must not block discovery');
assert.equal(blocked.writes(),0);

// Display preference shares the existing cards and preserves filter and reader state.
const viewNotes = JSON.stringify({completed:['001-web-and-django'],last:'001-web-and-django',notes:{'001-web-and-django':'retain original notes'}});
const preferences = new Map([['learning-notes:django:v1',viewNotes]]);
const v = setup({saved:preferences});
v.click('.tag-options [data-tag="python"]');
v.click('[data-domain="ai"]');
v.click('[data-level="advanced"]');
v.input('LoRA');
const beforeView = v.visible(), beforeURL = v.location.href;
const beforeCard = v.q('[data-course="finetuning"]');
v.click('[data-card-view-option="compact"]');
assert.equal(v.document.body.dataset.cardView,'compact');
assert.equal(v.q('[data-card-view-option="compact"]').getAttribute('aria-pressed'),'true');
assert.equal(v.q('[data-card-view-option="detailed"]').getAttribute('aria-pressed'),'false');
const classicOrder = Object.entries(metadata.courses).sort(([,a],[,b])=>a.classicOrder-b.classicOrder).map(([slug])=>slug);
assert.deepEqual(v.visible(),classicOrder,'Simple mode is the full original course list in its original order');
assert.equal(v.q('.classic-intro').hidden,false);
assert.equal(v.q('.library-hero').hidden,true);
assert.equal(v.q('#explore').hidden,true);
assert.equal(v.q('#learning-routes').hidden,true);
assert.equal(v.q('.filter-panel').hidden,true);
assert.equal(v.q('.library-top-nav').hidden,true);
assert.equal(v.q('#continue-learning').hidden,true);
assert.equal(v.q('#classic-results').children.length,slugs.length);
assert.ok([...v.document.querySelectorAll('[data-domain-group]')].every(el=>el.hidden));
assert.equal(v.q('[data-course="langgraph"] .classic-copy h2').textContent.trim(),'LangGraph 完整教學');
assert.equal(v.q('[data-course="finetuning"] .course-card-link').getAttribute('aria-labelledby'),'classic-title-finetuning');
assert.equal(v.location.href,beforeURL,'View switching must not modify filter URLs or history');
assert.equal(v.q('[data-course="finetuning"]'),beforeCard,'The same card and link remain in the DOM');
assert.equal(v.saved.get('learning-notes:django:v1'),viewNotes,'Reader data remains byte-identical');
assert.equal(v.saved.get(VIEW_KEY),'compact');
assert.equal(v.writes(),0);
assert.equal(v.preferenceWrites(),1);
v.click('[data-card-view-option="compact"]');
assert.equal(v.preferenceWrites(),1,'Repeated selection does not rewrite storage');
const restoredView = setup({saved:preferences});
assert.equal(restoredView.document.body.dataset.cardView,'compact','Saved preference survives reload');
assert.deepEqual(restoredView.visible(),classicOrder);
v.click('[data-card-view-option="detailed"]');
assert.deepEqual(v.visible(),beforeView,'Returning to the classified homepage restores all filters');
assert.equal(v.q('.classic-intro').hidden,true);
assert.equal(v.q('#explore').hidden,false);
assert.equal(v.q('#classic-results').children.length,0);
assert.equal(v.q('[data-course="finetuning"] .course-card-link').getAttribute('aria-labelledby'),'title-finetuning');
v.click('#clear-filters');
assert.equal(v.document.body.dataset.cardView,'detailed','Clearing filters must preserve display preference');
v.click('[data-route="models"]');
const routeBeforeView = v.visible();
v.click('[data-card-view-option="compact"]');
assert.deepEqual(v.visible(),classicOrder);
v.click('[data-card-view-option="detailed"]');
assert.deepEqual(v.visible(),routeBeforeView,'Route order survives view switching');
assert.equal(v.saved.get(VIEW_KEY),'detailed');
v.input('no matching course');
v.click('[data-card-view-option="compact"]');
assert.equal(v.q('#empty-results').hidden,true,'Original homepage shows its complete list without the detailed filters');
assert.deepEqual(v.visible(),classicOrder);
v.emit('storage',{key:VIEW_KEY,newValue:'detailed'});
assert.equal(v.document.body.dataset.cardView,'detailed','Other tabs can update the preference');
assert.equal(v.q('#empty-results').hidden,false,'The detailed empty state is restored');
const preferenceWritesBeforeClear = v.preferenceWrites();
v.emit('storage',{key:null});
assert.equal(v.document.body.dataset.cardView,'detailed');
assert.equal(v.preferenceWrites(),preferenceWritesBeforeClear,'Storage notifications never write back');
assert.equal(setup({saved:new Map([[VIEW_KEY,'unexpected']])}).document.body.dataset.cardView,'detailed');
blocked.click('[data-card-view-option="compact"]');
assert.equal(blocked.document.body.dataset.cardView,'compact','Blocked storage does not disable view switching');
assert.ok(blocked.visible().length>0);
const readOnlyView = setup({writeBlocked:true});
readOnlyView.click('[data-card-view-option="compact"]');
assert.equal(readOnlyView.document.body.dataset.cardView,'compact');
assert.equal(readOnlyView.saved.has(VIEW_KEY),false);
const sqlHome=setup();
sqlHome.click('.tag-options [data-tag="sql"]');assert.deepEqual(sqlHome.visible(),['sql']);
sqlHome.click('[data-card-view-option="compact"]');assert.deepEqual(sqlHome.visible(),classicOrder);
sqlHome.click('[data-card-view-option="detailed"]');assert.deepEqual(sqlHome.visible(),['sql']);
sqlHome.click('[data-route="data-to-web"]');assert.deepEqual(sqlHome.visible(),['sql','django']);
assert.equal(sqlHome.writes(),0,'New engineering route preserves reader storage');
const documentHome=setup();documentHome.click('.tag-options [data-tag="documents"]');assert.deepEqual(documentHome.visible(),['multimodal']);documentHome.click('[data-card-view-option="compact"]');assert.deepEqual(documentHome.visible(),classicOrder);documentHome.click('[data-card-view-option="detailed"]');assert.deepEqual(documentHome.visible(),['multimodal']);documentHome.click('[data-route="document-ai"]');assert.deepEqual(documentHome.visible(),['image-recognition','multimodal','rag']);assert.equal(documentHome.writes(),0);
export const report={courses:slugs.length,domains:5,checks:'tag/domain/level/search, routes, SQL route, deep links/history, offline, no-JS, escaped input, read-only progress, original/classified homepage switching and persistence'};
console.log('PASS homepage:',JSON.stringify(report));
