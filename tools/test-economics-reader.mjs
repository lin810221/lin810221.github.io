/* Model/reader DOM acceptance. Real-browser layout is a separate surface. */
import {readFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
import {parseHTML,Event,HTMLElement} from '../.qa/vendor/linkedom.mjs';
import {parse} from '../.qa/vendor/acorn.mjs';
import katex from '../.qa/vendor/katex.mjs';
const root=new URL('../',import.meta.url),read=file=>readFile(new URL(file,root),'utf8');
for(const file of ['assets/reader.js','economics/assets/overview.js','economics/assets/course-data.js'])parse(await read(file),{ecmaVersion:'latest'});
const {document:home}=parseHTML(await read('index.html'));assert.equal(home.querySelectorAll('.subject-feature').length,13);assert.equal(home.querySelectorAll('a[href="economics/index.html"]').length,1);
const {window,document}=parseHTML(await read('economics/index.html')),q=s=>document.querySelector(s),location={hash:''};
const previous=JSON.stringify({completed:['01-scope-and-overlap'],notes:{'01-scope-and-overlap':'preserve search'}}),storage=new Map([['learning-notes:search:v1',previous]]);
HTMLElement.prototype.focus=function(){};HTMLElement.prototype.scrollIntoView=function(){};window.scrollTo=()=>{};window.print=()=>{};
q('#search-dialog').showModal=function(){this.open=true;};q('#search-dialog').close=function(){this.open=false;};
Object.assign(globalThis,{window,document,location,requestAnimationFrame:fn=>fn(),localStorage:{getItem:key=>storage.get(key)??null,setItem:(key,value)=>storage.set(key,value)}});
await import(new URL('economics/assets/course-data.js',root).href);await import(new URL('economics/assets/overview.js',root).href);await import(new URL('assets/reader.js',root).href);
assert.equal(document.querySelectorAll('.chapter-link').length,84);assert.equal(document.querySelectorAll('.module-row').length,14);assert.equal(document.querySelectorAll('.econ-lab').length,10);
const ids=[...document.querySelectorAll('[id]')].map(x=>x.id);assert.equal(ids.length,new Set(ids).size);
for(const control of document.querySelectorAll('.econ-lab input,.econ-lab select'))assert.ok(document.querySelector(`label[for="${control.id}"]`));
for(const plot of document.querySelectorAll('.econ-chart')){assert.equal(plot.getAttribute('role'),'img');assert.ok(q('#'+plot.getAttribute('aria-labelledby')));assert.ok(!plot.innerHTML.includes('NaN'));}
assert.ok(q('#quick-start').textContent.includes('課內進階'));assert.equal(document.querySelectorAll('.econ-lab [data-status="error"]').length,0);
const lab=window.EconomicsLab,input=id=>q(id).dispatchEvent(new Event('input')),near=(a,b)=>assert.ok(Math.abs(a-b)<1e-8,`${a} != ${b}`);
function choose(id,value){const option=[...q(id).querySelectorAll('option')].find(item=>item.value===value);assert.ok(option);option.selected=true;q(id).dispatchEvent(new Event('change'));}
near(lab.frontier(60).y,64);assert.throws(()=>lab.frontier(101));q('#ppf-x').value='100';input('#ppf-x');assert.ok(q('#ppf-out').textContent.includes('無有限斜率'));
const tax=lab.market(20);assert.equal(tax.q,30);assert.equal(tax.pb,70);assert.equal(tax.ps,50);assert.equal(tax.revenue,600);assert.equal(tax.dwl,100);near(tax.cs+tax.psurplus+tax.revenue+tax.dwl,1600);
assert.equal(lab.market(80).pb,null);assert.equal(lab.market(100).q,0);near(lab.market(10,2,1).buyerShare,2/3);q('#tax-value').value='80';input('#tax-value');assert.ok(q('#tax-out').textContent.includes('無成交價'));q('#tax-value').value='';input('#tax-value');assert.equal(q('#tax-out').dataset.status,'error');q('#tax-value').value='20';input('#tax-value');assert.equal(q('#tax-out').dataset.status,'ok');
near(lab.elasticity(60,70).value,-13/7);near(lab.elasticity(70,60).value,-13/7);q('#elastic-p2').value='60';input('#elastic-p2');assert.equal(q('#elastic-out').dataset.status,'error');q('#elastic-p2').value='70';input('#elastic-p2');
const con=lab.consumer();assert.equal(con.x,30);assert.equal(con.y,20);assert.equal(con.expenditure,120);assert.equal(lab.consumer(0).utility,0);q('#consumer-income').value='0';input('#consumer-income');assert.ok(!q('#consumer-chart').innerHTML.includes('NaN'));q('#consumer-income').value='120';input('#consumer-income');
const mon=lab.monopoly();assert.equal(mon.q,40);assert.equal(mon.p,60);assert.equal(mon.qc,80);assert.equal(mon.profit,1600);assert.equal(mon.dwl,800);
assert.deepEqual(lab.game('pd').pure,[[1,1]]);assert.equal(lab.game('pennies').pure.length,0);near(lab.game('pennies').mixed.p,.5);assert.equal(lab.game('ties').pure.length,4);near(lab.game('coordination').mixed.q,.4);choose('#game-kind','ties');assert.equal(document.querySelectorAll('#game-matrix .equilibrium').length,4);choose('#game-kind','pennies');assert.ok(q('#game-out').textContent.includes('0.500'));
const ext=lab.externality(1);near(ext.qo,80/3);near(ext.tax,80/3);near(ext.loss,800/3);assert.equal(lab.externality(0).loss,0);
const price=lab.prices(2025);assert.equal(price.nominal,3085);assert.equal(price.real,2930);near(price.cpi,2960/2800*100);near(price.deflator,3085/2930*100);choose('#price-year','2024');assert.ok(q('#price-out').textContent.includes('CPI=100.000'));
const steady=lab.solow(.2,1).steady;near(lab.solow(.2,steady).rows[60].k,steady);assert.ok(lab.solow(.2,.1).rows[60].k>.1);
const policy=lab.policy(0,2,1,2);near(policy.y,-4/3);near(policy.inflation,10/3);near(policy.real,7/3);near(policy.nominal,13/3);q('#policy-u').value='0';input('#policy-u');assert.ok(q('#policy-out').textContent.includes('通膨=2.000%'));
function navigate(id){location.hash='#'+id;window.dispatchEvent(new Event('hashchange'));}
let equations=0,examples=0;
for(const lesson of window.COURSE.lessons){
  navigate(lesson.id);assert.equal(q('.lesson-header h1').textContent,lesson.title);assert.equal(document.querySelectorAll('.chapter-link[aria-current="page"]').length,1);assert.ok(document.querySelectorAll('.toc-links a').length>=4);
  for(const el of document.querySelectorAll('.math-block,.math-source')){const tex=el.textContent.trim().replace(/^\$\$\s*|\s*\$\$$/g,'').replace(/^\$|\$$/g,'');katex.renderToString(tex,{displayMode:el.classList.contains('math-block'),throwOnError:true,strict:'error'});equations++;}
  if(lesson.example){examples++;assert.equal(q('.example-download a').getAttribute('href'),'examples.zip');}
}
assert.equal(examples,42);assert.ok(equations>=21);assert.deepEqual(window.COURSE.groups.map(g=>window.COURSE.lessons.filter(l=>l.group===g.id).length),Array(14).fill(6));
navigate('01-economic-questions');q('#complete-lesson').click();q('#lesson-notes').value='模型算術不等於因果證據。';input('#lesson-notes');navigate('07-supply-demand-equilibrium');assert.ok(q('.lesson-kicker').textContent.includes('CHAPTER 02'));assert.ok(q('.lesson-kicker').textContent.includes('UNIT 01 OF 6'));navigate('01-economic-questions');assert.equal(q('#lesson-notes').value,'模型算術不等於因果證據。');assert.equal(q('#progress-count').textContent,'1 / 84');assert.equal(storage.get('learning-notes:search:v1'),previous);
q('#open-search').click();for(const term of ['Solow','GDP','機會成本','Nash','資料版本','BPM7']){q('#search-input').value=term;input('#search-input');assert.ok(document.querySelectorAll('.search-result').length>0);}q('#close-search').click();q('#menu-toggle').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'true');q('#sidebar-shade').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'false');
navigate('overview');assert.equal(document.querySelectorAll('.econ-lab').length,10);assert.equal(q('#tax-out').dataset.status,'ok');assert.ok(q('#policy-out').textContent.includes('3.333'));assert.equal(document.querySelectorAll('#game-matrix .equilibrium').length,1);
const css=await read('economics/assets/course.css'),styleDoc=parseHTML('<html><head><style>'+css+'</style></head></html>').document;assert.ok(styleDoc.querySelector('style').sheet.cssRules.length>20);
export const report={syntax:'PASS',units:84,chapters:14,examples,equations,labs:'PPF, tax, elasticity, consumer, monopoly, games, externality, indexes, Solow, IS-MP-PC: PASS',reader:'TOC, ZIP, search, notes, progress, chapter reset, menu, remount: PASS',isolation:'search course preserved',limit:'DOM emulation; real-browser layout not verified'};
