/* Original teaching models, fictional data and explicit scope. No health scoring. */
(() => {
  'use strict';
  const finite=(...v)=>{if(v.some(x=>typeof x!=='number'||!Number.isFinite(x)))throw new RangeError('需輸入有限數字');};
  const nn=(...v)=>{finite(...v);if(v.some(x=>x<0))throw new RangeError('需輸入非負數字');};
  const pos=(...v)=>{nn(...v);if(v.some(x=>x===0))throw new RangeError('分母、長度與時長需大於0');};
  const integer=(...v)=>{nn(...v);if(v.some(x=>!Number.isSafeInteger(x)))throw new RangeError('次數需為非負整數');};
  const flag=v=>{if(typeof v!=='boolean')throw new RangeError('需明示完整或適用狀態');};
  function moment(force=100,radius=.3,angle=90){nn(force,radius,angle);if(angle>180)throw new RangeError('夾角需在0至180度');return force*radius*Math.sin(angle*Math.PI/180);}
  function pressure(force=100,area=10){nn(force);pos(area);return force/(area*.0001)/1000;}
  function fit(reach=60,clearance=62){pos(reach,clearance);const rows=Array.from({length:12},(_,j)=>{const i=j+1,r=i===11?null:50+2*i,c=i===12?null:55+i;return {id:'F'+String(i).padStart(2,'0'),reach:r,clearance:c,result:r===null||c===null?null:r>=reach&&c<=clearance};}),known=rows.filter(r=>r.result!==null),matched=known.filter(r=>r.result).length;return {rows,known:known.length,matched,unmatched:known.length-matched,unknown:12-known.length,fraction:known.length?matched/known.length:null};}
  function geometry(horizontal=60,vertical=-15){pos(horizontal);finite(vertical);return {distance:Math.hypot(horizontal,vertical),angle:Math.atan2(vertical,horizontal)*180/Math.PI};}
  function angular(height=4,distance=60){pos(height,distance);return 2*Math.atan(height/(2*distance*10))*180/Math.PI;}
  function schedule(work=50,change=10,cycles=4){pos(work);nn(change);integer(cycles);if(!cycles)throw new RangeError('至少一個週期');return {work:work*cycles,change:change*cycles,total:(work+change)*cycles};}
  function repetition(actions=90,observed=10,active=7){integer(actions);pos(observed);nn(active);if(active>observed)throw new RangeError('活動時間不能超過觀察時間');return {rate:actions/observed,fraction:active/observed};}
  function rnle(load=12,h=25,v=75,d=50,a=0,fm=.94,cm=1,verified=true){
    nn(load,h,v,d,a);flag(verified);
    if(h>63||v>175||d>175||a>135)throw new RangeError('超出本課RNLE幾何範圍，不能裁到上限繼續');
    for(const x of [fm,cm])if(x!==null){nn(x);if(x>1)throw new RangeError('倍率需在0至1，未知不可填最佳值');}
    const factors={HM:25/Math.max(25,h),VM:1-.003*Math.abs(v-75),DM:.82+4.5/Math.max(25,d),AM:1-.0032*a,FM:fm,CM:cm};
    const rwl=verified&&fm!==null&&cm!==null?23*Object.values(factors).reduce((p,x)=>p*x,1):null;
    return {factors,rwl,li:rwl===null||rwl===0?null:load/rwl};
  }
  function hav(a=4,ta=120,b=2,tb=120,complete=true){
    flag(complete);for(const x of [a,ta,b,tb])if(x!==null)nn(x);
    if((ta??0)+(tb??0)>1440)throw new RangeError('不重疊觸發時間不能超過一天');
    const known=[[a,ta],[b,tb]].filter(p=>p.every(x=>x!==null)),subtotal=Math.sqrt(known.reduce((s,[v,t])=>s+v*v*t,0)/480);
    return {subtotal,a8:complete&&known.length===2?subtotal:null};
  }
  function work(force=100,distance=5,seconds=10,angle=0){nn(force,distance,angle);pos(seconds);if(angle>90)throw new RangeError('本課同向推拉模型夾角需在0至90度');const joules=force*Math.cos(angle*Math.PI/180)*distance;return {joules,watts:joules/seconds};}
  const CONTROLS={eliminate:'消除：先評估取消不必要轉運或重複步驟，確認沒有把危害轉給別人。',engineering:'工程：調整存放、支撐、治具或設備，同時確認可達性、維護及新危害。',organization:'組織：協調人力、節奏、維護與回報；輪調要確認實際改變暴露。',ppe:'個人裝備：配合必要防護及工作條件，確認尺寸、抓握與限制；不取代來源改善。'};
  function control(name='engineering'){if(!Object.hasOwn(CONTROLS,name))throw new RangeError('需選控制方向');return CONTROLS[name];}
  function observations(mode='missing'){
    if(!['missing','complete','zero'].includes(mode))throw new RangeError('需選明示的虛構資料');
    const values=mode==='zero'?Array(12).fill(0):[80,90,100,70,85,95,90,80,100,110,90,mode==='complete'?90:null],known=values.filter(x=>x!==null),sum=known.reduce((a,b)=>a+b,0);
    return {values,observed:known.length,missing:12-known.length,minutes:known.length*10,subtotal:sum,available:sum/(known.length*10),complete:known.length===12?sum:null};
  }
  window.ErgoLab=Object.freeze({moment,pressure,fit,geometry,angular,schedule,repetition,rnle,hav,work,control,observations});
  const esc=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const field=(id,label,value,min=0,max=10000,step='1')=>`<label for="${id}"><span>${label}</span><input id="${id}" type="number" value="${value}" min="${min}" max="${max}" step="${step}"></label>`;
  const select=(id,label,options)=>`<label for="${id}"><span>${label}</span><select id="${id}">${options.map(([v,t],i)=>`<option value="${v}"${i===0?' selected':''}>${t}</option>`).join('')}</select></label>`;
  const lab=(i,title,controls,caption,plot=false)=>`<section class="ergo-lab" id="ergo-lab-${i}"><header><span class="mono">LAB ${String(i).padStart(2,'0')}</span><h3>${title}</h3></header><div class="ergo-lab-body"><div class="ergo-controls">${controls}</div>${plot?`<div id="ergo-plot-${i}" class="ergo-plot"></div>`:''}<output id="ergo-out-${i}" aria-live="polite"></output><p class="lab-caption">${caption}</p></div></section>`;
  function bars(id,labels,values,unit){const max=Math.max(1,...values.filter(v=>v!==null));return `<svg class="ergo-chart" viewBox="0 0 680 ${55+labels.length*36}" role="img" aria-labelledby="${id}-title"><title id="${id}-title">${esc(unit)}：${labels.map((s,i)=>esc(s)+' '+(values[i]===null?'未知':values[i].toFixed(3))).join('；')}</title>${labels.map((s,i)=>`<text x="10" y="${34+i*36}">${esc(s)}</text><rect x="170" y="${17+i*36}" width="${values[i]===null?0:values[i]/max*260}" height="23" rx="3" fill="${i%2?'#a4c7e9':'#b5e99b'}" opacity=".75"/><text x="450" y="${34+i*36}">${values[i]===null?'未知':values[i].toFixed(3)} ${esc(unit)}</text>`).join('')}</svg>`;}
  function diagram(horizontal,vertical){const scale=160/Math.max(horizontal,Math.abs(vertical),1),x=80+horizontal*scale,y=130-vertical*scale;return `<svg class="ergo-chart" viewBox="0 0 550 300" role="img" aria-labelledby="ergo-geometry-title"><title id="ergo-geometry-title">點到點視線幾何：水平${horizontal}cm，垂直${vertical}cm；不是建議角度或姿勢</title><path d="M60 130H280M80 280V15" fill="none" stroke="currentColor" stroke-dasharray="4 5"/><path d="M80 130L${x} ${y}" fill="none" stroke="#b5e99b" stroke-width="3"/><circle cx="80" cy="130" r="5" fill="#a4c7e9"/><circle cx="${x}" cy="${y}" r="5" fill="#b5e99b"/><text x="300" y="70">眼睛為原點</text><text x="300" y="100">向右：水平距離</text><text x="300" y="130">向上：垂直正值</text><text x="300" y="160">僅示範兩個點的幾何</text></svg>`;}
  window.renderCourseOverview=({course,saved,escapeHTML:e,main,toc,footer})=>{
    const start=saved.last||course.lessons[0].id;
    main.innerHTML=`<section class="course-hero" id="intro"><div class="eyebrow">THE ERGONOMICS GUIDE <span>／ 讓任務與環境，適合人的需要</span></div><h1>Move. Adapt. Work<span class="hero-period">.</span></h1><h2 class="hero-subtitle">理解身體承受什麼，<br>也學會改變工作的條件。</h2><p class="hero-description">從骨、關節、肌肉、神經與疼痛，走到桌椅、鍵鼠、搬抬、工具和振動。用任務分析找到改善方向，用清楚的模型理解算術，也保留人的差異與未知。</p><div class="hero-meta"><span><b>16</b> 章主線</span><span><b>96</b> 個閱讀單元</span><span><b>48</b> 份 Python 範例</span><span><b>12</b> 個互動實驗</span></div><div class="hero-actions"><a class="primary-button" href="#${start}">${saved.last?'繼續學習':'從人、任務與環境開始'} <span aria-hidden="true">↗</span></a><a class="text-link" href="#overview/experiments">先動手改變一個力臂 ↓</a></div></section>
    <section id="scope" class="ergo-scope"><div><span class="mono">UNDERSTAND · 01–05</span><h3>身體與觀察</h3><p>結構、力學、疼痛與任務資料，先建立能解釋的基礎。</p></div><div><span class="mono">ADAPT · 06–12</span><h3>工作與環境</h3><p>工作站、上下肢任務、搬抬、重複、推拉與振動。</p></div><div><span class="mono">VERIFY · 13–16</span><h3>改善與證據</h3><p>參與式設計、台灣預防計畫、不同需求與可重跑報告。</p></div></section>
    <section id="quick-start"><div class="section-header"><h2>完整學習，也能先解決一個工作問題</h2><span>OBSERVE → UNDERSTAND → ADAPT → REVIEW</span></div><div class="ergo-route"><p><a href="#01-ergonomics-map">學科地圖</a> → <a href="#13-forces-and-moments">外力與力矩</a> → <a href="#25-task-analysis">觀察任務</a> → <a href="#31-seat-and-support">桌椅配置</a> → <a href="#55-rnle-equation">搬抬公式</a> → <a href="#78-taiwan-prevention-plan">台灣預防計畫</a> → <a href="#95-complete-capstone">完整專題</a>。</p><p><strong>基礎與課內進階都在本課。</strong>電腦工作可先讀第6–8章，搬運與現場工作讀第10–13章；從零學習依16章順序。閱讀不需Python，互動與範例只用明示假設及虛構資料。</p><p>疼痛與功能需求見<a href="#19-pain-and-nociception">第4章</a>；<a href="#23-when-to-seek-help">需要及時評估的情況</a>可直接閱讀，不用先完成課程。</p></div></section>
    <section id="roadmap"><div class="section-header"><h2>完整學習路線</h2><span>16 CHAPTERS · 96 UNITS</span></div><div class="module-list">${course.groups.map(g=>{const units=course.lessons.filter(l=>l.group===g.id);return `<a class="module-row" href="#${units[0].id}"><span class="module-num">${g.number}</span><div><div class="module-name">${e(g.title)}</div><div class="module-description">${e(g.description)}</div></div><span class="module-count">${units.length} UNITS ↗</span></a>`;}).join('')}</div></section>
    <section id="experiments"><div class="section-header"><h2>把距離、力與資料的關係看清楚</h2><span>12 INTERACTIVE LABS</span></div><p class="hero-description">調整假設、比較算術與未知。模型不測你的組織負荷、不診斷、不預測個人傷害，也不提供正式工具總分或合規認證。</p>
    ${lab(1,'力矩：同一個力，作用位置不同',field('moment-force','外力 F（N）',100,0,10000,.1)+field('moment-radius','作用點距離 r（m）',.3,0,10,.01)+field('moment-angle','r與F夾角（°）',90,0,180,.1),'M=F×r×sinθ，顯示力矩大小；不是腰椎、肌肉或組織實際內力。',true)}
    ${lab(2,'接觸壓：平均分配的簡化模型',field('pressure-force','外力（N）',100,0,10000,.1)+field('pressure-area','假設均勻接觸面積（cm²）',10,.01,10000,.1),'P=F/A。真實接觸通常不均勻；此處不是皮膚或神經傷害門檻。',true)}
    ${lab(3,'兩個尺寸條件，必須同時成立',field('fit-reach','要求伸取距離（cm）',60,1,150)+field('fit-clearance','可用淨空（cm）',62,1,150),'12名虛構使用者；伸取能力≥要求且淨空需求≤可用才符合。兩人缺項保持未知，不是人口覆蓋率或健康保證。',true)}
    ${lab(4,'視線幾何：位置、距離與角度',field('view-horizontal','水平距離（cm）',60,1,200,.5)+field('view-vertical','目標相對眼睛垂直位置（cm）',-15,-100,100,.5),'負值在眼睛下方。畫面只顯示兩點幾何，不決定理想頸部角度；字體、眼鏡、視力與任務仍需考量。',true)}
    ${lab(5,'文字視角：大小和距離一起看',field('angle-height','文字實體高度（mm）',4,.1,100,.1)+field('angle-distance','觀察距離（cm）',60,1,300,.5),'α=2 atan(h/2d)，使用相同長度單位；不是視力檢查、螢幕CSS字級或通用字體處方。',true)}
    ${lab(6,'工作變化的時間帳本',field('schedule-work','每週期原任務分鐘',50,1,240)+field('schedule-change','每週期改變活動分鐘',10,0,120)+field('schedule-cycles','週期數',4,1,20),'只算排程。改變活動不一定是充分恢復；這不是每小時休息的通用法令，也不是RNLE工時分類或個人休息處方。',true)}
    ${lab(7,'次數與活動比例：分母有何不同',field('rep-actions','觀察窗中的動作次數',90,0,100000)+field('rep-observed','觀察窗分鐘',10,.1,120,.1)+field('rep-active','其中活動分鐘',7,0,120,.1),'次數/觀察分鐘與活動分鐘/觀察分鐘不同。不是ART評分，也不能代替RNLE規定的頻率觀察和工時分類。')}
    ${lab(8,'RNLE：明示假設下的倍率算術',field('rnle-load','負重（kg）',12,0,100,.1)+field('rnle-h','H水平距離（cm）',25,0,63,.5)+field('rnle-v','V手部高度（cm）',75,0,175,.5)+field('rnle-d','D垂直位移（cm）',50,0,175,.5)+field('rnle-a','A不對稱位置角（°）',0,0,135,.5)+select('rnle-context','適用與表格條件',[['teaching','明示教學假設：已確認條件'],['unknown','尚未確認：保留未知']]),'假設FM=.94（1次/分鐘、短工時及符合恢復），CM=1（正式良好抓握），非自動查表。H從內踝中點到手部投影，A不是脊柱扭轉角；H/D低於25按手冊處理，超上限拒絕。只示範單一端、單一情境，不是完整現場評估；23kg非個人通用限重，LI非傷害機率。',true)}
    ${lab(9,'手－手臂振動：平方與實際觸發時間',field('hav-a','A段已加權三軸合成 a_hv（m/s²）',4,0,100,.1)+field('hav-ta','A段實際觸發分鐘',120,0,1440)+field('hav-b','B段已加權三軸合成 a_hv（m/s²）',2,0,100,.1)+field('hav-tb','B段實際觸發分鐘',120,0,1440)+select('hav-complete','整日資料',[['complete','明示僅這兩段，資料完整'],['missing','另有未知段，完整日值未知']]),'A(8)=√Σ(a²×分鐘)/480；輸入已完成正式頻率加權和三軸合成，時間不重疊。不是手機原始加速度，不可用於WBV；不提供法規或個人健康判定。',true)}
    ${lab(10,'推拉外功：不是代謝消耗',field('work-force','指定恆定外力（N）',100,0,10000,.1)+field('work-distance','水平位移（m）',5,0,1000,.1)+field('work-time','完成時間（s）',10,.1,10000,.1)+field('work-angle','外力與位移夾角（°）',0,0,90,.1),'W=F×d×cosθ；平均外功率=W/t。未測啟動力、路況、人體內部作功或效率，不能換成熱量或安全推拉限力。',true)}
    ${lab(11,'同一任務，可以在哪裡改變',select('control-direction','虛構取料工作的改善方向',[['engineering','工程設計'],['eliminate','消除不必要工作段'],['organization','組織與維護'],['ppe','必要個人裝備']]),'原創控制層級文字，不計正式風險分數；需參與式試用、檢查新危害與回顧。')}
    ${lab(12,'觀察缺漏：已知小計不等於完整總量',select('obs-mode','12段、每段10分鐘的虛構資料',[['missing','原始案例：11段已知、1段未知'],['complete','另明示第12段為90次'],['zero','另組完整觀察：全部0次']]),'柱狀圖只表示動作數。最後一段未知不是休息或0；可用頻率的分母是已觀察分鐘，不是原排120分鐘，更非完整班次。',true)}
    </section><section id="baseline" class="reading-note"><strong>正式版次、查核與離線學習</strong><p>2026-11-13查核：RNLE採Revised9/2021（含短工時恢復更正），入口2026更新；台灣指引標2014初版，法規依現行條文；臨床來源區分WHO2023、NICE2026更新與適用範圍。Python3.15.2，只用標準函式庫。所有實驗在本機運算，無攝影或個人資料蒐集。</p><a href="examples/README.md">執行方式、資料及模型限制 ↗</a> · <a href="examples.zip" download>下載完整程式、資料與測試 ↓</a> · <a href="#96-exercises-and-references">綜合練習與來源 →</a></section>${footer}`;
    toc.innerHTML='<h2 class="toc-label">本頁導覽</h2><div class="toc-links"><a href="#overview/intro">關於課程</a><a href="#overview/scope">身體、工作與改善</a><a href="#overview/quick-start">閱讀路線</a><a href="#overview/roadmap">完整目錄</a><a href="#overview/experiments">十二個互動實驗</a><a href="#overview/baseline">版本與下載</a></div><div class="toc-tip"><p>先確認任務、單位、分母與適用範圍。</p><p>改善要追蹤，未知要保留。</p></div>';
    mount(main);
  };
  window.renderCourseOverview.courseSlug='ergonomics';
  function mount(main){
    const q=s=>main.querySelector(s),n=id=>{const el=q('#'+id),v=Number(el.value);if(!el.value.trim()||!Number.isFinite(v)||v<Number(el.min)||v>Number(el.max))throw new RangeError('數字需在欄位標示範圍內');return v;},s=id=>q('#'+id).value,f=v=>v===null?'未知／無定義':v.toFixed(3);
    const out=(i,text,ok=true)=>{q('#ergo-out-'+i).textContent=text;q('#ergo-out-'+i).dataset.status=ok?'ok':'error';},plot=(i,labels,values,unit)=>q('#ergo-plot-'+i).innerHTML=bars('ergo-bars-'+i,labels,values,unit);
    function bind(i,fn){const run=()=>{try{fn();}catch(error){out(i,error.message,false);const p=q('#ergo-plot-'+i);if(p)p.innerHTML='';}};for(const el of q('#ergo-lab-'+i).querySelectorAll('input,select'))el.addEventListener(el.tagName==='SELECT'?'change':'input',run);run();}
    bind(1,()=>{const m=moment(n('moment-force'),n('moment-radius'),n('moment-angle'));plot(1,['外力矩大小'],[m],'N·m');out(1,`外力矩大小 ${f(m)} N·m。不是組織內力或傷害預測。`);});
    bind(2,()=>{const p=pressure(n('pressure-force'),n('pressure-area'));plot(2,['假設平均壓力'],[p],'kPa');out(2,`均勻模型 ${f(p)} kPa，不代表實際局部峰值或健康門檻。`);});
    bind(3,()=>{const r=fit(n('fit-reach'),n('fit-clearance'));plot(3,['已知符合','已知不符合','未知'],[r.matched,r.unmatched,r.unknown],'人');out(3,`已知 ${r.known}/12；符合 ${r.matched}，不符合 ${r.unmatched}，未知 ${r.unknown}；已知樣本比例 ${r.fraction===null?'未知':f(r.fraction*100)+'%'}。僅兩條幾何條件，非人口或健康保證。`);});
    bind(4,()=>{const h=n('view-horizontal'),v=n('view-vertical'),r=geometry(h,v);q('#ergo-plot-4').innerHTML=diagram(h,v);out(4,`點到點距離 ${f(r.distance)} cm；相對水平角 ${f(r.angle)}°。不決定理想姿勢。`);});
    bind(5,()=>{const a=angular(n('angle-height'),n('angle-distance'));plot(5,['文字視角'],[a],'°');out(5,`視角 ${f(a)}°＝${f(a*60)}角分；不是視力或字體處方。`);});
    bind(6,()=>{const r=schedule(n('schedule-work'),n('schedule-change'),n('schedule-cycles'));plot(6,['原任務時間','改變活動時間'],[r.work,r.change],'分鐘');out(6,`總 ${f(r.total)} 分鐘，原任務 ${f(r.work)}、改變活動 ${f(r.change)}。不是通用休息規範或充分恢復保證。`);});
    bind(7,()=>{const r=repetition(n('rep-actions'),n('rep-observed'),n('rep-active'));out(7,`每觀察分鐘 ${f(r.rate)} 次；活動比例 ${f(r.fraction*100)}%。不是正式工具分數或完整班次值。`);});
    bind(8,()=>{const verified=s('rnle-context')==='teaching',r=rnle(n('rnle-load'),n('rnle-h'),n('rnle-v'),n('rnle-d'),n('rnle-a'),verified?.94:null,verified?1:null,verified);plot(8,Object.keys(r.factors),Object.values(r.factors),'倍率');out(8,`教學RWL ${f(r.rwl)} kg；LI ${f(r.li)}。${verified?'FM=.94、CM=1及適用條件皆為明示教學假設。':'適用及表格條件未確認，不能宣告可用限值。'}不是個人限重、傷害機率或安全認證。`);});
    bind(9,()=>{const r=hav(n('hav-a'),n('hav-ta'),n('hav-b'),n('hav-tb'),s('hav-complete')==='complete');plot(9,['已知段A(8)小計','完整日A(8)'],[r.subtotal,r.a8],'m/s²');out(9,`已知段A(8)小計 ${f(r.subtotal)} m/s²；完整日A(8) ${f(r.a8)} m/s²。不是WBV或個人疾病判定。`);});
    bind(10,()=>{const r=work(n('work-force'),n('work-distance'),n('work-time'),n('work-angle'));plot(10,['指定外力作功'],[r.joules],'J');out(10,`外功 ${f(r.joules)} J；平均外功率 ${f(r.watts)} W。不是代謝消耗或安全限力。`);});
    bind(11,()=>out(11,control(s('control-direction'))+'\n與工作者討論、試用並追蹤，不以單一措施宣告完成。'));
    bind(12,()=>{const r=observations(s('obs-mode'));plot(12,r.values.map((_,i)=>'時段'+String(i+1).padStart(2,'0')),r.values,'次');out(12,`排定120分鐘；觀察 ${r.observed}/12段、${r.minutes}分鐘；缺 ${r.missing}段；已知小計 ${r.subtotal}次；可用頻率 ${f(r.available)}次/分鐘；完整總量 ${f(r.complete)}次。不是傷害分級。`);});
  }
})();
