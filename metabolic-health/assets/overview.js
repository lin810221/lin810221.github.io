/* Original offline teaching arithmetic; all examples and model inputs fictional. */
(() => {
  'use strict';
  const nn=(...v)=>{if(v.some(x=>typeof x!=='number'||!Number.isFinite(x)||x<0))throw new RangeError('請輸入非負有限數值');};
  const pos=(...v)=>{nn(...v);if(v.some(x=>x===0))throw new RangeError('分母與長度需大於0');};
  const integer=(...v)=>{nn(...v);if(v.some(x=>!Number.isSafeInteger(x)))throw new RangeError('人數、年齡與期限需為整數');};
  const probability=(...v)=>{nn(...v);if(v.some(x=>x>1))throw new RangeError('機率需在0至1');};
  function toy(input=10,clearance=.2){nn(input);probability(clearance);let state=0;return Array.from({length:25},(_,i)=>{state=state+(i<5?input:0)-clearance*state;return {step:i+1,state};});}
  function body(kg=70,cm=170,waist=85){pos(kg,cm,waist);return {bmi:kg/(cm/100)**2,waistHeight:waist/cm};}
  function units(value=100,analyte='glucose',direction='toSI'){
    nn(value);const factors={glucose:18,cholesterol:38.67,triglycerides:88.57,creatinine:1/88.4};
    if(!Object.hasOwn(factors,analyte)||!['toSI','fromSI'].includes(direction))throw new RangeError('不支援此分析物或方向；Lp(a)無通用固定換算');
    const si=analyte==='creatinine'?'µmol/L':'mmol/L';return {value:direction==='toSI'?value/factors[analyte]:value*factors[analyte],source:direction==='toSI'?'mg/dL':si,target:direction==='toSI'?si:'mg/dL'};
  }
  function a1c(value=6.5,source='NGSP'){nn(value);if(!['NGSP','IFCC'].includes(source))throw new RangeError('需指定NGSP或IFCC');const result=source==='NGSP'?(value-2.152)/.09148:value*.09148+2.152;if(result<0)throw new RangeError('此輸入換算超出非負示範範圍');return result;}
  function bp(missing=true,excludeFirst=false){
    if(typeof missing!=='boolean'||typeof excludeFirst!=='boolean')throw new RangeError('需明示缺漏及首日規則');
    const days=Array.from({length:7},(_,i)=>({day:i+1,readings:[0,1,2,3].map(j=>missing&&i===6&&j===3?null:122+i+1+j%2)}));
    const selected=excludeFirst?days.slice(1):days,values=selected.flatMap(x=>x.readings).filter(x=>x!==null),available=values.reduce((a,b)=>a+b,0)/values.length;
    return {expected:selected.length*4,valid:values.length,available,complete:values.length===selected.length*4?available:null,days:selected.map(d=>({day:d.day,n:d.readings.filter(x=>x!==null).length,mean:d.readings.filter(x=>x!==null).reduce((a,b)=>a+b,0)/d.readings.filter(x=>x!==null).length}))};
  }
  function nonhdl(tc=200,hdl=50){nn(tc,hdl);if(hdl>tc)throw new RangeError('HDL不可大於TC，請核對資料');return tc-hdl;}
  function fib4(age=50,ast=30,alt=25,platelets=200,stable=true){integer(age);if(age<18)throw new RangeError('本公式展示限成人，不作兒少判讀');nn(ast);pos(alt,platelets);if(typeof stable!=='boolean')throw new RangeError('需明示情境');return stable?age*ast/(platelets*Math.sqrt(alt)):null;}
  function acr(albumin=30,creatinine=1){nn(albumin);pos(creatinine);return albumin/creatinine;}
  function risk(e0=100,n0=1000,e1=70,n1=1000){integer(e0,n0,e1,n1);pos(n0,n1);if(e0>n0||e1>n1)throw new RangeError('事件人數不可超過各組總人數');const p0=e0/n0,p1=e1/n1,arr=p0-p1;return {p0,p1,rr:p0?p1/p0:null,rrr:p0?1-p1/p0:null,arr,number:arr?1/Math.abs(arr):null,direction:arr>0?'降低':arr<0?'增加':'無差異'};}
  function screening(n=10000,prevalence=.01,sensitivity=.9,specificity=.95){integer(n);pos(n);probability(prevalence,sensitivity,specificity);const tp=n*prevalence*sensitivity,fn=n*prevalence*(1-sensitivity),fp=n*(1-prevalence)*(1-specificity),tn=n*(1-prevalence)*specificity;return {tp,fn,fp,tn,ppv:tp+fp?tp/(tp+fp):null,npv:tn+fn?tn/(tn+fn):null};}
  function ageScope(age=45,horizon=10){integer(age,horizon);if(![10,30].includes(horizon))throw new RangeError('期限僅10或30年');return age>=30&&age<=(horizon===10?79:59);}
  function assumed(baseline=.05,rr=.8){probability(baseline);nn(rr);const after=baseline*rr;if(after>1)throw new RangeError('假設結果超過100%，請修正輸入');return {before:baseline,after,difference:baseline-after};}
  window.MetabolicLab=Object.freeze({toy,body,units,a1c,bp,nonhdl,fib4,acr,risk,screening,ageScope,assumed});
  const esc=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const field=(id,label,value,min=0,max=10000,step='1')=>`<label for="${id}"><span>${label}</span><input id="${id}" type="number" value="${value}" min="${min}" max="${max}" step="${step}"></label>`;
  const select=(id,label,options)=>`<label for="${id}"><span>${label}</span><select id="${id}">${options.map(([v,text],i)=>`<option value="${v}"${i===0?' selected':''}>${text}</option>`).join('')}</select></label>`;
  const lab=(n,title,controls,caption,plot=false)=>`<section class="metabolic-lab" id="metabolic-lab-${n}"><header><span class="mono">LAB ${String(n).padStart(2,'0')}</span><h3>${title}</h3></header><div class="metabolic-lab-body"><div class="metabolic-controls">${controls}</div>${plot?`<div class="metabolic-plot" id="metabolic-plot-${n}"></div>`:''}<output id="metabolic-out-${n}" aria-live="polite"></output><p class="lab-caption">${caption}</p></div></section>`;
  function bars(id,labels,values,unit){const max=Math.max(1,...values.filter(v=>v!==null));return `<svg class="metabolic-chart" viewBox="0 0 680 ${55+labels.length*40}" role="img" aria-labelledby="${id}-title"><title id="${id}-title">${esc(unit)}：${labels.map((s,i)=>esc(s)+' '+(values[i]===null?'未知':values[i].toFixed(3))).join('；')}</title>${labels.map((s,i)=>`<text x="10" y="${36+i*40}">${esc(s)}</text><rect x="170" y="${19+i*40}" width="${values[i]===null?0:values[i]/max*270}" height="23" rx="3" fill="${i%2?'#a4c7e9':'#b5e99b'}" opacity=".75"/><text x="460" y="${36+i*40}">${values[i]===null?'未知':values[i].toFixed(3)} ${esc(unit)}</text>`).join('')}</svg>`;}
  function curve(rows){const hi=Math.max(1,...rows.map(r=>r.state));return `<svg class="metabolic-chart" viewBox="0 0 620 250" role="img" aria-labelledby="balance-title"><title id="balance-title">未校準輸入清除模型，25步，最後${rows.at(-1).state.toFixed(3)}任意單位；不是血糖預測</title><path d="M45 25V210H580" fill="none" stroke="currentColor"/><polyline points="${rows.map((r,i)=>`${45+i/24*530},${210-r.state/hi*170}`).join(' ')}" fill="none" stroke="#b5e99b" stroke-width="3"/><text x="45" y="240">第1步 → 第25步；縱軸0至${hi.toFixed(1)}，任意模型單位</text></svg>`;}
  window.renderCourseOverview=({course,saved,escapeHTML:e,main,toc,footer})=>{
    const start=saved.last||course.lessons[0].id;
    main.innerHTML=`<section class="course-hero" id="intro"><div class="eyebrow">THE METABOLIC HEALTH GUIDE <span>／ 從數字，回到身體的連結</span></div><h1>Connect &amp; prevent<span class="hero-period">.</span></h1><h2 class="hero-subtitle">理解代謝如何運作，<br>讓預防有脈絡、有依據。</h2><p class="hero-description">血糖、血壓、血脂與體重，不是彼此無關的紅字。從器官與調節開始，把心臟、肝臟、腎臟、生活與環境連起來，學會閱讀量測、風險與證據。</p><div class="hero-meta"><span><b>16</b> 章主線</span><span><b>96</b> 個閱讀單元</span><span><b>48</b> 份 Python 範例</span><span><b>12</b> 個互動實驗</span></div><div class="hero-actions"><a class="primary-button" href="#${start}">${saved.last?'繼續學習':'從代謝健康的第一個問題開始'} <span aria-hidden="true">↗</span></a><a class="text-link" href="#overview/experiments">先玩單位與篩檢實驗 ↓</a></div></section>
    <section id="scope" class="metabolic-scope"><div><span class="mono">UNDERSTAND · 01–04</span><h3>代謝與量測</h3><p>調節、器官分工、體位與血糖，建立從零開始的基礎。</p></div><div><span class="mono">CONNECT · 05–10</span><h3>風險與器官</h3><p>糖尿病預防、血壓血脂、心血管、MASLD與腎臟。</p></div><div><span class="mono">PREVENT · 11–16</span><h3>生活與證據</h3><p>飲食、活動、睡眠、環境、篩檢與可重跑報告。</p></div></section>
    <section id="quick-start"><div class="section-header"><h2>先讀全貌，再選一條問題路線</h2><span>MEASURE → CONNECT → EVALUATE → PREVENT</span></div><div class="metabolic-route"><p><a href="#01-metabolic-health-map">代謝地圖</a> → <a href="#19-glucose-units">血糖單位</a> → <a href="#31-home-measurement">居家血壓</a> → <a href="#37-particles-and-nonhdl">血脂</a> → <a href="#57-urine-acr">尿ACR</a> → <a href="#85-screening-bayes">篩檢預測值</a> → <a href="#95-capstone">整合專題</a>。</p><p><strong>課內進階都在本課完成。</strong>完整學習依16章順序；先想看健檢可讀第4、6、7、10、14章，再回補調節與證據。程式為可選實作，純閱讀不用安裝Python。營養與運動必要概念在此說明，另回連既有課程深入學習。</p></div></section>
    <section id="roadmap"><div class="section-header"><h2>完整學習路線</h2><span>16 CHAPTERS · 96 UNITS</span></div><div class="module-list">${course.groups.map(g=>{const units=course.lessons.filter(l=>l.group===g.id);return `<a class="module-row" href="#${units[0].id}"><span class="module-num">${g.number}</span><div><div class="module-name">${e(g.title)}</div><div class="module-description">${e(g.description)}</div></div><span class="module-count">${units.length} UNITS ↗</span></a>`;}).join('')}</div></section>
    <section id="experiments"><div class="section-header"><h2>把容易混淆的數字，親手拆開</h2><span>12 INTERACTIVE LABS</span></div><p class="hero-description">用虛構數字觀察算術、假設與缺漏。工具不輸出個人診斷、治療目標、用藥或PREVENT風險；每項結果旁都保留單位與用途。</p>
    ${lab(1,'輸入與清除：任意回饋模型',field('balance-input','前5步各自的任意輸入',10,0,100,.5)+field('balance-clearance','每步清除比例',.2,0,1,.05),'state下一步＝state＋當步input−clearance×state；只前5步輸入，共25步，未校準人體，不代表血糖、胰島素或熱量。',true)}
    ${lab(2,'BMI與腰高比：算術不是完整評估',field('body-kg','虛構體重 kg',70,.1,300,.1)+field('body-cm','身高 cm',170,50,250,.1)+field('body-waist','腰圍 cm',85,1,250,.1),'只顯示比值，不訂理想體重，不自動套成人分類給兒少、孕期或特殊族群。')}
    ${lab(3,'檢驗單位：先選分析物',select('unit-analyte','分析物',[['glucose','血糖'],['cholesterol','膽固醇'],['triglycerides','三酸甘油酯'],['creatinine','肌酸酐']])+select('unit-direction','方向',[['toSI','mg/dL → SI'],['fromSI','SI → mg/dL']])+field('unit-value','輸入數值（依方向的來源單位）',100,0,10000,.01),'血糖18.0、膽固醇38.67、TG88.57、肌酸酐88.4各有方向與單位；Lp(a)沒有通用固定mg/dL↔nmol/L係數。')}
    ${lab(4,'HbA1c：NGSP與IFCC',select('a1c-source','輸入制度',[['NGSP','NGSP %'],['IFCC','IFCC mmol/mol']])+field('a1c-value','HbA1c數值（依所選制度）',6.5,0,200,.01),'NGSP%=0.09148×IFCC+2.152。mmol/mol不是血糖mmol/L，換算不處理紅血球干擾，也不作診斷。')}
    ${lab(5,'血壓缺漏：有平均，不代表完整',select('bp-missing','虛構第7天晚間第2次',[['missing','缺漏：有效27/28'],['complete','已觀察：有效28/28']])+select('bp-first','首日處理規則',[['keep','保留全部排定日（預設）'],['exclude','明示排除首日作比較']]),'資料為7×早晚×2；展示收縮壓可用平均與完整性，不畫診斷線。排除首日是規則比較，不宣稱普遍722要求。',true)}
    ${lab(6,'non-HDL：同單位相減',field('nonhdl-tc','總膽固醇 mg/dL',200,0,600,.1)+field('nonhdl-hdl','HDL-C mg/dL',50,0,300,.1),'non-HDL-C=TC−HDL-C；必須同檢體、同單位。這裡沒有LDL估算或個人目標。')}
    ${lab(7,'FIB-4：四個輸入與一個前提',field('fib-age','成人年齡 歲',50,18,100)+field('fib-ast','AST U/L',30,0,1000,.1)+field('fib-alt','ALT U/L',25,.1,1000,.1)+field('fib-platelets','血小板 10^9/L',200,.1,1000,.1)+select('fib-context','使用情境',[['stable','明示穩定成人，只看公式'],['acute','急性或背景不明：不算']]),'age×AST/(platelets×√ALT)。不同年齡與路徑影響解釋，不顯示風險帶、分期或回診頻率。')}
    ${lab(8,'尿ACR：分母要是尿液',field('acr-albumin','同尿檢體白蛋白 mg/L',30,0,10000,.1)+field('acr-creatinine','同尿檢體肌酸酐 g/L',1,.01,20,.01),'mg/L÷g/L=mg/g；不能改用血清肌酸酐。單次比值不是慢性腎病診斷。')}
    ${lab(9,'相對與絕對：虛構三年事件人數',field('risk-e0','對照組事件人數',100,0,100000)+field('risk-n0','對照組總人數',1000,1,100000)+field('risk-e1','介入組事件人數',70,0,100000)+field('risk-n1','介入組總人數',1000,1,100000),'假設同結果、完整三年、每人至多一次事件；不是DPP人年資料。NNT／NNH為點估計，未提供信賴區間。',true)}
    ${lab(10,'篩檢Bayes：敏感度不是PPV',field('screen-prev','虛構盛行率 %',1,0,100,.1)+field('screen-sens','假設敏感度 %',90,0,100,.1)+field('screen-spec','假設特異度 %',95,0,100,.1),'假設一萬人，四格為期望人數；盛行率改變PPV。並非真實檢驗效能，也非個人診斷。',true)}
    ${lab(11,'PREVENT：只看年齡與期限的範圍',field('prevent-age','假設年齡 歲',45,0,110)+select('prevent-horizon','期限',[['10','十年'],['30','三十年']]),'十年30–79、三十年30–59。只核對年齡條件，不是完整適用性判定；ASCVD、總CVD、HF不可混用，美國模型不等於台灣校準。')}
    ${lab(12,'同一假設RR，不同基線的絕對差',field('effect-baseline','手動假設基線風險 %',5,0,100,.1)+field('effect-rr','手動假設相對風險RR',.8,0,3,.05),'只做baseline×RR，不含任何治療實證係數或個人預測；同一RR不保證適用所有族群。',true)}
    </section><section id="baseline" class="reading-note"><strong>正式版本、地區與離線實作</strong><p>2026-11-10查核：ADA2026、CKM2026、2026血脂與AGA路徑、KDIGO2024正式版、台灣2026高齡血壓與現行預防保健。草案、公告與未來生效規則另標，不混作現行定義。Python3.15.2，48份範例只用標準函式庫。</p><a href="examples/README.md">執行、資料與公式限制 ↗</a> · <a href="examples.zip" download>完整範例、資料與測試 ↓</a> · <a href="#96-exercises-and-references">總複習與來源 →</a></section>${footer}`;
    toc.innerHTML='<h2 class="toc-label">本頁導覽</h2><div class="toc-links"><a href="#overview/intro">關於課程</a><a href="#overview/scope">代謝、器官與預防</a><a href="#overview/quick-start">快速閱讀路線</a><a href="#overview/roadmap">完整目錄</a><a href="#overview/experiments">十二個互動實驗</a><a href="#overview/baseline">版本與下載</a></div><div class="toc-tip"><p>先確認分析物、單位、時間和用途，再解釋數字。</p><p>本課進度與筆記獨立保存。</p></div>';
    mount(main);
  };
  window.renderCourseOverview.courseSlug='metabolic-health';
  function mount(main){
    const q=s=>main.querySelector(s),n=id=>{const el=q('#'+id),v=Number(el.value);if(!el.value.trim()||!Number.isFinite(v)||v<Number(el.min)||v>Number(el.max))throw new RangeError('輸入需在欄位標示範圍內');return v;},s=id=>q('#'+id).value,f=v=>v===null?'未知／無定義':v.toFixed(3);
    const out=(i,text,ok=true)=>{q('#metabolic-out-'+i).textContent=text;q('#metabolic-out-'+i).dataset.status=ok?'ok':'error';},plot=(i,labels,values,unit)=>q('#metabolic-plot-'+i).innerHTML=bars('metabolic-bars-'+i,labels,values,unit);
    function bind(i,fn){const run=()=>{try{fn();}catch(error){out(i,error.message,false);const p=q('#metabolic-plot-'+i);if(p)p.innerHTML='';}};for(const control of q('#metabolic-lab-'+i).querySelectorAll('input,select'))control.addEventListener(control.tagName==='SELECT'?'change':'input',run);run();}
    bind(1,()=>{const rows=toy(n('balance-input'),n('balance-clearance'));q('#metabolic-plot-1').innerHTML=curve(rows);out(1,`第25步 ${f(rows.at(-1).state)} 任意模型單位。不是人體血糖或胰島素預測。`);});
    bind(2,()=>{const r=body(n('body-kg'),n('body-cm'),n('body-waist'));out(2,`BMI ${f(r.bmi)} kg/m²；腰高比 ${f(r.waistHeight)}。未產生分類或目標。`);});
    bind(3,()=>{const value=n('unit-value'),r=units(value,s('unit-analyte'),s('unit-direction'));out(3,`所選分析物：${value} ${r.source} ≈ ${f(r.value)} ${r.target}。保留原始報告；不是診斷。`);});
    bind(4,()=>{const source=s('a1c-source'),value=n('a1c-value');out(4,`${value} ${source==='NGSP'?'NGSP %':'IFCC mmol/mol'} → ${f(a1c(value,source))} ${source==='NGSP'?'IFCC mmol/mol':'NGSP %'}。這不是血糖mmol/L。`);});
    bind(5,()=>{const r=bp(s('bp-missing')==='missing',s('bp-first')==='exclude');plot(5,r.days.map(d=>`第${d.day}天 n=${d.n}/4`),r.days.map(d=>d.mean),'mmHg');out(5,`有效 ${r.valid}／排定 ${r.expected}；可用收縮壓平均 ${f(r.available)} mmHg；完整平均 ${f(r.complete)}。不作診斷或藥物判斷。`);});
    bind(6,()=>out(6,`non-HDL-C ${f(nonhdl(n('nonhdl-tc'),n('nonhdl-hdl')))} mg/dL。沒有個人風險或治療目標。`));
    bind(7,()=>out(7,`FIB-4公式值 ${f(fib4(n('fib-age'),n('fib-ast'),n('fib-alt'),n('fib-platelets'),s('fib-context')==='stable'))}。非診斷、非纖維化分期。`));
    bind(8,()=>out(8,`尿ACR算術 ${f(acr(n('acr-albumin'),n('acr-creatinine')))} mg/g。仍需採樣、持續性與臨床背景。`));
    bind(9,()=>{const r=risk(n('risk-e0'),n('risk-n0'),n('risk-e1'),n('risk-n1'));plot(9,['對照三年風險','介入三年風險'],[r.p0*100,r.p1*100],'%');out(9,`RR ${f(r.rr)}；相對降低 ${r.rrr===null?'未知':f(r.rrr*100)+'%'}；ARR ${f(r.arr*100)} 個百分點；${r.direction==='降低'?'NNT':r.direction==='增加'?'NNH':'無有限NNT'}點值 ${f(r.number)}。虛構三年，方向：${r.direction}。`);});
    bind(10,()=>{const r=screening(10000,n('screen-prev')/100,n('screen-sens')/100,n('screen-spec')/100);plot(10,['真陽性','偽陽性','真陰性','偽陰性'],[r.tp,r.fp,r.tn,r.fn],'人（期望）');out(10,`PPV ${r.ppv===null?'未知':f(r.ppv*100)+'%'}；NPV ${r.npv===null?'未知':f(r.npv*100)+'%'}。分母與敏感度不同，不作個人診斷。`);});
    bind(11,()=>{const age=n('prevent-age'),h=Number(s('prevent-horizon'));out(11,`${age}歲、${h}年：年齡條件${ageScope(age,h)?'在範圍內':'不在範圍內'}。尚未判定完整適用性，沒有產生PREVENT機率。`);});
    bind(12,()=>{const r=assumed(n('effect-baseline')/100,n('effect-rr'));plot(12,['假設基線','假設乘積'],[r.before*100,r.after*100],'%');out(12,`假設差 ${f(r.difference*100)} 個百分點。沒有實際治療效果係數，未推估個人風險。`);});
  }
})();
