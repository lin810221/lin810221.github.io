/* DOM acceptance for original ergonomics teaching. No browser-layout claims. */
import {readFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
import {parseHTML,Event,HTMLElement} from '../.qa/vendor/linkedom.mjs';
import {parse} from '../.qa/vendor/acorn.mjs';
import katex from '../.qa/vendor/katex.mjs';
const root=new URL('../',import.meta.url),read=file=>readFile(new URL(file,root),'utf8');
for(const file of ['assets/reader.js','ergonomics/assets/overview.js','ergonomics/assets/course-data.js'])parse(await read(file),{ecmaVersion:'latest'});
const {document:home}=parseHTML(await read('index.html'));assert.equal(home.querySelectorAll('.subject-feature').length,16);assert.equal(home.querySelectorAll('a[href="ergonomics/index.html"]').length,1);
const {window,document}=parseHTML(await read('ergonomics/index.html')),q=s=>document.querySelector(s),location={hash:''};
assert.ok(q('meta[name="description"]').getAttribute('content').includes('肌肉骨骼'));
const previous=JSON.stringify({completed:['01-mental-health-map'],notes:{'01-mental-health-map':'preserve mental'}}),storage=new Map([['learning-notes:mental-health:v1',previous]]);
HTMLElement.prototype.focus=function(){};HTMLElement.prototype.scrollIntoView=function(){};window.scrollTo=()=>{};window.print=()=>{};
q('#search-dialog').showModal=function(){this.open=true;};q('#search-dialog').close=function(){this.open=false;};
Object.assign(globalThis,{window,document,location,requestAnimationFrame:fn=>fn(),localStorage:{getItem:key=>storage.get(key)??null,setItem:(key,value)=>storage.set(key,value)}});
await import(new URL('ergonomics/assets/course-data.js',root).href);await import(new URL('ergonomics/assets/overview.js',root).href);await import(new URL('assets/reader.js',root).href);
assert.equal(document.querySelectorAll('.chapter-link').length,96);assert.equal(document.querySelectorAll('.module-row').length,16);assert.equal(document.querySelectorAll('.ergo-lab').length,12);
const ids=[...document.querySelectorAll('[id]')].map(x=>x.id);assert.equal(ids.length,new Set(ids).size);
for(const c of document.querySelectorAll('.ergo-lab input,.ergo-lab select'))assert.ok(q(`label[for="${c.id}"]`));
for(const svg of document.querySelectorAll('.ergo-chart')){assert.equal(svg.getAttribute('role'),'img');assert.ok(q('#'+svg.getAttribute('aria-labelledby')));assert.ok(!svg.innerHTML.includes('NaN'));}
const lessonIds=new Set(window.COURSE.lessons.map(l=>l.id));for(const a of document.querySelectorAll('main a[href^="#"]')){const href=a.getAttribute('href').slice(1);assert.ok(href.startsWith('overview')||lessonIds.has(href),href);}
assert.equal(document.querySelectorAll('.ergo-lab [data-status="error"]').length,0);assert.ok(q('#quick-start').textContent.includes('課內進階'));
const lab=window.ErgoLab,input=id=>q(id).dispatchEvent(new Event('input')),near=(a,b)=>assert.ok(Math.abs(a-b)<1e-8,`${a} != ${b}`);
function choose(id,value){const options=[...q(id).querySelectorAll('option')];assert.ok(options.some(o=>o.value===value));for(const o of options)o.selected=false;options.find(o=>o.value===value).selected=true;assert.equal(q(id).value,value);q(id).dispatchEvent(new Event('change'));}
near(lab.moment(),30);near(lab.moment(100,.6),60);near(lab.moment(100,.3,0),0);near(lab.moment(100,.3,30),15);assert.throws(()=>lab.moment(100,.3,181));
q('#moment-radius').value='';input('#moment-radius');assert.equal(q('#ergo-out-1').dataset.status,'error');assert.equal(q('#ergo-plot-1').innerHTML,'');q('#moment-radius').value='.6';input('#moment-radius');assert.ok(q('#ergo-out-1').textContent.includes('60.000'));
near(lab.pressure(100,10),100);near(lab.pressure(100,20),50);near(lab.pressure(0,10),0);assert.throws(()=>lab.pressure(100,0));q('#pressure-area').value='20';input('#pressure-area');assert.ok(q('#ergo-out-2').textContent.includes('50.000'));
assert.equal(lab.fit().known,10);assert.equal(lab.fit().matched,3);assert.equal(lab.fit().unknown,2);near(lab.fit().fraction,.3);assert.equal(lab.fit(150,1).matched,0);const altered=lab.fit();altered.rows[0].reach=999;assert.notEqual(lab.fit().rows[0].reach,999);
near(lab.geometry(60,-15).distance,Math.hypot(60,15));assert.ok(lab.geometry().angle<0);near(lab.geometry(60,0).angle,0);assert.throws(()=>lab.geometry(0,0));q('#view-vertical').value='0';input('#view-vertical');assert.ok(q('#ergo-out-4').textContent.includes('0.000°'));assert.ok(q('#ergo-plot-4 title').textContent.includes('不是建議角度'));
near(lab.angular(),2*Math.atan(4/1200)*180/Math.PI);assert.ok(lab.angular(4,120)<lab.angular(4,60));assert.throws(()=>lab.angular(0));
assert.deepEqual(lab.schedule(),{work:200,change:40,total:240});assert.equal(lab.schedule(50,0,1).total,50);assert.throws(()=>lab.schedule(50,10,1.5));q('#schedule-change').value='0';input('#schedule-change');assert.ok(q('#ergo-out-6').textContent.includes('200.000'));
near(lab.repetition().rate,9);near(lab.repetition().fraction,.7);assert.throws(()=>lab.repetition(90,10,11));assert.throws(()=>lab.repetition(2.5));q('#rep-active').value='11';input('#rep-active');assert.equal(q('#ergo-out-7').dataset.status,'error');q('#rep-active').value='7';input('#rep-active');
const r=lab.rnle();near(r.rwl,23*.91*.94);near(r.li,12/r.rwl);near(lab.rnle(12,50).rwl,r.rwl/2);near(lab.rnle(12,0).rwl,r.rwl);near(lab.rnle(12,25,75,0).factors.DM,1);near(lab.rnle(12,25,0,25).factors.VM,.775);
assert.equal(lab.rnle(12,25,75,50,0,null,1).rwl,null);assert.equal(lab.rnle(12,25,75,50,0,.94,null).rwl,null);assert.equal(lab.rnle(12,25,75,50,0,.94,1,false).li,null);assert.equal(lab.rnle(12,25,75,50,0,0,1).li,null);assert.equal(lab.rnle(0).li,0);
for(const args of [[12,64],[12,25,176],[12,25,75,176],[12,25,75,50,136]])assert.throws(()=>lab.rnle(...args));
choose('#rnle-context','unknown');assert.ok(q('#ergo-out-8').textContent.includes('RWL 未知'));assert.ok(q('#ergo-plot-8 title').textContent.includes('FM 未知'));choose('#rnle-context','teaching');q('#rnle-h').value='64';input('#rnle-h');assert.equal(q('#ergo-out-8').dataset.status,'error');assert.equal(q('#ergo-plot-8').innerHTML,'');q('#rnle-h').value='25';input('#rnle-h');
near(lab.hav().a8,Math.sqrt(5));near(lab.hav(4,120,0,0).a8,2);assert.equal(lab.hav(4,120,2,120,false).a8,null);assert.equal(lab.hav(null,120).a8,null);assert.equal(lab.hav(0,0,0,0).a8,0);assert.throws(()=>lab.hav(4,1440,2,1));
choose('#hav-complete','missing');assert.ok(q('#ergo-out-9').textContent.includes('完整日A(8) 未知'));choose('#hav-complete','complete');assert.ok(q('#ergo-out-9').textContent.includes('2.236'));
near(lab.work().joules,500);near(lab.work().watts,50);near(lab.work(100,5,10,90).joules,0);near(lab.work(0).joules,0);assert.throws(()=>lab.work(100,5,0));assert.throws(()=>lab.work(100,5,10,91));
assert.ok(lab.control('eliminate').includes('取消'));assert.throws(()=>lab.control('fake'));choose('#control-direction','ppe');assert.ok(q('#ergo-out-11').textContent.includes('不取代來源改善'));
assert.equal(lab.observations().observed,11);assert.equal(lab.observations().minutes,110);assert.equal(lab.observations().subtotal,990);near(lab.observations().available,9);assert.equal(lab.observations().complete,null);assert.equal(lab.observations('complete').complete,1080);assert.equal(lab.observations('zero').complete,0);
choose('#obs-mode','zero');assert.ok(q('#ergo-out-12').textContent.includes('完整總量 0.000次'));assert.ok(!q('#ergo-plot-12').innerHTML.includes('NaN'));
for(const fn of [()=>lab.moment(true),()=>lab.pressure(Infinity),()=>lab.fit(NaN),()=>lab.angular(-1),()=>lab.schedule(1,1,0),()=>lab.rnle(12,25,75,50,0,1.1),()=>lab.hav(1,-1),()=>lab.hav(1,1,1,1,'yes'),()=>lab.observations('fake')])assert.throws(fn);
// Every numeric lab clears stale output plots after an invalid input and recovers.
for(const [i,id] of [[2,'pressure-area'],[3,'fit-reach'],[4,'view-horizontal'],[5,'angle-height'],[6,'schedule-work'],[9,'hav-a'],[10,'work-time']]){const old=q('#'+id).value;q('#'+id).value='';input('#'+id);assert.equal(q('#ergo-out-'+i).dataset.status,'error');assert.equal(q('#ergo-plot-'+i).innerHTML,'');q('#'+id).value=old;input('#'+id);assert.equal(q('#ergo-out-'+i).dataset.status,'ok');}
function navigate(id){location.hash='#'+id;window.dispatchEvent(new Event('hashchange'));}
let equations=0,examples=0;
for(const lesson of window.COURSE.lessons){navigate(lesson.id);assert.equal(q('.lesson-header h1').textContent,lesson.title);assert.equal(document.querySelectorAll('.chapter-link[aria-current="page"]').length,1);assert.ok(document.querySelectorAll('.toc-links a').length>=4);
  for(const el of document.querySelectorAll('.math-block,.math-source')){const tex=el.textContent.trim().replace(/^\$\$\s*|\s*\$\$$/g,'').replace(/^\$|\$$/g,'');katex.renderToString(tex,{displayMode:el.classList.contains('math-block'),throwOnError:true,strict:'error'});equations++;}
  if(lesson.example){examples++;assert.equal(q('.example-download a').getAttribute('href'),'examples.zip');}
}
assert.equal(examples,48);assert.ok(equations>=8);assert.deepEqual(window.COURSE.groups.map(g=>window.COURSE.lessons.filter(l=>l.group===g.id).length),Array(16).fill(6));
navigate('01-ergonomics-map');q('#complete-lesson').click();q('#lesson-notes').value='先確認任務、單位與未知。';input('#lesson-notes');navigate('07-bone-and-remodeling');assert.ok(q('.lesson-kicker').textContent.includes('CHAPTER 02'));assert.ok(q('.lesson-kicker').textContent.includes('UNIT 01 OF 6'));navigate('01-ergonomics-map');assert.equal(q('#lesson-notes').value,'先確認任務、單位與未知。');assert.equal(q('#progress-count').textContent,'1 / 96');assert.equal(storage.get('learning-notes:mental-health:v1'),previous);
q('#open-search').click();for(const term of ['力矩','肌腱','RNLE','ART','振動','人因']){q('#search-input').value=term;input('#search-input');assert.ok(document.querySelectorAll('.search-result').length>0,term);}q('#close-search').click();q('#menu-toggle').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'true');q('#sidebar-shade').click();assert.equal(q('#menu-toggle').getAttribute('aria-expanded'),'false');
navigate('overview');assert.equal(document.querySelectorAll('.ergo-lab').length,12);assert.equal(document.querySelectorAll('.ergo-lab [data-status="error"]').length,0);assert.ok(q('#ergo-out-3').textContent.includes('30.000%'));assert.ok(q('#ergo-out-8').textContent.includes('19.674'));assert.ok(q('#ergo-out-12').textContent.includes('完整總量 未知'));
const css=await read('ergonomics/assets/course.css'),styleDoc=parseHTML('<html><head><style>'+css+'</style></head></html>').document;assert.ok(styleDoc.querySelector('style').sheet.cssRules.length>20);
export const report={syntax:'PASS',units:96,chapters:16,examples,equations,labs:'12 labs: physical units, geometry, RNLE bounds, missingness, HAV, zero, errors and remount PASS',reader:'TOC, ZIP, search, notes, progress, chapter reset and menu PASS',isolation:'mental-health preserved',limit:'DOM emulation; real-browser layout not verified'};
