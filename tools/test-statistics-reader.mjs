/* Numerical and reader DOM QA. Does not replace actual browser layout review. */
import {readFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
import {parseHTML,Event,HTMLElement} from '../.qa/vendor/linkedom.mjs';
import {parse} from '../.qa/vendor/acorn.mjs';
import katex from '../.qa/vendor/katex.mjs';
const root=new URL('../',import.meta.url),read=file=>readFile(new URL(file,root),'utf8');
for(const file of ['assets/reader.js','applied-statistics/assets/overview.js','applied-statistics/assets/course-data.js'])parse(await read(file),{ecmaVersion:'latest'});
const {document:home}=parseHTML(await read('index.html'));assert.ok(home.querySelectorAll('.subject-feature').length>=8);assert.equal(home.querySelectorAll('a[href="applied-statistics/index.html"]').length,1);
const {window,document}=parseHTML(await read('applied-statistics/index.html'));
const previous=JSON.stringify({completed:['01-representations'],notes:{'01-representations':'preserve this note'}}),storage=new Map([['learning-notes:deep-learning:v1',previous]]),location={hash:''},q=s=>document.querySelector(s);
HTMLElement.prototype.focus=function(){};HTMLElement.prototype.scrollIntoView=function(){};window.scrollTo=()=>{};window.print=()=>{};
q('#search-dialog').showModal=function(){this.open=true;};q('#search-dialog').close=function(){this.open=false;};
Object.assign(globalThis,{window,document,location,requestAnimationFrame:fn=>fn(),localStorage:{getItem:k=>storage.get(k)??null,setItem:(k,v)=>storage.set(k,v)}});
await import(new URL('applied-statistics/assets/course-data.js',root).href);await import(new URL('applied-statistics/assets/overview.js',root).href);await import(new URL('assets/reader.js',root).href);
assert.equal(q('.topbar-subject').textContent,'應用統計');assert.equal(document.querySelectorAll('.chapter-link').length,70);assert.equal(document.querySelectorAll('.module-row').length,11);assert.equal(document.querySelectorAll('.as-lab').length,8);
const ids=[...document.querySelectorAll('[id]')].map(x=>x.id);assert.equal(ids.length,new Set(ids).size);
for(const input of document.querySelectorAll('.as-lab input,.as-lab select'))assert.ok(document.querySelector(`label[for="${input.id}"]`));
for(const svg of document.querySelectorAll('.as-plot')){assert.equal(svg.getAttribute('role'),'img');assert.ok(svg.querySelector('title'));}
const lab=window.AppliedStatisticsLab,near=(a,b,t=1e-10)=>assert.ok(Math.abs(a-b)<=t,`${a} versus ${b}`),input=id=>q(id).dispatchEvent(new Event('input')),change=id=>q(id).dispatchEvent(new Event('change'));
for(const [id,value] of [['ci-level','.95'],['power-alpha','.05']])Object.defineProperty(q('#'+id),'value',{value,writable:true,configurable:true});
const d=lab.describe([2,4,6]);near(d.mean,4);near(d.median,4);near(d.sd,2);near(lab.quantile([1,2,3,4],.25),1.75);
const h=lab.histogram([0,2,4,6],3,0,6);assert.deepEqual(h.counts,[1,1,2]);near(h.density.reduce((s,x)=>s+x*h.width,0),1);assert.throws(()=>lab.histogram([0,7],3,0,6),RangeError);
const before=Number(q('#desc-mean').textContent);q('#desc-last').value='40';input('#desc-last');assert.ok(Number(q('#desc-mean').textContent)>before);assert.equal(q('#desc-median').textContent,'5');q('#desc-bins').value='10';input('#desc-bins');
near(lab.binomial(3,.5)[1],.375);near(lab.binomial(10,.3).reduce((a,b)=>a+b,0),1);assert.deepEqual(lab.binomial(3,0),[1,0,0,0]);assert.deepEqual(lab.binomial(3,1),[0,0,0,1]);assert.throws(()=>lab.binomial(2,1.1),RangeError);
q('#bin-n').value='1';input('#bin-n');assert.equal(q('#bin-k').max,'1');assert.equal(q('#bin-k').value,'1');q('#bin-k').value='0';input('#bin-k');assert.equal(q('#bin-tail').textContent,'1');
const s1=lab.sampling(1),s80=lab.sampling(80);assert.ok(s80.summary.sd<s1.summary.sd/5);near(s80.summary.mean,1,.03);assert.deepEqual(lab.sampling(80),s80);
q('#sampling-n').value='100';input('#sampling-n');assert.equal(q('#sampling-theory').textContent,'0.1');
// Reference constants from standard normal distribution, independent of the UI approximation.
for(const [z,p] of [[-3,.0013498980316300946],[-1,.15865525393145707],[0,.5],[1,.8413447460685429],[3,.9986501019683699]])near(lab.cdf(z),p,1e-7);
near(lab.inverseNormal(.975),1.959963984540054,2e-6);assert.throws(()=>lab.inverseNormal(1),RangeError);
const c=lab.coverage(25,.95),cLarge=lab.coverage(100,.95);near(cLarge.half,c.half/2);assert.equal(cLarge.covered,c.covered);assert.ok(c.covered>100&&c.covered<120);assert.ok(lab.coverage(25,.99).covered>=c.covered);
const oldWidth=Number(q('#ci-width').textContent);q('#ci-n').value='100';input('#ci-n');near(Number(q('#ci-width').textContent),oldWidth/2,1e-4);q('#ci-level').value='.99';change('#ci-level');assert.ok(Number(q('#ci-width').textContent)>oldWidth/2);q('#ci-redraw').click();
near(lab.power(30,0).power,.05,2e-7);near(lab.power(30,.5).power,lab.power(30,-.5).power,1e-12);assert.ok(lab.power(100,.5).power>lab.power(20,.5).power);
q('#power-delta').value='0';input('#power-delta');assert.equal(q('#power-value').textContent,'5.0%');q('#power-alpha').value='.01';change('#power-alpha');assert.equal(q('#power-value').textContent,'1.0%');
const a=lab.anova([[1,2,3],[3,4,5],[5,6,7]]);near(a.between,24);near(a.within,6);near(a.total,30);near(a.F,12);near(a.eta,.8);
assert.equal(q('#anova-f').textContent,'12');q('#anova-spread').value='2';input('#anova-spread');assert.equal(q('#anova-f').textContent,'3');q('#anova-middle').value='6';input('#anova-middle');assert.ok(Number(q('#anova-between').textContent)>24);
const r=lab.ols([-2,-1,0,1,2],[-2,-3,3,1,6]);near(r.intercept,1);near(r.slope,2);near(r.r2,20/27);near(r.residuals.reduce((a,b)=>a+b,0),0);assert.throws(()=>lab.ols([1,1,1],[1,2,3]),RangeError);
const slope=Number(q('#reg-slope').textContent);q('#reg-last').value='24';input('#reg-last');assert.ok(Number(q('#reg-slope').textContent)>slope);
near(lab.alpha([[1,1],[2,2],[4,4],[5,5]]).value,1);assert.equal(lab.alpha([[1,1],[1,1],[1,1]]).value,null);
const uncorrected=Number(q('#alpha-value').textContent);q('#alpha-reverse').checked=true;change('#alpha-reverse');assert.ok(Number(q('#alpha-value').textContent)>uncorrected);q('#alpha-last').value='1';input('#alpha-last');assert.equal(q('#alpha-last-value').textContent,'1');
for(const svg of document.querySelectorAll('.as-plot'))assert.ok(!/NaN|Infinity/.test(svg.innerHTML));

function navigate(id){location.hash='#'+id;window.dispatchEvent(new Event('hashchange'));}
let examples=0,equations=0;
for(const lesson of window.COURSE.lessons){
  navigate(lesson.id);assert.equal(q('.lesson-header h1').textContent,lesson.title);assert.ok(q('.lesson-breadcrumb').textContent.startsWith('應用統計'));assert.equal(document.querySelectorAll('.chapter-link[aria-current="page"]').length,1);
  for(const a of document.querySelectorAll('.toc-links a'))assert.ok(document.getElementById(a.getAttribute('href').split('/')[1]));
  if(lesson.example){examples++;assert.equal(q('.example-download a').getAttribute('href'),'examples.zip');}
  const {document:doc}=parseHTML(`<!doctype html><html><body>${lesson.html}</body></html>`);
  for(const element of doc.querySelectorAll('.math-source,.math-block')){const text=element.textContent.trim(),display=element.classList.contains('math-block'),tex=display?text.slice(2,-2).trim():text.slice(1,-1);assert.ok(katex.renderToString(tex,{displayMode:display,throwOnError:true}).includes('class="katex'));equations++;}
}
assert.equal(examples,40);assert.ok(equations>=25);
const codes=window.COURSE.lessons.map(l=>l.title.split('　')[0]);for(const [chapter,sections] of [[1,4],[2,3],[3,3],[4,5],[5,8],[6,4],[7,8],[8,5],[9,3],[10,11]])for(let section=1;section<=sections;section++)assert.ok(codes.includes(`${chapter}-${section}`));
navigate('01-statistics-definition');q('#complete-lesson').click();assert.equal(q('#progress-count').textContent,'1 / 70');q('#lesson-notes').value='先問觀察單位與分母。';input('#lesson-notes');navigate('02-statistics-branches');navigate('01-statistics-definition');assert.equal(q('#lesson-notes').value,'先問觀察單位與分母。');
assert.equal(storage.get('learning-notes:deep-learning:v1'),previous);assert.equal(JSON.parse(storage.get('learning-notes:applied-statistics:v1')).completed.length,1);
q('#open-search').click();for(const text of ['Welch','信賴區間','因素分析','10-11']){q('#search-input').value=text;input('#search-input');assert.ok(document.querySelectorAll('.search-result').length>0);}q('#close-search').click();q('#menu-toggle').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'true');q('#sidebar-shade').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'false');
navigate('overview');assert.equal(document.querySelectorAll('.as-lab').length,8);assert.equal(q('#desc-mean').textContent,'5.3333');assert.equal(q('#power-value').textContent,'78.2%');
export const report={syntax:'PASS',units:70,chapters:10,groupsIncludingAppendices:11,examples,equations,labs:'histogram, binomial, repeated sampling, CI coverage, normal power, ANOVA, OLS, alpha: PASS',reader:'original section codes, TOC, ZIP, search, notes, progress, menu, remount: PASS',isolation:'deep learning notes preserved',limit:'DOM emulation; no real-browser layout verification'};
