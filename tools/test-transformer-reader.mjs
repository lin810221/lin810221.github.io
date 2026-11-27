/* Original numeric/reader DOM QA; a real browser is required for layout review. */
import {readFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
import {parseHTML,Event,HTMLElement} from '../.qa/vendor/linkedom.mjs';
import {parse} from '../.qa/vendor/acorn.mjs';
import katex from '../.qa/vendor/katex.mjs';
const root=new URL('../',import.meta.url),read=file=>readFile(new URL(file,root),'utf8');
for(const file of ['assets/reader.js','transformer/assets/overview.js','transformer/assets/course-data.js'])parse(await read(file),{ecmaVersion:'latest'});
const {document:home}=parseHTML(await read('index.html'));
assert.equal(home.querySelectorAll('.subject-feature').length,Object.keys(JSON.parse(await readFile(new URL('tools/library.json',root),'utf8')).courses).length);
assert.equal(home.querySelectorAll('a[href="transformer/index.html"]').length,1);
const {window,document}=parseHTML(await read('transformer/index.html'));
const old=JSON.stringify({completed:['001-task-map'],notes:{'001-task-map':'影像課筆記保留'}});
const storage=new Map([['learning-notes:image-recognition:v1',old]]),location={hash:''},q=s=>document.querySelector(s);
HTMLElement.prototype.focus=function(){};HTMLElement.prototype.scrollIntoView=function(){};
window.scrollTo=()=>{};window.print=()=>{};
q('#search-dialog').showModal=function(){this.open=true;};q('#search-dialog').close=function(){this.open=false;};
Object.assign(globalThis,{window,document,location,requestAnimationFrame:fn=>fn(),localStorage:{getItem:k=>storage.get(k)??null,setItem:(k,v)=>storage.set(k,v)}});
await import(new URL('transformer/assets/course-data.js',root).href);
await import(new URL('transformer/assets/overview.js',root).href);
await import(new URL('assets/reader.js',root).href);
const navigate=id=>{location.hash='#'+id;window.dispatchEvent(new Event('hashchange'));};
const input=id=>q('#'+id).dispatchEvent(new Event('input'));
const select=(id,value)=>{const element=q('#'+id);for(const option of element.querySelectorAll('option'))option.selected=false;element.querySelector(`option[value="${value}"]`).selected=true;element.dispatchEvent(new Event('change'));};
const near=(a,b,tol=1e-8)=>assert.ok(Math.abs(a-b)<tol,`${a} vs ${b}`);
assert.equal(q('.topbar-subject').textContent,'Transformer 與 LLM 原理');
assert.equal(document.querySelectorAll('.chapter-link').length,96);
assert.equal(document.querySelectorAll('.module-row').length,16);
assert.equal(document.querySelectorAll('.tf-lab').length,10);
assert.equal(document.querySelectorAll('.tf-atlas img').length,32);
let ids=[...document.querySelectorAll('[id]')].map(e=>e.id);assert.equal(ids.length,new Set(ids).size);
for(const e of document.querySelectorAll('.tf-lab input,.tf-lab select'))assert.ok(q(`label[for="${e.id}"]`));
for(const svg of document.querySelectorAll('.tf-plot')){assert.equal(svg.getAttribute('role'),'img');assert.ok(svg.querySelector('title'));}
const lab=window.TransformerLab;
for(const text of ['banana bandana','學習學習🙂','e\u0301','<eos>']){const a=lab.bpe(text,8),b=lab.bpe(text,8);assert.equal(a.text,text);assert.deepEqual(a,b);assert.ok(a.ids.length<=a.bytes.length);}
select('tf-text','學習學習🙂');assert.ok(q('#tf-bytes-output').textContent.includes('學習學習🙂'));q('#tf-merges').value='0';input('tf-merges');assert.equal(q('#tf-bpe-count').textContent,'16');
near(lab.chain([.5,.25,.8]).joint,.1);near(lab.chain([.5,.25,.8]).nll,-Math.log(.1)/3);assert.throws(()=>lab.chain([0]),RangeError);assert.equal(q('#tf-joint').textContent,'0.1');q('#tf-p1').value='1';input('tf-p1');assert.equal(q('#tf-joint').textContent,'0.2');
const att=lab.attention([1,0],[[1,0],[0,1],[1,1]],[[2,0],[0,4],[6,2]]);near(att.weights.reduce((a,b)=>a+b,0),1);near(att.output[0],2*att.weights[0]+6*att.weights[2]);
q('#tf-hide-key').checked=true;q('#tf-hide-key').dispatchEvent(new Event('change'));assert.equal(q('#tf-attn-value').textContent,'['+lab.attention([1,0],[[1,0],[0,1],[1,1]],[[2,0],[0,4],[6,2]],[true,true,false]).output.map(x=>Number(x.toFixed(5))).join(', ')+']');
assert.throws(()=>lab.attention([1],[[1]],[[1]],[false]),RangeError);
assert.deepEqual(lab.allowed(3,2),[[true,true,true,true,false],[true,true,true,true,true]]);assert.equal(q('#tf-mask-first').textContent,'11110');q('#tf-past').value='0';input('tf-past');assert.equal(q('#tf-mask-first').textContent,'10');q('#tf-new').value='1';input('tf-new');assert.equal(q('#tf-mask-first').textContent,'1');
const dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),qv=[1,2,3,4],kv=[2,1,1,3];near(dot(lab.rotate(qv,3),lab.rotate(kv,7)),dot(lab.rotate(qv,13),lab.rotate(kv,17)));near(Math.hypot(...lab.rotate(qv,5)),Math.hypot(...qv));
const priorDot=q('#tf-rope-dot').textContent;q('#tf-rope-shift').value='11';input('tf-rope-shift');assert.equal(q('#tf-rope-dot').textContent,priorDot);
const oldNorm=q('#tf-layer-values').textContent;q('#tf-offset').value='4';input('tf-offset');assert.equal(q('#tf-layer-values').textContent,oldNorm);assert.notDeepEqual(lab.norm([1,2,3,4],'rms'),lab.norm([5,6,7,8],'rms'));
const filtered=lab.sampleDistribution([Math.log(.6),Math.log(.25),Math.log(.1),Math.log(.05)],1,4,.8);assert.deepEqual(filtered.ids,[0,1]);near(filtered.probabilities[0],.6/.85);assert.deepEqual(lab.sampleDistribution([0,0,0],1,2,1).ids,[0,1]);
q('#tf-topk').value='1';input('tf-topk');assert.equal(q('#tf-sampling-ids').textContent,'0');assert.throws(()=>lab.sampleDistribution([1,2],0),RangeError);
assert.equal(lab.kvBytes(2,32,4096,8,128,2),2**30);assert.equal(q('#tf-kv-gib').textContent,'1');select('tf-kv-heads','32');assert.equal(q('#tf-kv-gib').textContent,'4');select('tf-kv-heads','1');assert.equal(q('#tf-kv-gib').textContent,'0.125');
near(lab.aggregate([2,8],[1,3]).nll,2.6);assert.equal(q('#tf-weighted-nll').textContent,'2.6');q('#tf-count-a').value='8';input('tf-count-a');assert.equal(q('#tf-weighted-nll').textContent,'2');
const preferred=lab.dpo(2,1,.2),reversed=lab.dpo(0,1,.2);assert.ok(preferred.loss<reversed.loss);near(lab.dpo(1,1,.2).loss,Math.log(2));q('#tf-policy-gap').value='1';input('tf-policy-gap');near(Number(q('#tf-dpo-loss').textContent),Math.log(2),1e-5);assert.throws(()=>lab.dpo(1,0,0),RangeError);
for(const plot of document.querySelectorAll('.tf-plot'))assert.ok(!/NaN|Infinity/.test(plot.innerHTML));
const course=window.COURSE,allIds=new Set(course.lessons.map(l=>l.id));let equations=0,examples=0;const used=new Set();
for(const lesson of course.lessons){
  navigate(lesson.id);assert.equal(q('.lesson-header h1').textContent,lesson.title);
  assert.equal(document.querySelectorAll('.chapter-link[aria-current="page"]').length,1);
  assert.ok(q('.tf-task').textContent.includes(lesson.title));
  const figure=q('.tf-figure img');assert.ok(figure.getAttribute('alt').length>=20);used.add(figure.getAttribute('src'));
  for(const link of document.querySelectorAll('.toc-links a'))assert.ok(document.getElementById(link.getAttribute('href').split('/')[1]));
  for(const a of document.querySelectorAll('.lesson-content a[href^="#"]')){const id=a.getAttribute('href').slice(1).split('/')[0];assert.ok(allIds.has(id)||document.getElementById(id),`${lesson.id}: broken ${id}`);}
  if(lesson.example){examples++;assert.equal(q('.example-download a').getAttribute('href'),'examples.zip');}
  const {document:doc}=parseHTML(`<!doctype html><html><body>${lesson.html}</body></html>`);
  const pageIds=[...doc.querySelectorAll('[id]')].map(x=>x.id);assert.equal(pageIds.length,new Set(pageIds).size);
  for(const e of doc.querySelectorAll('.math-source,.math-block')){
    const text=e.textContent.trim(),display=e.classList.contains('math-block'),tex=e.getAttribute('data-tex') ?? (display?text.slice(2,-2).trim():text.slice(1,-1));
    assert.ok(katex.renderToString(tex,{displayMode:display,throwOnError:true}).includes('class="katex'));equations++;
  }
}
assert.equal(used.size,32);assert.equal(examples,41);assert.ok(equations>=100);
navigate('001-lm-task');q('#complete-lesson').click();assert.equal(q('#progress-count').textContent,'1 / 96');
q('#lesson-notes').value='SDPA True允許；target只shift一次。';q('#lesson-notes').dispatchEvent(new Event('input'));navigate('007-unicode');navigate('001-lm-task');assert.equal(q('#lesson-notes').value,'SDPA True允許；target只shift一次。');assert.equal(storage.get('learning-notes:image-recognition:v1'),old);
q('#open-search').click();for(const term of ['RoPE','GQA','DPO','5.24.0','-100']){q('#search-input').value=term;q('#search-input').dispatchEvent(new Event('input'));assert.ok(document.querySelectorAll('.search-result').length>0);}
q('#close-search').click();q('#menu-toggle').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'true');q('#sidebar-shade').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'false');
navigate('overview');assert.equal(document.querySelectorAll('.tf-lab').length,10);assert.equal(q('#tf-mask-first').textContent,'11110');assert.equal(q('#tf-kv-gib').textContent,'1');assert.equal(q('#tf-weighted-nll').textContent,'2.6');
export const report={slug:course.slug,syntax:'PASS',modules:16,units:96,figures:used.size,examples,equations,labs:'10 deterministic numerical laboratories PASS',reader:'TOC/search/notes/progress/downloads/menu/remount PASS',isolation:'existing image course notes preserved',limit:'DOM simulation; no real-browser layout review'};
