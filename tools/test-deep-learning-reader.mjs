/* Real numerical/reader DOM QA; this does not assess browser layout. */
import {readFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
import {parseHTML,Event,HTMLElement} from '../.qa/vendor/linkedom.mjs';
import {parse} from '../.qa/vendor/acorn.mjs';
import katex from '../.qa/vendor/katex.mjs';
const root=new URL('../',import.meta.url),read=file=>readFile(new URL(file,root),'utf8');
for(const file of ['assets/reader.js','deep-learning/assets/overview.js','deep-learning/assets/course-data.js'])parse(await read(file),{ecmaVersion:'latest'});
const {document:home}=parseHTML(await read('index.html'));
assert.ok(home.querySelectorAll('.subject-feature').length>=7);
assert.equal(home.querySelectorAll('a[href="deep-learning/index.html"]').length,1);
const {window,document}=parseHTML(await read('deep-learning/index.html'));
const savedML=JSON.stringify({completed:['01-first-model'],notes:{'01-first-model':'existing ML notes'}});
const storage=new Map([['learning-notes:machine-learning:v1',savedML]]),location={hash:''},q=s=>document.querySelector(s);
HTMLElement.prototype.focus=function(){};HTMLElement.prototype.scrollIntoView=function(){};
window.scrollTo=()=>{};window.print=()=>{};
q('#search-dialog').showModal=function(){this.open=true;};q('#search-dialog').close=function(){this.open=false;};
Object.assign(globalThis,{window,document,location,requestAnimationFrame:fn=>fn(),localStorage:{getItem:k=>storage.get(k)??null,setItem:(k,v)=>storage.set(k,v)}});
await import(new URL('deep-learning/assets/course-data.js',root).href);
await import(new URL('deep-learning/assets/overview.js',root).href);
await import(new URL('assets/reader.js',root).href);
assert.equal(q('.topbar-subject').textContent,'深度學習');
assert.equal(document.querySelectorAll('.chapter-link').length,72);
assert.equal(document.querySelectorAll('.module-row').length,12);
assert.equal(document.querySelectorAll('.dl-lab').length,6);
const ids=[...document.querySelectorAll('[id]')].map(e=>e.id);assert.equal(ids.length,new Set(ids).size);
for(const element of document.querySelectorAll('.dl-lab input,.dl-lab select'))assert.ok(document.querySelector(`label[for="${element.id}"]`));
for(const svg of document.querySelectorAll('.dl-plot')){assert.equal(svg.getAttribute('role'),'img');assert.ok(svg.querySelector('title'));}
const lab=window.DeepLearningLab,near=(a,b,tol=1e-10)=>assert.ok(Math.abs(a-b)<=tol,`${a} vs ${b}`);
near(lab.activation('sigmoid',0).derivative,.25);near(lab.activation('tanh',0).derivative,1);near(lab.activation('relu',0).derivative,0);
for(const name of ['sigmoid','tanh','relu'])for(const x of [-2,.7,2]){
  const numerical=(lab.activation(name,x+1e-5).y-lab.activation(name,x-1e-5).y)/2e-5;
  near(lab.activation(name,x).derivative,numerical,1e-8);
}
assert.throws(()=>lab.activation('wrong',0),RangeError);assert.throws(()=>lab.activation('relu',Infinity),RangeError);
const input=id=>q(id).dispatchEvent(new Event('input')),change=id=>q(id).dispatchEvent(new Event('change'));
for(const [id,value] of [['act-kind','sigmoid'],['conv-kernel','edge'],['norm-mode','batch']])Object.defineProperty(q('#'+id),'value',{value,writable:true,configurable:true});
assert.equal(q('#act-chain').textContent,'9.537e-7');q('#act-kind').value='tanh';change('#act-kind');assert.equal(q('#act-chain').textContent,'1.000e+0');q('#act-x').value='6';input('#act-x');assert.equal(q('#act-y').textContent,'1');
const a=lab.newNetwork(),b=lab.newNetwork();assert.deepEqual(a,b);
const initial=lab.xorLoss(a),step=.0001,index=3,original=a.v[index];
a.v[index]=original+step;const lp=lab.xorLoss(a);a.v[index]=original-step;const lm=lab.xorLoss(a);a.v[index]=original;
lab.train(a,1,.5);near((original-a.v[index])/.5,(lp-lm)/(2*step),1e-8);
lab.train(b,1000);assert.ok(lab.xorLoss(b)<.1&&lab.xorLoss(b)<initial);
for(const [x,y] of [[[0,0],0],[[0,1],1],[[1,0],1],[[1,1],0]])assert.equal(Number(lab.forward(b,x).p>=.5),y);
const uiInitial=Number(q('#xor-loss').textContent);for(let i=0;i<5;i++)q('#xor-train').click();assert.equal(q('#xor-steps').textContent,'1000');assert.equal(q('#xor-correct').textContent,'4 / 4');assert.ok(Number(q('#xor-loss').textContent)<uiInitial);
for(let i=0;i<15;i++)q('#xor-train').click();assert.equal(q('#xor-steps').textContent,'4000');assert.ok(q('#xor-train').disabled);
q('#xor-reset').click();assert.equal(q('#xor-steps').textContent,'0');near(Number(q('#xor-loss').textContent),uiInitial);
assert.throws(()=>lab.train(a,0),RangeError);
assert.deepEqual(lab.convolution([[1,2,3],[4,5,6],[7,8,9]],[[1,0],[0,-1]]),[[-4,-4],[-4,-4]]);
assert.throws(()=>lab.convolution([[1],[2,3]],[[1]]),RangeError);
assert.ok(q('#conv-products').textContent.endsWith('= -8'));q('#conv-position').value='2';input('#conv-position');assert.ok(q('#conv-products').textContent.endsWith('= 8'));
q('#conv-kernel').value='blur';change('#conv-kernel');near(Number(q('#conv-output td').textContent),13/9,1e-4);
const rows=[[1,2,3],[4,8,6],[7,8,9]],modified=rows.map(r=>[...r]);modified[0][0]+=2;
const bn=lab.normalize(rows,'batch'),ln=lab.normalize(rows,'layer'),bm=lab.normalize(modified,'batch'),lm2=lab.normalize(modified,'layer');
near(bn.means[0],4);near(bn.variances[0],6);assert.notEqual(bn.values[1][0],bm.values[1][0]);assert.deepEqual(ln.values[1],lm2.values[1]);assert.deepEqual(bn.values.map(r=>r[1]),bm.values.map(r=>r[1]));
assert.notEqual(Number(q('#norm-other').textContent),0);q('#norm-mode').value='layer';change('#norm-mode');assert.equal(q('#norm-other').textContent,'0');
assert.throws(()=>lab.normalize(rows,'unknown'),RangeError);
const keys=[[1,0],[0,1],[1,1]],masked=lab.attention(keys,keys,[1,2,4]),perturbed=lab.attention(keys,keys,[1,2,100]);
for(const row of masked.weights)near(row.reduce((s,w)=>s+w,0),1);near(masked.weights[0][2],0);near(masked.outputs[0],perturbed.outputs[0]);near(masked.outputs[1],perturbed.outputs[1]);assert.notEqual(masked.outputs[2],perturbed.outputs[2]);
assert.notEqual(lab.attention(keys,keys,[1,2,4],false).outputs[0],lab.attention(keys,keys,[1,2,100],false).outputs[0]);
assert.throws(()=>lab.attention(keys,keys,[1,2,4],true,0),RangeError);
assert.equal(q('#attn-out').textContent,'1');q('#attn-future').value='6';input('#attn-future');assert.equal(q('#attn-change').textContent,'0');q('#attn-causal').checked=false;change('#attn-causal');assert.ok(Number(q('#attn-change').textContent)>0);
q('#attn-temperature').value='.3';input('#attn-temperature');near(Number(q('#attn-sum').textContent),1);
const first=lab.diffusion([2],[-1],1);near(first.abar,.97);near(first.values[0],Math.sqrt(.97)*2-Math.sqrt(.03));
const last=lab.diffusion([2],[-1],30);assert.ok(last.abar<first.abar);near(last.signal**2+last.sigma**2,1);
assert.deepEqual(lab.diffusion([2],[-1],30),last);assert.throws(()=>lab.diffusion([1],[0],0),RangeError);
q('#noise-step').value='30';input('#noise-step');near(Number(q('#noise-abar').textContent),last.abar,1e-4);
for(const plot of document.querySelectorAll('.dl-plot'))assert.ok(!/NaN|Infinity/.test(plot.innerHTML));

function navigate(id){location.hash='#'+id;window.dispatchEvent(new Event('hashchange'));}
let equations=0,examples=0;
for(const lesson of window.COURSE.lessons){
  navigate(lesson.id);assert.equal(q('.lesson-header h1').textContent,lesson.title);assert.ok(q('.lesson-breadcrumb').textContent.startsWith('深度學習'));
  assert.equal(document.querySelectorAll('.chapter-link[aria-current="page"]').length,1);
  for(const link of document.querySelectorAll('.toc-links a'))assert.ok(document.getElementById(link.getAttribute('href').split('/')[1]));
  if(lesson.example){examples++;assert.equal(q('.example-download a').getAttribute('href'),'examples.zip');}
  const {document:doc}=parseHTML(`<!doctype html><html><body>${lesson.html}</body></html>`);
  for(const element of doc.querySelectorAll('.math-source,.math-block')){
    const text=element.textContent.trim(),display=element.classList.contains('math-block'),tex=display?text.slice(2,-2).trim():text.slice(1,-1);
    assert.ok(katex.renderToString(tex,{displayMode:display,throwOnError:true}).includes('class="katex'));equations++;
  }
}
assert.equal(examples,42);assert.ok(equations>=62);
navigate('01-representations');q('#complete-lesson').click();assert.equal(q('#progress-count').textContent,'1 / 72');
q('#lesson-notes').value='先檢查梯度與資料邊界。';input('#lesson-notes');navigate('02-environment');navigate('01-representations');assert.equal(q('#lesson-notes').value,'先檢查梯度與資料邊界。');
assert.equal(storage.get('learning-notes:machine-learning:v1'),savedML);assert.equal(JSON.parse(storage.get('learning-notes:deep-learning:v1')).completed.length,1);
q('#open-search').click();for(const term of ['Jacobian','Diffusion','蒸餾','2.15.0']){q('#search-input').value=term;input('#search-input');assert.ok(document.querySelectorAll('.search-result').length>0);}
q('#close-search').click();q('#menu-toggle').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'true');q('#sidebar-shade').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'false');
navigate('overview');assert.equal(document.querySelectorAll('.dl-lab').length,6);assert.equal(q('#xor-steps').textContent,'0');assert.equal(q('#attn-out').textContent,'1');assert.equal(q('#noise-step').value,'1');
export const report={syntax:'PASS',chapters:72,modules:12,examples,equations,labs:'activation derivatives, trained XOR, kernel arithmetic, norm axes, causal attention, fixed-noise diffusion: PASS',reader:'TOC, downloads, search, notes, progress, menu, remount: PASS',isolation:'machine learning notes preserved',limit:'DOM emulation; no real-browser layout review'};
