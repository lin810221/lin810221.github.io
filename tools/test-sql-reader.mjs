/* Actual shared reader and fixed relational labs; DOM emulation is not browser layout QA. */
import {readFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
import {parseHTML,Event,HTMLElement} from '../.qa/vendor/linkedom.mjs';
import {parse} from '../.qa/vendor/acorn.mjs';
import katex from '../.qa/vendor/katex.mjs';
const root=new URL('../',import.meta.url),read=f=>readFile(new URL(f,root),'utf8');
for(const f of ['assets/reader.js','sql/assets/overview.js','sql/assets/course-data.js'])parse(await read(f),{ecmaVersion:'latest'});
const {document:home}=parseHTML(await read('index.html'));
assert.equal(home.querySelectorAll('.subject-feature').length,Object.keys(JSON.parse(await read('tools/library.json')).courses).length);
assert.equal(home.querySelectorAll('a[href="sql/index.html"]').length,1);
const {window,document}=parseHTML(await read('sql/index.html'));
const old=JSON.stringify({completed:['001-web-and-django'],notes:{'001-web-and-django':'Django 原本的筆記'}});
const storage=new Map([['learning-notes:django:v1',old]]),location={hash:''},q=s=>document.querySelector(s);
HTMLElement.prototype.focus=function(){};HTMLElement.prototype.scrollIntoView=function(){};
if(!Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'checked'))Object.defineProperty(window.HTMLInputElement.prototype,'checked',{
  get(){return this.hasAttribute('checked');},set(v){v?this.setAttribute('checked',''):this.removeAttribute('checked');}
});
window.scrollTo=()=>{};window.print=()=>{};
q('#search-dialog').showModal=function(){this.open=true;};q('#search-dialog').close=function(){this.open=false;};
window.katex={render:(tex,el,options)=>{el.innerHTML=katex.renderToString(tex,options);}};
Object.assign(globalThis,{window,document,location,requestAnimationFrame:fn=>fn(),localStorage:{getItem:k=>storage.get(k)??null,setItem:(k,v)=>storage.set(k,v)}});
await import(new URL('assets/math.js',root).href);await import(new URL('sql/assets/course-data.js',root).href);
await import(new URL('sql/assets/overview.js',root).href);await import(new URL('assets/reader.js',root).href);
const navigate=id=>{location.hash='#'+id;window.dispatchEvent(new Event('hashchange'));};
const input=(id,v)=>{q('#'+id).value=String(v);q('#'+id).dispatchEvent(new Event('input'));};
const checked=(id,v)=>{q('#'+id).checked=v;q('#'+id).dispatchEvent(new Event('change'));};
const select=(id,v)=>{for(const x of q('#'+id).querySelectorAll('option'))x.selected=false;q('#'+id).querySelector(`option[value="${v}"]`).selected=true;q('#'+id).dispatchEvent(new Event('change'));};
assert.equal(q('.topbar-subject').textContent,'SQL 與資料工程');assert.equal(document.querySelectorAll('.chapter-link').length,108);
assert.equal(document.querySelectorAll('.module-row').length,18);assert.equal(document.querySelectorAll('.tf-lab').length,12);
assert.equal(document.querySelectorAll('.tf-atlas img').length,36);
for(const e of document.querySelectorAll('.tf-lab input,.tf-lab select'))assert.ok(q(`label[for="${e.id}"]`));
for(const a of document.querySelectorAll('a[href^="#"]')){const id=a.getAttribute('href').slice(1);if(id==='main'||id.startsWith('overview'))continue;assert.ok(window.COURSE.lessons.some(l=>l.id===id),id);}
const lab=window.SQLLab;
assert.equal(lab.filter('paid',0).reduce((s,x)=>s+x.cents,0),13000);
select('sq-status','paid');input('sq-min',4000);assert.equal(q('#sq-filter-count').textContent,'2');
assert.equal(lab.fanout(2,2).rows,4);input('sq-left',0);assert.equal(q('#sq-pairs').textContent,'0');input('sq-left',5);input('sq-right',5);assert.equal(q('#sq-pairs').textContent,'25');
assert.deepEqual(lab.nulls('is-null').filter(x=>x.result===true).map(x=>x.id),[2,4]);select('sq-predicate','equals-null');assert.equal(q('#sq-null-output').querySelectorAll('tbody tr').length,4);assert.ok(q('#sq-null-output').textContent.includes('UNKNOWN'));
assert.deepEqual(lab.windows('rows').map(x=>x.total),[3000,8000,10000,14000,15000]);
assert.deepEqual(lab.windows('range').map(x=>x.total),[3000,10000,10000,15000,15000]);select('sq-frame','range');assert.ok(q('#sq-window-output').textContent.includes('10000'));
assert.deepEqual(lab.weighted(80,20),{weighted:26,naive:50});assert.equal(q('#sq-weighted').textContent,'26%');input('sq-rate-a',0);input('sq-rate-b',100);assert.equal(q('#sq-weighted').textContent,'90%');
assert.deepEqual(lab.cursor(102,false),[104,105]);assert.deepEqual(lab.cursor(102,true),[103,104,105]);select('sq-after','102');checked('sq-tuple',true);assert.equal(q('#sq-next').textContent,'103, 104, 105');select('sq-after','105');assert.equal(q('#sq-next').textContent,'沒有下一筆');
assert.deepEqual(lab.scd(24,false),['south']);assert.deepEqual(lab.scd(24,true),['north','south']);checked('sq-overlap',true);assert.equal(q('#sq-scd-count').textContent,'2');input('sq-hour',48);assert.equal(q('#sq-scd-count').textContent,'0');
assert.deepEqual(lab.publication('after_commit'),{cursor:8,db:11500,pointer:12000,pending:true,recovered:11500});select('sq-fault','after_commit');assert.equal(q('#sq-recovered').textContent,'11500');select('sq-fault','before_commit');assert.equal(q('#sq-recovered').textContent,'12000');
assert.deepEqual(lab.quality(10,2,1),{known:8,distinct:7,completeness:.8,uniqueness:.875});assert.equal(lab.quality(0,0,0).completeness,null);assert.equal(lab.quality(10,10,0).uniqueness,null);input('sq-n',0);assert.ok(q('#sq-complete').textContent.includes('未定義'));input('sq-n',2);input('sq-missing',100);input('sq-duplicate',100);assert.ok(!/NaN|Infinity/.test(q('#sq-quality-output').textContent));
assert.deepEqual(lab.dag(false).order,['extract','normalize','validate','publish']);checked('sq-cycle',true);assert.ok(q('#sq-dag-state').textContent.includes('循環'));
assert.deepEqual(lab.retry(5),{waits:[1,2,4,8],total:15});input('sq-attempts',1);assert.equal(q('#sq-waits').textContent,'0');input('sq-attempts',8);assert.equal(q('#sq-waits').textContent,'7');assert.equal(lab.retry(8).total,39);
assert.equal(lab.freshness(30,false).ok,true);assert.equal(lab.freshness(35,false).ok,false);checked('sq-future',true);assert.ok(q('#sq-fresh-state').textContent.includes('不可信'));
for(const fn of [()=>lab.filter('x',0),()=>lab.fanout(-1,2),()=>lab.weighted(NaN,2),()=>lab.cursor(0,true),()=>lab.scd(49,false),()=>lab.publication('x'),()=>lab.quality(2,0,2),()=>lab.retry(0),()=>lab.freshness(Infinity,false)])assert.throws(fn,RangeError);
for(const svg of document.querySelectorAll('.tf-plot')){assert.equal(svg.getAttribute('role'),'img');assert.ok(svg.querySelector('title'));assert.ok(!/NaN|Infinity/.test(svg.innerHTML));}
assert.equal(document.querySelectorAll('.math-block[data-math-error]').length,0);
for(const m of document.querySelectorAll('.tf-lab .math-block'))assert.ok(m.querySelector('.katex'),'interactive formula must render');
const course=window.COURSE;let equations=0,examples=0;const used=new Set();
for(const l of course.lessons){
  navigate(l.id);assert.equal(q('.lesson-header h1').textContent,l.title);assert.ok(q('.tf-task').textContent.includes(l.title));
  assert.equal(document.querySelectorAll('.chapter-link[aria-current="page"]').length,1);used.add(q('.tf-figure img').getAttribute('src'));
  for(const a of document.querySelectorAll('.toc-links a'))assert.ok(document.getElementById(a.getAttribute('href').split('/')[1]));
  if(l.example){examples++;assert.equal(q('.example-download a').getAttribute('href'),'examples.zip');}
  const {document:doc}=parseHTML(`<!doctype html><html><body>${l.html}</body></html>`);
  for(const m of doc.querySelectorAll('.math-source,.math-block')){assert.ok(m.querySelector('.katex'));assert.ok(katex.renderToString(m.getAttribute('data-tex'),{throwOnError:true}));equations++;}
}
assert.equal(used.size,36);assert.ok(equations>=30);assert.equal(examples,108);
navigate('001-data-lifecycle');q('#complete-lesson').click();assert.equal(q('#progress-count').textContent,'1 / 108');
q('#lesson-notes').value='游標必須與交易和發布責任一致。';q('#lesson-notes').dispatchEvent(new Event('input'));
navigate('037-bound-crud');navigate('001-data-lifecycle');assert.equal(q('#lesson-notes').value,'游標必須與交易和發布責任一致。');assert.equal(storage.get('learning-notes:django:v1'),old);
q('#open-search').click();for(const term of ['2.0.1','NULL','CDC','11500','RLS']){q('#search-input').value=term;q('#search-input').dispatchEvent(new Event('input'));assert.ok(document.querySelectorAll('.search-result').length>0,term);}
q('#close-search').click();q('#menu-toggle').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'true');q('#sidebar-shade').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'false');
navigate('overview');assert.equal(document.querySelectorAll('.tf-lab').length,12);assert.equal(q('#sq-filter-count').textContent,'5');assert.equal(q('#sq-pairs').textContent,'4');
const ids=[...document.querySelectorAll('[id]')].map(x=>x.id);assert.equal(ids.length,new Set(ids).size);
export const report={slug:'sql',modules:18,units:108,figures:36,equations,examples,labs:'12 relational and failure-boundary labs PASS',reader:'math/search/progress/notes/downloads/menu/remount PASS',isolation:'Django notes preserved',limit:'DOM simulation, not browser layout QA'};
