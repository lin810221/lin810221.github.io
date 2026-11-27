/* DOM regression only; actual browser layout has a separate validation boundary. */
import {readFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
import {parseHTML,Event,HTMLElement} from '../.qa/vendor/linkedom.mjs';
import {parse} from '../.qa/vendor/acorn.mjs';
import katex from '../.qa/vendor/katex.mjs';
const root=new URL('../',import.meta.url),read=file=>readFile(new URL(file,root),'utf8');
for(const file of ['assets/reader.js','finetuning/assets/overview.js','finetuning/assets/course-data.js'])parse(await read(file),{ecmaVersion:'latest'});
const {document:home}=parseHTML(await read('index.html'));
assert.equal(home.querySelectorAll('.subject-feature').length,Object.keys(JSON.parse(await readFile(new URL('tools/library.json',root),'utf8')).courses).length);
assert.equal(home.querySelectorAll('a[href="finetuning/index.html"]').length,1);
const {window,document}=parseHTML(await read('finetuning/index.html'));
const old=JSON.stringify({completed:['001-lm-task'],notes:{'001-lm-task':'原理課筆記'}});
const storage=new Map([['learning-notes:transformer:v1',old]]),location={hash:''},q=s=>document.querySelector(s);
HTMLElement.prototype.focus=function(){};HTMLElement.prototype.scrollIntoView=function(){};
window.scrollTo=()=>{};window.print=()=>{};
q('#search-dialog').showModal=function(){this.open=true;};q('#search-dialog').close=function(){this.open=false;};
window.katex={render:(tex,el,options)=>{el.innerHTML=katex.renderToString(tex,options);}};
Object.assign(globalThis,{window,document,location,requestAnimationFrame:fn=>fn(),localStorage:{getItem:k=>storage.get(k)??null,setItem:(k,v)=>storage.set(k,v)}});
await import(new URL('assets/math.js',root).href);
await import(new URL('finetuning/assets/course-data.js',root).href);
await import(new URL('finetuning/assets/overview.js',root).href);
await import(new URL('assets/reader.js',root).href);
const navigate=id=>{location.hash='#'+id;window.dispatchEvent(new Event('hashchange'));};
const input=(id,value)=>{q('#'+id).value=String(value);q('#'+id).dispatchEvent(new Event('input'));};
const near=(a,b,tol=1e-6)=>assert.ok(Math.abs(a-b)<tol,`${a} vs ${b}`);
assert.equal(q('.topbar-subject').textContent,'LLM 微調與模型適應');
assert.equal(document.querySelectorAll('.chapter-link').length,72);
assert.equal(document.querySelectorAll('.module-row').length,12);
assert.equal(document.querySelectorAll('.tf-lab').length,8);
assert.equal(document.querySelectorAll('.tf-atlas img').length,24);
for(const e of document.querySelectorAll('.tf-lab input,.tf-lab select'))assert.ok(q(`label[for="${e.id}"]`));
const lab=window.FinetuningLab;
near(lab.masked([.5,.25],[true,true]).loss,-Math.log(.125)/2);
assert.throws(()=>lab.masked([.5],[false]),RangeError);
near(Number(q('#ft-mask-loss').textContent),1.039721);
q('#ft-user').checked=true;q('#ft-user').dispatchEvent(new Event('change'));
near(Number(q('#ft-mask-loss').textContent),lab.masked([.9,.9,.5,.25],[true,true,true,true]).loss);
assert.deepEqual(lab.lora(100,200,4,8),{base:20000,adapter:1200,scale:2,rsScale:4});
input('ft-rank',16);assert.equal(q('#ft-lora-count').textContent,'131,072');
assert.throws(()=>lab.lora(1,1,0,1),RangeError);
assert.equal(lab.quantize([0,1],4).mse,0);
input('ft-bits',8);assert.ok(Number(q('#ft-quant-mse').textContent)<.0001);
const m=lab.memory(7e9,8e6,4,1);assert.equal(m.base,3.5e9);assert.equal(m.states,128e6);
assert.throws(()=>lab.memory(-1,2,4,0),RangeError);
near(lab.aggregate(2,8),2.6);input('ft-count-a',8);assert.equal(q('#ft-acc-loss').textContent,'2');
near(lab.dpo(1,1,.2).loss,Math.log(2));assert.ok(lab.dpo(3,1,.2).loss<lab.dpo(0,1,.2).loss);
input('ft-gap',1);near(Number(q('#ft-dpo-loss').textContent),Math.log(2));
assert.throws(()=>lab.dpo(1,0,0),RangeError);
for(const t of [.5,1,2,6]){const r=lab.kd(t);near(r.teacher.reduce((a,b)=>a+b,0),1);assert.ok(r.loss>=0);}
input('ft-temperature',6);assert.ok(q('#ft-kd-output .katex'));
assert.deepEqual(lab.budget(120,3,4,4),{microbatches:90,updates:24,exposures:360});
input('ft-accumulation',1);assert.equal(q('#ft-budget-updates').textContent,'90');
for(const svg of document.querySelectorAll('.tf-plot')){assert.equal(svg.getAttribute('role'),'img');assert.ok(svg.querySelector('title'));assert.ok(!/NaN|Infinity/.test(svg.innerHTML));}
const course=window.COURSE,allIds=new Set(course.lessons.map(l=>l.id));let equations=0,examples=0;const used=new Set();
for(const lesson of course.lessons){
  navigate(lesson.id);assert.equal(q('.lesson-header h1').textContent,lesson.title);
  assert.equal(document.querySelectorAll('.chapter-link[aria-current="page"]').length,1);
  assert.ok(q('.tf-task').textContent.includes(lesson.title));
  const figure=q('.tf-figure img');assert.ok(figure.getAttribute('alt').length>=20);used.add(figure.getAttribute('src'));
  for(const link of document.querySelectorAll('.toc-links a'))assert.ok(document.getElementById(link.getAttribute('href').split('/')[1]));
  if(lesson.example){examples++;assert.equal(q('.example-download a').getAttribute('href'),'examples.zip');}
  const {document:doc}=parseHTML(`<!doctype html><html><body>${lesson.html}</body></html>`);
  const pageIds=[...doc.querySelectorAll('[id]')].map(x=>x.id);assert.equal(pageIds.length,new Set(pageIds).size);
  for(const e of doc.querySelectorAll('.math-source,.math-block')){
    const tex=e.getAttribute('data-tex');assert.ok(tex);
    assert.ok(e.querySelector('.katex'));assert.ok(katex.renderToString(tex,{throwOnError:true}).includes('class="katex'));equations++;
  }
}
assert.equal(used.size,24);assert.ok(examples>=24);assert.ok(equations>=70);
navigate('001-adaptation-map');q('#complete-lesson').click();assert.equal(q('#progress-count').textContent,'1 / 72');
q('#lesson-notes').value='LoRA基底凍結；先核對assistant mask。';q('#lesson-notes').dispatchEvent(new Event('input'));
navigate('007-data-schema');navigate('001-adaptation-map');assert.equal(q('#lesson-notes').value,'LoRA基底凍結；先核對assistant mask。');assert.equal(storage.get('learning-notes:transformer:v1'),old);
q('#open-search').click();for(const term of ['LoRA','DPO','5.24.1','-100','蒸餾']){q('#search-input').value=term;q('#search-input').dispatchEvent(new Event('input'));assert.ok(document.querySelectorAll('.search-result').length>0,term);}
q('#close-search').click();q('#menu-toggle').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'true');q('#sidebar-shade').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'false');
navigate('overview');assert.equal(document.querySelectorAll('.tf-lab').length,8);assert.equal(q('#ft-acc-loss').textContent,'2.6');assert.equal(q('#ft-budget-updates').textContent,'24');
export const report={slug:course.slug,syntax:'PASS',modules:12,units:72,figures:used.size,examples,equations,labs:'8 deterministic numerical labs PASS',reader:'TOC/search/notes/progress/downloads/menu/remount PASS',isolation:'Transformer notes preserved',limit:'DOM simulation, not browser layout review'};
