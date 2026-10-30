/* DOM emulation, numerical lab checks and KaTeX validation; no layout claims. */
import {readFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
import {parseHTML,Event,HTMLElement} from '../.qa/vendor/linkedom.mjs';
import {parse} from '../.qa/vendor/acorn.mjs';
import katex from '../.qa/vendor/katex.mjs';
const root=new URL('../',import.meta.url),read=file=>readFile(new URL(file,root),'utf8');
for(const file of ['assets/reader.js','pytorch/assets/overview.js','pytorch/assets/course-data.js'])parse(await read(file),{ecmaVersion:'latest'});
const {document:home}=parseHTML(await read('index.html'));
assert.ok(home.querySelectorAll('.subject-feature').length>=5);
assert.equal(home.querySelectorAll('a[href="pytorch/index.html"]').length,1);
const {window,document}=parseHTML(await read('pytorch/index.html'));
const oldNotes=JSON.stringify({completed:['01-representation'],notes:{'01-representation':'existing note'}});
const storage=new Map([['learning-notes:embedding:v1',oldNotes]]),location={hash:''};
const q=s=>document.querySelector(s);
HTMLElement.prototype.focus=function(){};HTMLElement.prototype.scrollIntoView=function(){};
window.scrollTo=()=>{};window.print=()=>{};
q('#search-dialog').showModal=function(){this.open=true;};q('#search-dialog').close=function(){this.open=false;};
Object.assign(globalThis,{window,document,location,localStorage:{getItem:k=>storage.get(k)??null,setItem:(k,v)=>storage.set(k,v)},requestAnimationFrame:fn=>fn()});
await import(new URL('pytorch/assets/course-data.js',root).href);
await import(new URL('pytorch/assets/overview.js',root).href);
await import(new URL('assets/reader.js',root).href);
assert.equal(q('.topbar-subject').textContent,'PyTorch');
assert.equal(document.querySelectorAll('.chapter-link').length,48);
assert.equal(document.querySelectorAll('.module-row').length,8);
assert.equal(document.querySelectorAll('.torch-lab').length,4);
assert.equal(q('#shape-result').textContent,'[4,4]');
assert.equal(document.querySelectorAll('.torch-cell').length,16);
const lab=window.PyTorchLab;
assert.deepEqual(lab.broadcast([3,4],[4]),[3,4]);
assert.deepEqual(lab.broadcast([3,1],[3]),[3,3]);
assert.throws(()=>lab.broadcast([3,4],[3]),RangeError);
assert.throws(()=>lab.broadcast([0],[1]),RangeError);
assert.deepEqual(lab.gradient(3,2,0,10),{prediction:6,error:-4,loss:16,dw:-24,db:-8});
assert.throws(()=>lab.gradient(NaN,1,0,0),RangeError);
Object.defineProperty(q('#shape-target'),'value',{value:'flat',writable:true,configurable:true});
const input=id=>q(id).dispatchEvent(new Event('input')),change=id=>q(id).dispatchEvent(new Event('change'));
q('#shape-target').value='column';change('#shape-target');
assert.equal(q('#shape-result').textContent,'[4,1]');assert.equal(document.querySelectorAll('.torch-cell').length,4);
q('#shape-size').value='6';input('#shape-size');assert.equal(q('#shape-result').textContent,'[6,1]');
assert.equal(q('#grad-loss').textContent,'16');assert.equal(q('#grad-dw').textContent,'-24');
q('#grad-w').value='3';q('#grad-b').value='1';input('#grad-w');
assert.equal(q('#grad-loss').textContent,'0');assert.equal(q('#grad-dw').textContent,'0');
q('#grad-w').value='-2';input('#grad-w');assert.ok(!q('#gradient-graph').innerHTML.includes('NaN'));
const state=()=>JSON.parse(q('#step-state').textContent),next=()=>q('#step-next').click();
assert.equal(state().w,2);next();next();next();next();
assert.equal(state().w,2);assert.equal(state().grad,-24);
next();assert.equal(state().w,2.24);assert.equal(state().optimizer_updates,1);
// Compare a deliberately stale gradient on the second update.
q('#step-clear').checked=false;for(let i=0;i<5;i++)next();
assert.equal(state().grad,-43.68);assert.equal(state().w,2.6768);
q('#step-reset').click();for(let i=0;i<10;i++)next();
assert.equal(state().grad,-19.68);assert.equal(state().w,2.4368);
assert.deepEqual(lab.batching(10,4,2),{sizes:[4,4,2],count:10,groups:[8,2],dropped:0,weighted:1.8,naive:2});
assert.deepEqual(lab.batching(10,4,2,true).sizes,[4,4]);
assert.throws(()=>lab.batching(1,0,1),RangeError);
assert.equal(q('#batch-weighted').textContent,'1.8');assert.equal(q('#batch-naive').textContent,'2');
q('#batch-drop').checked=true;change('#batch-drop');assert.equal(q('#batch-count').textContent,'8 / 10');
assert.equal(q('#batch-weighted').textContent,'1.5');
q('#batch-n').value='2';q('#batch-size').value='8';input('#batch-n');
assert.equal(q('#batch-count').textContent,'0 / 2');assert.equal(q('#batch-weighted').textContent,'—');
assert.ok(q('#batch-groups').textContent.includes('沒有有效'));

function navigate(id){location.hash='#'+id;window.dispatchEvent(new Event('hashchange'));}
let equations=0,examples=0;
for(const lesson of window.COURSE.lessons){
  navigate(lesson.id);
  assert.equal(q('.lesson-header h1').textContent,lesson.title);
  assert.ok(q('.lesson-breadcrumb').textContent.startsWith('PyTorch'));
  for(const link of document.querySelectorAll('.toc-links a'))assert.ok(document.getElementById(link.getAttribute('href').split('/')[1]));
  if(lesson.example){examples++;assert.equal(q('.example-download a').getAttribute('href'),'examples.zip');}
  const {document:doc}=parseHTML(`<!doctype html><html><body>${lesson.html}</body></html>`);
  for(const element of doc.querySelectorAll('.math-source,.math-block')){
    const display=element.classList.contains('math-block'),text=element.textContent.trim();
    const tex=display?text.slice(2,-2).trim():text.slice(1,-1);
    assert.ok(katex.renderToString(tex,{displayMode:display,throwOnError:true}).includes('class="katex'));equations++;
  }
}
assert.equal(examples,24);assert.ok(equations>=12);
navigate('01-mental-model');q('#complete-lesson').click();assert.equal(q('#progress-count').textContent,'1 / 48');
q('#lesson-notes').value='eval 不會清除梯度。';input('#lesson-notes');
navigate('02-installation');navigate('01-mental-model');assert.equal(q('#lesson-notes').value,'eval 不會清除梯度。');
assert.equal(storage.get('learning-notes:embedding:v1'),oldNotes);
assert.equal(JSON.parse(storage.get('learning-notes:pytorch:v1')).completed.length,1);
q('#open-search').click();
for(const term of ['GradScaler','續訓','2.15.0','DataLoader']){q('#search-input').value=term;input('#search-input');assert.ok(document.querySelectorAll('.search-result').length>0);}
q('#close-search').click();q('#menu-toggle').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'true');
q('#sidebar-shade').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'false');
navigate('overview');assert.equal(document.querySelectorAll('.torch-lab').length,4);assert.equal(q('#shape-result').textContent,'[4,4]');assert.equal(state().w,2);
export const report={syntax:'PASS',chapters:48,modules:8,examples,equations,
 labs:'broadcast, analytic gradients, SGD state, stale gradients, weighted tail batches: PASS',
 reader:'TOC, download, search, notes, progress, menu, remount: PASS',isolation:'Embedding notes preserved',limit:'DOM emulation; no real-browser layout check'};
