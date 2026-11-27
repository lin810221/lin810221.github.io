/* Actual course reader DOM and deterministic labs; not a browser layout claim. */
import {readFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
import {parseHTML,Event,HTMLElement} from '../.qa/vendor/linkedom.mjs';
import {parse} from '../.qa/vendor/acorn.mjs';
import katex from '../.qa/vendor/katex.mjs';
const root=new URL('../',import.meta.url),read=f=>readFile(new URL(f,root),'utf8');
for(const f of ['assets/reader.js','django/assets/overview.js','django/assets/course-data.js'])parse(await read(f),{ecmaVersion:'latest'});
const {document:home}=parseHTML(await read('index.html'));
assert.equal(home.querySelectorAll('.subject-feature').length,Object.keys(JSON.parse(await readFile(new URL('tools/library.json',root),'utf8')).courses).length);
assert.equal(home.querySelectorAll('a[href="django/index.html"]').length,1);
const {window,document}=parseHTML(await read('django/index.html'));
const old=JSON.stringify({completed:['001-adaptation-map'],notes:{'001-adaptation-map':'原本微調筆記'}});
const storage=new Map([['learning-notes:finetuning:v1',old]]),location={hash:''},q=s=>document.querySelector(s);
HTMLElement.prototype.focus=function(){};HTMLElement.prototype.scrollIntoView=function(){};
// Linkedom omits the checked IDL property; emulate the browser checkbox contract.
if(!Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'checked')){
  Object.defineProperty(window.HTMLInputElement.prototype,'checked',{
    get(){return this.hasAttribute('checked');},set(value){value?this.setAttribute('checked',''):this.removeAttribute('checked');}
  });
}
window.scrollTo=()=>{};window.print=()=>{};
q('#search-dialog').showModal=function(){this.open=true;};q('#search-dialog').close=function(){this.open=false;};
window.katex={render:(tex,el,options)=>{el.innerHTML=katex.renderToString(tex,options);}};
Object.assign(globalThis,{window,document,location,requestAnimationFrame:fn=>fn(),localStorage:{getItem:k=>storage.get(k)??null,setItem:(k,v)=>storage.set(k,v)}});
await import(new URL('assets/math.js',root).href);await import(new URL('django/assets/course-data.js',root).href);
await import(new URL('django/assets/overview.js',root).href);await import(new URL('assets/reader.js',root).href);
const navigate=id=>{location.hash='#'+id;window.dispatchEvent(new Event('hashchange'));};
const input=(id,value)=>{q('#'+id).value=String(value);q('#'+id).dispatchEvent(new Event('input'));};
const checked=(id,value)=>{q('#'+id).checked=value;q('#'+id).dispatchEvent(new Event('change'));};
const select=(id,value)=>{for(const x of q('#'+id).querySelectorAll('option'))x.selected=false;q('#'+id).querySelector(`option[value="${value}"]`).selected=true;q('#'+id).dispatchEvent(new Event('change'));};
assert.equal(q('.topbar-subject').textContent,'Django');assert.equal(document.querySelectorAll('.chapter-link').length,84);
assert.equal(document.querySelectorAll('.module-row').length,14);assert.equal(document.querySelectorAll('.tf-lab').length,8);
assert.equal(document.querySelectorAll('.tf-atlas img').length,28);
for(const e of document.querySelectorAll('.tf-lab input,.tf-lab select'))assert.ok(q(`label[for="${e.id}"]`));
const lab=window.DjangoLab;
assert.equal(q('#dj-form-state').textContent,'驗證通過');assert.equal(q('#dj-status').textContent,'302');
assert.equal(q('#dj-writes').textContent,'1');assert.ok(q('#dj-task-state').textContent.includes('同程序'));
assert.equal(lab.route('/tasks/new/').name,'desk:create');assert.equal(lab.route('/tasks/12/').parameters.pk,'12');
assert.equal(lab.route('/tasks/12/edit/').name,'desk:update');assert.equal(lab.route('/tasks/abc/').name,'404');
select('dj-path','/tasks/abc/');assert.ok(q('#dj-route-output').textContent.includes('404'));
assert.deepEqual(lab.middleware(true).response,['Authentication','Session','Security']);checked('dj-block',true);assert.ok(!q('#dj-middleware-output').textContent.includes('View'));
assert.deepEqual(lab.queries(0),{naive:1,select:1,prefetch:1});input('dj-rows',20);assert.equal(q('#dj-naive').textContent,'21');
assert.throws(()=>lab.queries(-1),RangeError);assert.equal(lab.form(' x ',2,true).title,'x');
checked('dj-own-tag',true);input('dj-title',' <script>test</script> ');assert.equal(q('#dj-form-state').textContent,'驗證通過');assert.equal(q('#dj-form-output script'),null);
checked('dj-own-tag',false);assert.equal(q('#dj-form-state').textContent,'拒絕寫入');input('dj-priority',4);assert.ok(q('#dj-form-output').textContent.includes('優先度'));
assert.equal(lab.access('POST',true,true,false),403);assert.equal(lab.access('GET',false,true,true),302);
assert.equal(lab.access('GET',true,false,true),404);assert.equal(lab.access('POST',true,true,true),302);
checked('dj-auth',true);checked('dj-owner',false);checked('dj-csrf',true);assert.equal(q('#dj-status').textContent,'404');checked('dj-csrf',false);assert.equal(q('#dj-status').textContent,'403');
assert.equal(lab.prg(true,true).writes,1);assert.equal(lab.prg(true,false).writes,2);assert.equal(lab.prg(false,false).writes,0);
checked('dj-valid',true);checked('dj-redirect',false);assert.equal(q('#dj-writes').textContent,'2');
assert.deepEqual(lab.cache(.8,1,21,12,5),{expected:4.999999999999999,pages:3});
input('dj-hit',1);assert.equal(q('#dj-expected').textContent,'1');input('dj-total',0);assert.equal(q('#dj-pages').textContent,'1');
assert.ok(lab.task('immediate',true,false).includes('同程序'));select('dj-backend','external');checked('dj-committed',true);checked('dj-worker',false);assert.ok(q('#dj-task-state').textContent.includes('等待worker'));
checked('dj-committed',false);assert.ok(q('#dj-task-state').textContent.includes('不enqueue'));
for(const svg of document.querySelectorAll('.tf-plot')){assert.equal(svg.getAttribute('role'),'img');assert.ok(svg.querySelector('title'));assert.ok(!/NaN|Infinity/.test(svg.innerHTML));}
const course=window.COURSE;let equations=0,examples=0;const used=new Set();
for(const l of course.lessons){
  navigate(l.id);assert.equal(q('.lesson-header h1').textContent,l.title);assert.ok(q('.tf-task').textContent.includes(l.title));
  assert.equal(document.querySelectorAll('.chapter-link[aria-current="page"]').length,1);
  used.add(q('.tf-figure img').getAttribute('src'));
  for(const a of document.querySelectorAll('.toc-links a'))assert.ok(document.getElementById(a.getAttribute('href').split('/')[1]));
  if(l.example){examples++;assert.equal(q('.example-download a').getAttribute('href'),'examples.zip');}
  const {document:doc}=parseHTML(`<!doctype html><html><body>${l.html}</body></html>`);
  for(const m of doc.querySelectorAll('.math-source,.math-block')){assert.ok(m.querySelector('.katex'));assert.ok(katex.renderToString(m.getAttribute('data-tex'),{throwOnError:true}));equations++;}
}
assert.equal(used.size,28);assert.ok(equations>=20);assert.ok(examples>=24);
navigate('001-web-and-django');q('#complete-lesson').click();assert.equal(q('#progress-count').textContent,'1 / 84');
q('#lesson-notes').value='Model與migration不同；owner範圍每次檢查。';q('#lesson-notes').dispatchEvent(new Event('input'));
navigate('007-project-layout');navigate('001-web-and-django');assert.equal(q('#lesson-notes').value,'Model與migration不同；owner範圍每次檢查。');assert.equal(storage.get('learning-notes:finetuning:v1'),old);
q('#open-search').click();for(const term of ['6.1.3','CSRF','FETCH_RAISE','SQLite','GitHub Pages']){q('#search-input').value=term;q('#search-input').dispatchEvent(new Event('input'));assert.ok(document.querySelectorAll('.search-result').length>0,term);}
q('#close-search').click();q('#menu-toggle').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'true');q('#sidebar-shade').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'false');
navigate('overview');assert.equal(document.querySelectorAll('.tf-lab').length,8);assert.equal(q('#dj-naive').textContent,'21');assert.equal(q('#dj-pages').textContent,'3');
export const report={slug:'django',modules:14,units:84,figures:28,equations,examples,labs:'8 deterministic labs PASS',reader:'search/notes/progress/downloads/menu/remount PASS',isolation:'existing fine-tuning notes preserved',limit:'DOM simulation, not browser layout review'};
