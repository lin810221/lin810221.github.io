/* DOM acceptance: arithmetic semantics and reader behavior; no visual claims. */
import {readFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
import {parseHTML,Event,HTMLElement} from '../.qa/vendor/linkedom.mjs';
import {parse} from '../.qa/vendor/acorn.mjs';
import katex from '../.qa/vendor/katex.mjs';
const root=new URL('../',import.meta.url),read=file=>readFile(new URL(file,root),'utf8');
for(const file of ['assets/reader.js','exercise-science/assets/overview.js','exercise-science/assets/course-data.js'])parse(await read(file),{ecmaVersion:'latest'});
const {document:home}=parseHTML(await read('index.html'));assert.equal(home.querySelectorAll('.subject-feature').length,14);assert.equal(home.querySelectorAll('a[href="exercise-science/index.html"]').length,1);
const {window,document}=parseHTML(await read('exercise-science/index.html')),q=s=>document.querySelector(s),location={hash:''};
const previous=JSON.stringify({completed:['01-nutrition-and-food'],notes:{'01-nutrition-and-food':'preserve nutrition'}}),storage=new Map([['learning-notes:nutrition:v1',previous]]);
HTMLElement.prototype.focus=function(){};HTMLElement.prototype.scrollIntoView=function(){};window.scrollTo=()=>{};window.print=()=>{};
q('#search-dialog').showModal=function(){this.open=true;};q('#search-dialog').close=function(){this.open=false;};
Object.assign(globalThis,{window,document,location,requestAnimationFrame:fn=>fn(),localStorage:{getItem:key=>storage.get(key)??null,setItem:(key,value)=>storage.set(key,value)}});
await import(new URL('exercise-science/assets/course-data.js',root).href);await import(new URL('exercise-science/assets/overview.js',root).href);await import(new URL('assets/reader.js',root).href);
assert.equal(document.querySelectorAll('.chapter-link').length,96);assert.equal(document.querySelectorAll('.module-row').length,16);assert.equal(document.querySelectorAll('.exercise-lab').length,12);
const ids=[...document.querySelectorAll('[id]')].map(x=>x.id);assert.equal(ids.length,new Set(ids).size);
for(const control of document.querySelectorAll('.exercise-lab input,.exercise-lab select'))assert.ok(q(`label[for="${control.id}"]`));
for(const plot of document.querySelectorAll('.exercise-chart')){assert.equal(plot.getAttribute('role'),'img');assert.ok(q('#'+plot.getAttribute('aria-labelledby')));assert.ok(!plot.innerHTML.includes('NaN'));}
assert.equal(document.querySelectorAll('.exercise-lab [data-status="error"]').length,0);assert.ok(q('#quick-start').textContent.includes('課內進階'));
const lab=window.ExerciseLab,input=id=>q(id).dispatchEvent(new Event('input')),near=(a,b)=>assert.ok(Math.abs(a-b)<1e-8,`${a} != ${b}`);
function choose(id,value){const options=[...q(id).querySelectorAll('option')];assert.ok(options.some(o=>o.value===value));for(const option of options)option.selected=option.value===value;q(id).dispatchEvent(new Event('change'));}
near(lab.torque(100,.3,30),15);near(lab.torque(100,.3,180),0);assert.throws(()=>lab.torque(100,.3,181));q('#torque-force').value='';input('#torque-force');assert.equal(q('#exercise-out-1').dataset.status,'error');assert.equal(q('#exercise-plot-1').innerHTML,'');q('#torque-force').value='100';input('#torque-force');
near(lab.work(20,.5,2).joules,98.0665);near(lab.work(20,.5,2).watts,49.03325);assert.equal(lab.work(20,0,2).watts,0);assert.throws(()=>lab.work(20,1,0));
assert.equal(lab.volume().total,960);assert.equal(lab.volume(3,8,40,false).total,null);assert.equal(lab.volume(0,8,40,false).total,0);assert.throws(()=>lab.volume(2.5));choose('#volume-known','no');assert.ok(q('#exercise-out-3').textContent.includes('未知'));
assert.equal(lab.oneRM().epley,70);assert.equal(lab.oneRM().brzycki,67.5);assert.equal(lab.oneRM(60,1).epley,60);assert.throws(()=>lab.oneRM(60,11));assert.throws(()=>lab.oneRM(60,1.5));
assert.equal(lab.rir(2),8);assert.throws(()=>lab.rir(5));assert.throws(()=>lab.rir(-1));
const hr=lab.heart(60,180,.6);assert.equal(hr.hrr,132);assert.equal(hr.maxPercent,108);assert.throws(()=>lab.heart(180,60));q('#hr-max').value='60';input('#hr-max');assert.equal(q('#exercise-out-6').dataset.status,'error');assert.equal(q('#exercise-plot-6').innerHTML,'');q('#hr-max').value='180';input('#hr-max');
assert.equal(lab.pace(5,30).seconds,360);assert.equal(lab.pace(5,30).kmh,10);assert.throws(()=>lab.pace(0,30));near(lab.pace(10,52).seconds*lab.pace(10,52).kmh,3600);
assert.equal(lab.intervals().total,1710);assert.equal(lab.intervals(6,60,90,600,300,true).total,1800);assert.equal(lab.intervals(1,60,90,0,0).recovery,0);assert.throws(()=>lab.intervals(0));choose('#interval-final','yes');assert.ok(q('#exercise-out-8').textContent.includes('1800s'));
assert.equal(lab.session(45,5),225);assert.equal(lab.session(30,7.5),225);assert.throws(()=>lab.session(30,11));
assert.equal(lab.weekly().total,1100);assert.equal(lab.weekly().ratio,1.1);assert.equal(lab.weekly(true).total,null);assert.equal(lab.weekly(true).subtotal,800);assert.equal(lab.weekly(true).ratio,null);choose('#week-missing','missing');assert.ok(q('#exercise-out-10').textContent.includes('未知'));assert.ok(q('#exercise-plot-10 title').textContent.includes('未知'));assert.ok(q('#exercise-out-10').textContent.includes('沒有安全判決'));
assert.equal(lab.equivalent(90,30),150);assert.equal(lab.equivalent(0,0),0);
const response=lab.response();assert.equal(response.length,28);assert.equal(response[0].value,-50);assert.equal(lab.response(0).at(-1).value,0);assert.throws(()=>lab.response(100,0,5));q('#toy-load').value='0';input('#toy-load');assert.ok(!q('#exercise-plot-12').innerHTML.includes('NaN'));assert.ok(q('#exercise-out-12').textContent.includes('不能解讀'));
for(const fn of [()=>lab.torque(NaN),()=>lab.work(Infinity),()=>lab.volume(-1),()=>lab.rir(true),()=>lab.heart(60,180,1.1),()=>lab.session(-1),()=>lab.equivalent(-1)])assert.throws(fn);
function navigate(id){location.hash='#'+id;window.dispatchEvent(new Event('hashchange'));}
let equations=0,examples=0;
for(const lesson of window.COURSE.lessons){
  navigate(lesson.id);assert.equal(q('.lesson-header h1').textContent,lesson.title);assert.equal(document.querySelectorAll('.chapter-link[aria-current="page"]').length,1);assert.ok(document.querySelectorAll('.toc-links a').length>=4);
  for(const el of document.querySelectorAll('.math-block,.math-source')){const tex=el.textContent.trim().replace(/^\$\$\s*|\s*\$\$$/g,'').replace(/^\$|\$$/g,'');katex.renderToString(tex,{displayMode:el.classList.contains('math-block'),throwOnError:true,strict:'error'});equations++;}
  if(lesson.example){examples++;assert.equal(q('.example-download a').getAttribute('href'),'examples.zip');}
}
assert.equal(examples,48);assert.ok(equations>=10);assert.deepEqual(window.COURSE.groups.map(g=>window.COURSE.lessons.filter(l=>l.group===g.id).length),Array(16).fill(6));
navigate('01-exercise-science-map');q('#complete-lesson').click();q('#lesson-notes').value='單位、任務與未知分開；ACWR不是安全區。';input('#lesson-notes');navigate('07-movement-map');assert.ok(q('.lesson-kicker').textContent.includes('CHAPTER 02'));assert.ok(q('.lesson-kicker').textContent.includes('UNIT 01 OF 6'));navigate('01-exercise-science-map');assert.equal(q('#lesson-notes').value,'單位、任務與未知分開；ACWR不是安全區。');assert.equal(q('#progress-count').textContent,'1 / 96');assert.equal(storage.get('learning-notes:nutrition:v1'),previous);
q('#open-search').click();for(const term of ['RIR','FITT','ACWR','力矩','肌肥大','並行訓練']){q('#search-input').value=term;input('#search-input');assert.ok(document.querySelectorAll('.search-result').length>0,term);}q('#close-search').click();q('#menu-toggle').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'true');q('#sidebar-shade').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'false');
navigate('overview');assert.equal(document.querySelectorAll('.exercise-lab').length,12);assert.equal(document.querySelectorAll('.exercise-lab [data-status="error"]').length,0);assert.ok(q('#exercise-out-3').textContent.includes('960.000'));assert.ok(q('#exercise-out-10').textContent.includes('1.100'));assert.ok(q('#exercise-out-8').textContent.includes('1710s'));
const css=await read('exercise-science/assets/course.css'),styleDoc=parseHTML('<html><head><style>'+css+'</style></head></html>').document;assert.ok(styleDoc.querySelector('style').sheet.cssRules.length>20);
export const report={syntax:'PASS',units:96,chapters:16,examples,equations,labs:'12 labs: arithmetic, domains, missing, scale, zero, error clearing and remount PASS',reader:'TOC, ZIP, search, notes, progress, chapter reset, menu PASS',isolation:'nutrition preserved',limit:'DOM emulation; real-browser layout not verified'};
