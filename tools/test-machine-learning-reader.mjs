/* Numerical demonstrations and full reader DOM checks, not browser layout QA. */
import {readFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
import {parseHTML,Event,HTMLElement} from '../.qa/vendor/linkedom.mjs';
import {parse} from '../.qa/vendor/acorn.mjs';
import katex from '../.qa/vendor/katex.mjs';
const root=new URL('../',import.meta.url),read=file=>readFile(new URL(file,root),'utf8');
for(const file of ['assets/reader.js','machine-learning/assets/overview.js','machine-learning/assets/course-data.js'])parse(await read(file),{ecmaVersion:'latest'});
const {document:home}=parseHTML(await read('index.html'));
assert.ok(home.querySelectorAll('.subject-feature').length>=6);
assert.equal(home.querySelectorAll('a[href="machine-learning/index.html"]').length,1);
const {window,document}=parseHTML(await read('machine-learning/index.html'));
const savedTorch=JSON.stringify({completed:['01-mental-model'],notes:{'01-mental-model':'prior PyTorch note'}});
const storage=new Map([['learning-notes:pytorch:v1',savedTorch]]),location={hash:''};
const q=s=>document.querySelector(s);
HTMLElement.prototype.focus=function(){};HTMLElement.prototype.scrollIntoView=function(){};
window.scrollTo=()=>{};window.print=()=>{};
q('#search-dialog').showModal=function(){this.open=true;};q('#search-dialog').close=function(){this.open=false;};
Object.assign(globalThis,{window,document,location,requestAnimationFrame:fn=>fn(),
  localStorage:{getItem:k=>storage.get(k)??null,setItem:(k,v)=>storage.set(k,v)}});
await import(new URL('machine-learning/assets/course-data.js',root).href);
await import(new URL('machine-learning/assets/overview.js',root).href);
await import(new URL('assets/reader.js',root).href);
assert.equal(q('.topbar-subject').textContent,'機器學習');
assert.equal(document.querySelectorAll('.chapter-link').length,60);
assert.equal(document.querySelectorAll('.module-row').length,10);
assert.equal(document.querySelectorAll('.ml-lab').length,5);
const lab=window.MachineLearningLab;
const line=[[-1,-1],[0,1],[1,3]];
assert.deepEqual(lab.ols(line),{w:2,b:1});assert.equal(lab.regression(line,2,1).mse,0);
assert.throws(()=>lab.ols([[1,2],[1,3]]),RangeError);
const before=Number(q('#reg-mse').textContent);q('#reg-fit').click();
assert.equal(q('#reg-w').value,'2.00');assert.equal(q('#reg-b').value,'1.00');
assert.ok(Number(q('#reg-mse').textContent)<before);assert.ok(Math.abs(Number(q('#reg-mse').textContent)-.88/7)<1e-4);
const input=id=>q(id).dispatchEvent(new Event('input')),change=id=>q(id).dispatchEvent(new Event('change'));
q('#reg-w').value='4';input('#reg-w');assert.ok(!q('#reg-plot').innerHTML.includes('NaN'));
assert.equal(q('#decision-cost').textContent,'7');assert.equal(q('#decision-precision').textContent,'60.0%');assert.equal(q('#decision-recall').textContent,'75.0%');
q('#decision-optimize').click();assert.equal(Number(q('#decision-threshold').value),.4);assert.equal(q('#decision-cost').textContent,'2');
q('#decision-threshold').value='1.01';input('#decision-threshold');assert.equal(q('#decision-precision').textContent,'0.0%');assert.equal(q('#decision-recall').textContent,'0.0%');
assert.deepEqual(lab.bestThreshold([1,1,0,0],[.9,.4,.8,.1],5,1),{threshold:.4,cost:1});
assert.throws(()=>lab.metrics([1],[2],.5),RangeError);
assert.equal(q('#cv-mean').textContent,'7.5');assert.equal(q('#cv-count').textContent,'16');
assert.equal(document.querySelectorAll('.ml-row.validation').length,4);
for(const [id,val] of [['cv-policy','safe'],['cluster-k','3'],['cluster-init','spread']])Object.defineProperty(q('#'+id),'value',{value:val,writable:true,configurable:true});
q('#cv-policy').value='leaked';change('#cv-policy');assert.equal(q('#cv-count').textContent,'20');assert.equal(q('#cv-mean').textContent,'14.3');
assert.equal(document.querySelectorAll('.ml-row.leaked').length,4);
q('#cv-fold').value='1';q('#cv-policy').value='safe';change('#cv-policy');assert.equal(q('#cv-count').textContent,'16');
assert.throws(()=>lab.foldStats([1,2,3],0),RangeError);
assert.equal(q('#tree-parent').textContent,'0.5');assert.equal(q('#tree-weighted').textContent,'0.2');assert.equal(q('#tree-gain').textContent,'0.3');
q('#tree-threshold').value='4.5';input('#tree-threshold');assert.equal(q('#tree-gain').textContent,'0.125');
assert.equal(lab.gini([0,0,1,1]),.5);
assert.equal(lab.split([{x:1,y:0},{x:2,y:0},{x:3,y:1},{x:4,y:1}],2.5).gain,.5);
assert.equal(lab.split([{x:1,y:0},{x:2,y:1}],0).gain,null);
assert.throws(()=>lab.split([],0),RangeError);
const points=[[0,0],[2,0],[10,0],[12,0]],centers=[[0,0],[10,0]],step=lab.lloyd(points,centers);
assert.deepEqual(step.centers,[[1,0],[11,0]]);assert.deepEqual(step.assignment,[0,0,1,1]);assert.equal(step.inertia,4);
assert.equal(lab.lloyd(points,step.centers).changed,false);
assert.deepEqual(lab.lloyd([[0,0],[1,0]],[[0,0],[100,100]]).counts,[2,0]);
let previous=Number(q('#cluster-inertia').textContent);
for(let i=0;i<10;i++){q('#cluster-step').click();const current=Number(q('#cluster-inertia').textContent);assert.ok(current<=previous+1e-4);previous=current;}
assert.ok(q('#cluster-step').disabled);assert.ok(!q('#cluster-plot').innerHTML.includes('NaN'));
q('#cluster-k').value='2';change('#cluster-k');assert.equal(document.querySelectorAll('.ml-center').length,2);assert.equal(q('#cluster-iteration').textContent,'0');
q('#cluster-init').value='crowded';change('#cluster-init');q('#cluster-step').click();assert.equal(q('#cluster-iteration').textContent,'1');q('#cluster-reset').click();assert.equal(q('#cluster-iteration').textContent,'0');

function navigate(id){location.hash='#'+id;window.dispatchEvent(new Event('hashchange'));}
let equations=0,examples=0;
for(const lesson of window.COURSE.lessons){
  navigate(lesson.id);assert.equal(q('.lesson-header h1').textContent,lesson.title);
  assert.ok(q('.lesson-breadcrumb').textContent.startsWith('機器學習'));
  assert.equal(document.querySelectorAll('.chapter-link[aria-current="page"]').length,1);
  for(const link of document.querySelectorAll('.toc-links a'))assert.ok(document.getElementById(link.getAttribute('href').split('/')[1]));
  if(lesson.example){examples++;assert.equal(q('.example-download a').getAttribute('href'),'examples.zip');}
  const {document:doc}=parseHTML(`<!doctype html><html><body>${lesson.html}</body></html>`);
  for(const element of doc.querySelectorAll('.math-source,.math-block')){
    const text=element.textContent.trim(),display=element.classList.contains('math-block');
    const tex=display?text.slice(2,-2).trim():text.slice(1,-1);
    assert.ok(katex.renderToString(tex,{displayMode:display,throwOnError:true}).includes('class="katex'));equations++;
  }
}
assert.equal(examples,30);assert.ok(equations>=30);
navigate('01-first-model');q('#complete-lesson').click();assert.equal(q('#progress-count').textContent,'1 / 60');
q('#lesson-notes').value='選模與門檻都要有資料邊界。';input('#lesson-notes');navigate('02-environment');navigate('01-first-model');
assert.equal(q('#lesson-notes').value,'選模與門檻都要有資料邊界。');
assert.equal(storage.get('learning-notes:pytorch:v1'),savedTorch);
assert.equal(JSON.parse(storage.get('learning-notes:machine-learning:v1')).completed.length,1);
q('#open-search').click();for(const term of ['Ridge','HDBSCAN','交叉驗證','FrozenEstimator']){q('#search-input').value=term;input('#search-input');assert.ok(document.querySelectorAll('.search-result').length>0);}
q('#close-search').click();q('#menu-toggle').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'true');q('#sidebar-shade').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'false');
navigate('overview');assert.equal(document.querySelectorAll('.ml-lab').length,5);assert.equal(q('#cv-count').textContent,'16');assert.equal(q('#cluster-iteration').textContent,'0');
export const report={syntax:'PASS',chapters:60,modules:10,examples,equations,
  labs:'OLS, cost thresholds, CV leakage boundaries, weighted Gini, Lloyd iterations: PASS',
  reader:'TOC, downloads, search, notes, progress, menu, remount: PASS',
  isolation:'PyTorch notes preserved',limit:'DOM emulation; no real-browser layout review'};
