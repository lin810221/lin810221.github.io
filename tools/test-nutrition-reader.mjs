/* DOM acceptance for nutrition arithmetic and the shared reader. No visual claims. */
import {readFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
import {parseHTML,Event,HTMLElement} from '../.qa/vendor/linkedom.mjs';
import {parse} from '../.qa/vendor/acorn.mjs';
import katex from '../.qa/vendor/katex.mjs';
const root=new URL('../',import.meta.url),read=file=>readFile(new URL(file,root),'utf8');
for(const file of ['assets/reader.js','nutrition/assets/overview.js','nutrition/assets/course-data.js'])parse(await read(file),{ecmaVersion:'latest'});
const {document:home}=parseHTML(await read('index.html'));assert.equal(home.querySelectorAll('.subject-feature').length,13);assert.equal(home.querySelectorAll('a[href="nutrition/index.html"]').length,1);
const {window,document}=parseHTML(await read('nutrition/index.html')),q=s=>document.querySelector(s),location={hash:''};
const previous=JSON.stringify({completed:['01-economic-questions'],notes:{'01-economic-questions':'preserve economics'}}),storage=new Map([['learning-notes:economics:v1',previous]]);
HTMLElement.prototype.focus=function(){};HTMLElement.prototype.scrollIntoView=function(){};window.scrollTo=()=>{};window.print=()=>{};
/* linkedom does not model the live checked IDL property. Browser semantics shim. */
if(typeof document.createElement('input').checked!=='boolean')Object.defineProperty(window.HTMLInputElement.prototype,'checked',{get(){return this.hasAttribute('checked');},set(v){this.toggleAttribute('checked',Boolean(v));},configurable:true});
q('#search-dialog').showModal=function(){this.open=true;};q('#search-dialog').close=function(){this.open=false;};
Object.assign(globalThis,{window,document,location,requestAnimationFrame:fn=>fn(),localStorage:{getItem:key=>storage.get(key)??null,setItem:(key,value)=>storage.set(key,value)}});
await import(new URL('nutrition/assets/course-data.js',root).href);await import(new URL('nutrition/assets/overview.js',root).href);await import(new URL('assets/reader.js',root).href);
assert.equal(document.querySelectorAll('.chapter-link').length,96);assert.equal(document.querySelectorAll('.module-row').length,16);assert.equal(document.querySelectorAll('.nutrition-lab').length,12);
const ids=[...document.querySelectorAll('[id]')].map(x=>x.id);assert.equal(ids.length,new Set(ids).size);
for(const control of document.querySelectorAll('.nutrition-lab input,.nutrition-lab select'))assert.ok(document.querySelector(`label[for="${control.id}"]`));
for(const plot of document.querySelectorAll('.nutrition-chart')){assert.equal(plot.getAttribute('role'),'img');assert.ok(q('#'+plot.getAttribute('aria-labelledby')));assert.ok(!plot.innerHTML.includes('NaN'));}
assert.equal(document.querySelectorAll('.nutrition-lab [data-status="error"]').length,0);assert.ok(q('#quick-start').textContent.includes('課內進階'));
const lab=window.NutritionLab,input=id=>q(id).dispatchEvent(new Event('input')),near=(a,b)=>assert.ok(Math.abs(a-b)<1e-8,`${a} != ${b}`);
function choose(id,value){const options=[...q(id).querySelectorAll('option')];assert.ok(options.some(o=>o.value===value));for(const option of options)option.selected=option.value===value;q(id).dispatchEvent(new Event('change'));}
near(lab.mass(1,'mg','ug'),1000);assert.throws(()=>lab.mass(1,'IU','g'));assert.throws(()=>lab.mass(NaN));
near(lab.energy().kcal,380);near(lab.energy().parts.reduce((a,b)=>a+b),380);assert.deepEqual(lab.energy(0,0,0,0).percent,[null,null,null,null]);
q('#energy-c').value='';input('#energy-c');assert.equal(q('#lab-out-2').dataset.status,'error');assert.equal(q('#lab-plot-2').innerHTML,'');q('#energy-c').value='50';input('#energy-c');assert.equal(q('#lab-out-2').dataset.status,'ok');
near(lab.serving().amount,270);near(lab.serving().wholePackage,450);assert.throws(()=>lab.serving(10,0));near(lab.salt(800),2);
assert.equal(lab.sugars(20,'unknown').free,null);assert.equal(lab.sugars(20,'whole_fruit').free,0);assert.equal(lab.sugars(20,'juice').free,20);choose('#sugar-recipe','juice');assert.ok(q('#lab-out-5').textContent.includes('20.000 g'));choose('#sugar-recipe','unknown');assert.ok(q('#lab-out-5').textContent.includes('未知'));
near(lab.cooking().per100,3.6);assert.throws(()=>lab.cooking(100,0));assert.throws(()=>lab.cooking(100,100,10,1.1));
assert.equal(lab.nrv(400).percent,20);assert.equal(lab.nrv(10,'sugars').percent,null);choose('#nrv-kind','sugars');assert.ok(q('#lab-out-7').textContent.includes('未設定'));
near(lab.vitamin(1000,'d_iu').amount,25);near(lab.vitamin(1200,'a_food_beta').amount,100);near(lab.vitamin(240,'folic_meal').amount,400);assert.throws(()=>lab.vitamin(100,'5-MTHF'));
assert.equal(lab.meal(200,'milk').total,445);assert.equal(lab.meal(200,'drink').total,null);assert.equal(lab.meal(200,'drink').knownSubtotal,225);assert.equal(lab.meal(0,'drink').total,225);choose('#meal-drink','drink');assert.ok(q('#lab-out-9').textContent.includes('未知'));assert.ok(q('#lab-plot-9 title').textContent.includes('未知'));
near(lab.bounds().low,203.2);near(lab.bounds().high,304.8);assert.throws(()=>lab.bounds(200,100));
const risk=lab.risk();near(risk.rr,.8);near(risk.arr,.02);near(risk.nnt,50);assert.equal(lab.risk(1,100,0,100).rr,null);assert.equal(lab.risk(1,100,1,100).nnt,null);assert.equal(lab.risk(20,100,10,100).direction,'harm');assert.throws(()=>lab.risk(2.5,100,5,100));q('#risk-et').value='1001';input('#risk-et');assert.equal(q('#lab-out-11').dataset.status,'error');assert.equal(q('#lab-plot-11').innerHTML,'');q('#risk-et').value='80';input('#risk-et');
for(let i=0;i<6;i++)q('#group-'+i).checked=true;input('#group-0');assert.ok(q('#lab-out-12').textContent.includes('6／6'));assert.ok(q('#lab-out-12').textContent.includes('不證明'));
for(const fn of [()=>lab.energy(-1),()=>lab.salt(Infinity),()=>lab.nrv(-1),()=>lab.vitamin(-1),()=>lab.groups([true])])assert.throws(fn);
function navigate(id){location.hash='#'+id;window.dispatchEvent(new Event('hashchange'));}
let equations=0,examples=0;
for(const lesson of window.COURSE.lessons){
  navigate(lesson.id);assert.equal(q('.lesson-header h1').textContent,lesson.title);assert.equal(document.querySelectorAll('.chapter-link[aria-current="page"]').length,1);assert.ok(document.querySelectorAll('.toc-links a').length>=4);
  for(const el of document.querySelectorAll('.math-block,.math-source')){const tex=el.textContent.trim().replace(/^\$\$\s*|\s*\$\$$/g,'').replace(/^\$|\$$/g,'');katex.renderToString(tex,{displayMode:el.classList.contains('math-block'),throwOnError:true,strict:'error'});equations++;}
  if(lesson.example){examples++;assert.equal(q('.example-download a').getAttribute('href'),'examples.zip');}
}
assert.equal(examples,48);assert.ok(equations>=10);assert.deepEqual(window.COURSE.groups.map(g=>window.COURSE.lessons.filter(l=>l.group===g.id).length),Array(16).fill(6));
navigate('01-nutrition-and-food');q('#complete-lesson').click();q('#lesson-notes').value='未知不是零；NRV不是個人需要。';input('#lesson-notes');navigate('07-digestive-map');assert.ok(q('.lesson-kicker').textContent.includes('CHAPTER 02'));assert.ok(q('.lesson-kicker').textContent.includes('UNIT 01 OF 6'));navigate('01-nutrition-and-food');assert.equal(q('#lesson-notes').value,'未知不是零；NRV不是個人需要。');assert.equal(q('#progress-count').textContent,'1 / 96');assert.equal(storage.get('learning-notes:economics:v1'),previous);
q('#open-search').click();for(const term of ['自由糖','DFE','RAE','過敏原','食物基質','Python']){q('#search-input').value=term;input('#search-input');assert.ok(document.querySelectorAll('.search-result').length>0,term);}q('#close-search').click();q('#menu-toggle').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'true');q('#sidebar-shade').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'false');
navigate('overview');assert.equal(document.querySelectorAll('.nutrition-lab').length,12);assert.equal(document.querySelectorAll('.nutrition-lab [data-status="error"]').length,0);assert.ok(q('#lab-out-9').textContent.includes('445.000'));assert.ok(q('#lab-out-12').textContent.includes('3／6'));
const css=await read('nutrition/assets/course.css'),styleDoc=parseHTML('<html><head><style>'+css+'</style></head></html>').document;assert.ok(styleDoc.querySelector('style').sheet.cssRules.length>20);
export const report={syntax:'PASS',units:96,chapters:16,examples,equations,labs:'12 labs numeric, missing, units, zero, invalid, scope and remount: PASS',reader:'TOC, ZIP, search, notes, progress, chapter reset, menu: PASS',isolation:'economics preserved',limit:'DOM emulation; real-browser layout not verified'};
