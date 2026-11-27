/* Reader integration and fixed visual labs. DOM QA is separate from browser layout. */
import {readFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
import {parseHTML,Event,HTMLElement} from '../.qa/vendor/linkedom.mjs';
import {parse} from '../.qa/vendor/acorn.mjs';
import katex from '../.qa/vendor/katex.mjs';
const root=new URL('../',import.meta.url),read=f=>readFile(new URL(f,root),'utf8');
for(const f of ['assets/reader.js','multimodal/assets/overview.js','multimodal/assets/course-data.js'])parse(await read(f),{ecmaVersion:'latest'});
const {document:home}=parseHTML(await read('index.html'));
assert.equal(home.querySelectorAll('.subject-feature').length,Object.keys(JSON.parse(await read('tools/library.json')).courses).length);
assert.equal(home.querySelectorAll('a[href="multimodal/index.html"]').length,1);
const {window,document}=parseHTML(await read('multimodal/index.html'));
const legacy=JSON.stringify({completed:['001-data-lifecycle'],notes:{'001-data-lifecycle':'SQL原本的筆記'}});
const storage=new Map([['learning-notes:sql:v1',legacy]]),location={hash:''},q=s=>document.querySelector(s);
HTMLElement.prototype.focus=function(){};HTMLElement.prototype.scrollIntoView=function(){};
if(!Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'checked'))Object.defineProperty(window.HTMLInputElement.prototype,'checked',{get(){return this.hasAttribute('checked');},set(v){v?this.setAttribute('checked',''):this.removeAttribute('checked');}});
window.scrollTo=()=>{};window.print=()=>{};q('#search-dialog').showModal=function(){this.open=true;};q('#search-dialog').close=function(){this.open=false;};
window.katex={render:(tex,el,options)=>{el.innerHTML=katex.renderToString(tex,options);}};
Object.assign(globalThis,{window,document,location,requestAnimationFrame:fn=>fn(),localStorage:{getItem:k=>storage.get(k)??null,setItem:(k,v)=>storage.set(k,v)}});
await import(new URL('assets/math.js',root).href);await import(new URL('multimodal/assets/course-data.js',root).href);await import(new URL('multimodal/assets/overview.js',root).href);await import(new URL('assets/reader.js',root).href);
const navigate=id=>{location.hash='#'+id;window.dispatchEvent(new Event('hashchange'));};
const input=(id,v)=>{q('#'+id).value=String(v);q('#'+id).dispatchEvent(new Event('input'));};
const checked=(id,v)=>{q('#'+id).checked=v;q('#'+id).dispatchEvent(new Event('change'));};
const select=(id,v)=>{for(const x of q('#'+id).querySelectorAll('option'))x.selected=false;q('#'+id).querySelector(`option[value="${v}"]`).selected=true;q('#'+id).dispatchEvent(new Event('change'));};
assert.equal(document.querySelectorAll('.chapter-link').length,96);assert.equal(document.querySelectorAll('.module-row').length,16);
assert.equal(document.querySelectorAll('.tf-lab').length,12);assert.equal(document.querySelectorAll('.tf-atlas img').length,32);
for(const e of document.querySelectorAll('.tf-lab input,.tf-lab select'))assert.ok(q(`label[for="${e.id}"]`));
for(const a of document.querySelectorAll('a[href^="#"]')){const id=a.getAttribute('href').slice(1);if(id==='main'||id.startsWith('overview'))continue;assert.ok(window.COURSE.lessons.some(l=>l.id===id),id);}
const lab=window.MultimodalLab;
assert.deepEqual(lab.dpi(144),{pixelWidth:1224,pixelHeight:1584,box:[700,776,900,812]});input('mm-resolution',72);assert.ok(q('#mm-pixel-size').textContent.includes('612'));
assert.equal(lab.overlap(0),1);assert.equal(lab.overlap(200),0);assert.equal(lab.overlap(100),1/3);input('mm-offset',300);assert.equal(q('#mm-iou-value').textContent,'0');
assert.equal(lab.tiling(64).length,6);assert.equal(lab.tiling(256).length,12);input('mm-overlap',256);assert.equal(q('#mm-tile-count').textContent,'12');
assert.equal(lab.order(false)[1],'D 右欄一');checked('mm-columns',true);assert.ok(q('#mm-order-output').textContent.indexOf('B 左欄二')<q('#mm-order-output').textContent.indexOf('D 右欄一'));
assert.deepEqual(lab.edit('4725','472S'),{distance:1,cer:.25});assert.equal(lab.edit('A','AAAA').cer,3);assert.equal(lab.edit('😀','😀').distance,0);input('mm-reference','');assert.ok(q('#mm-cer').textContent.includes('未定義'));input('mm-reference','<img src=x>');input('mm-prediction','<script>run</script>');assert.equal(q('#mm-edit-output script'),null);assert.equal(q('#mm-edit-output img'),null);
assert.equal(lab.headers(false).unique,false);checked('mm-preserve',true);assert.ok(q('#mm-header-state').textContent.includes('可區分'));
assert.equal(lab.reconcile(4500,225,4725).valid,true);input('mm-total',4726);assert.ok(q('#mm-money-state').textContent.includes('失敗'));
assert.ok(lab.contrastive(.1,false).loss<lab.contrastive(.1,true).loss);checked('mm-swap',true);assert.ok(Number(q('#mm-loss-value').textContent)>9);input('mm-temperature',.05);assert.ok(Number.isFinite(lab.contrastive(.05,true).loss));
assert.equal(lab.grounding(0,false).valid,true);checked('mm-wrong-region',true);assert.ok(q('#mm-ground-state').textContent.includes('錯框'));select('mm-page','1');assert.ok(q('#mm-ground-state').textContent.includes('錯頁'));
assert.deepEqual(lab.coverage(.9),{selected:[{score:.99,ok:false},{score:.95,ok:true}],coverage:.5,risk:.5});input('mm-threshold',100);assert.equal(q('#mm-coverage').textContent,'0%');assert.ok(q('#mm-risk-output').textContent.includes('未定義'));
assert.equal(lab.budget(4,false).estimated,3600);checked('mm-crops',true);assert.equal(q('#mm-estimate').textContent,'9600');
assert.equal(lab.timeline(1500).frame,3);assert.ok(lab.timeline(1500).transcript.startsWith('B'));input('mm-ms',3000);assert.ok(q('#mm-time-state').textContent.includes('結束'));assert.equal(lab.timeline(2000).frame,null);
for(const fn of [()=>lab.dpi(NaN),()=>lab.overlap(-1),()=>lab.tiling(512),()=>lab.edit('x'.repeat(81),''),()=>lab.reconcile(1.1,2,3),()=>lab.contrastive(0,false),()=>lab.grounding(2,false),()=>lab.coverage(Infinity),()=>lab.budget(0,false),()=>lab.timeline(3001)])assert.throws(fn,RangeError);
for(const svg of document.querySelectorAll('.tf-plot')){assert.equal(svg.getAttribute('role'),'img');assert.ok(svg.querySelector('title'));assert.ok(!/NaN|Infinity/.test(svg.innerHTML));}
for(const el of document.querySelectorAll('.tf-lab .math-block'))assert.ok(el.querySelector('.katex'));
let equations=0,examples=0;const used=new Set();
for(const l of window.COURSE.lessons){
  navigate(l.id);assert.equal(q('.lesson-header h1').textContent,l.title);assert.ok(q('.tf-task').textContent.includes(l.title));used.add(q('.tf-figure img').getAttribute('src'));
  assert.equal(document.querySelectorAll('.chapter-link[aria-current="page"]').length,1);
  for(const a of document.querySelectorAll('.toc-links a'))assert.ok(document.getElementById(a.getAttribute('href').split('/')[1]));
  if(l.example){examples++;assert.equal(q('.example-download a').getAttribute('href'),'examples.zip');}
  const {document:doc}=parseHTML(`<!doctype html><html><body>${l.html}</body></html>`);
  for(const m of doc.querySelectorAll('.math-source,.math-block')){assert.ok(m.querySelector('.katex'));katex.renderToString(m.getAttribute('data-tex'),{throwOnError:true});equations++;}
}
assert.equal(used.size,32);assert.equal(examples,96);assert.ok(equations>40);
navigate('001-task-map');q('#complete-lesson').click();assert.equal(q('#progress-count').textContent,'1 / 96');q('#lesson-notes').value='來源、頁面、區域與quote一起驗證。';q('#lesson-notes').dispatchEvent(new Event('input'));
navigate('049-openai-pdf');navigate('001-task-map');assert.equal(q('#lesson-notes').value,'來源、頁面、區域與quote一起驗證。');assert.equal(storage.get('learning-notes:sql:v1'),legacy);
q('#open-search').click();for(const term of ['2.2','OCR','4725','MaxSim','ASR']){q('#search-input').value=term;q('#search-input').dispatchEvent(new Event('input'));assert.ok(document.querySelectorAll('.search-result').length,term);}q('#close-search').click();
q('#menu-toggle').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'true');q('#sidebar-shade').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'false');
navigate('overview');assert.equal(document.querySelectorAll('.tf-lab').length,12);assert.equal(q('#mm-cer').textContent,'0.25');assert.equal(q('#mm-tile-count').textContent,'6');
const ids=[...document.querySelectorAll('[id]')].map(x=>x.id);assert.equal(ids.length,new Set(ids).size);
export const report={slug:'multimodal',modules:16,units:96,figures:32,equations,examples,labs:'12 visual experiments PASS',reader:'math/search/progress/notes/downloads/menu/remount PASS',isolation:'SQL notes preserved',limit:'DOM emulation, not real-browser layout'};
