/* Original offline population-health teaching cases; no external data or personal risk scoring. */
(() => {
  'use strict';
  const finite=(v,n)=>{if(typeof v!=='number'||!Number.isFinite(v))throw new RangeError(`${n}需為有限數字`);return v;};
  const nonnegative=(v,n)=>{finite(v,n);if(v<0)throw new RangeError(`${n}不能小於0`);return v;};
  const positive=(v,n)=>{finite(v,n);if(v<=0)throw new RangeError(`${n}需大於0`);return v;};
  const integer=(v,n)=>{nonnegative(v,n);if(!Number.isSafeInteger(v))throw new RangeError(`${n}需為可精確計數的非負整數`);return v;};
  const probability=(v,n)=>{nonnegative(v,n);if(v>1)throw new RangeError(`${n}需在0至1`);return v;};
  const ratio=(a,b)=>b===0?null:a/b;
  const checked=(v,n)=>{if(v!==null&&!Number.isFinite(v))throw new RangeError(`${n}超出此計算器範圍`);return v;};
  function frequency(population=1000,existing=100,newCases=45,personYears=810){
    for(const [v,n] of [[population,'基線人口'],[existing,'基線既有個案'],[newCases,'追蹤期間新個案']])integer(v,n);
    positive(population,'基線人口');positive(personYears,'實際無病人年');
    if(existing>population)throw new RangeError('既有個案不能超過基線人口');
    const atRisk=population-existing;if(newCases>atRisk)throw new RangeError('此首次發病封閉世代的新個案不能超過基線無病人數');
    if(personYears>atRisk)throw new RangeError('此一年度封閉世代的無病人年不能超過基線無病人數×1年');
    const rate=checked(newCases/personYears,'發生率');checked(rate*100,'每100人年發生率');
    return {population,existing,newCases,personYears,atRisk,prevalence:existing/population,risk:ratio(newCases,atRisk),rate};
  }
  function comparison(a=40,b=160,c=20,d=180){
    for(const [v,n] of [[a,'曝露發病'],[b,'曝露未發病'],[c,'未曝露發病'],[d,'未曝露未發病']])integer(v,n);
    if(!Number.isSafeInteger(a+b+c+d))throw new RangeError('總數超出精確計數範圍');
    const riskE=ratio(a,a+b),riskU=ratio(c,c+d),rr=riskE===null||riskU===null?null:ratio(riskE,riskU),rd=riskE===null||riskU===null?null:riskE-riskU;
    // Ratios of bounded row fractions avoid an overflowing cross-product.
    const oddsE=ratio(a,b),oddsU=ratio(c,d),or=oddsE===null||oddsU===null?null:ratio(oddsE,oddsU);
    return {a,b,c,d,riskE,riskU,rr:checked(rr,'風險比'),rd,or:checked(or,'勝算比')};
  }
  const AGE={a:[{events:20,n:1000},{events:80,n:1000}],b:[{events:36,n:2400},{events:36,n:600}]};
  function standardize(youngWeight=.8){
    probability(youngWeight,'共同標準年輕層權重');const weights=[youngWeight,1-youngWeight];
    const result=rows=>({rates:rows.map(r=>r.events/r.n),crude:rows.reduce((s,r)=>s+r.events,0)/rows.reduce((s,r)=>s+r.n,0),adjusted:rows.reduce((s,r,i)=>s+r.events/r.n*weights[i],0)});
    return {weights,a:result(AGE.a),b:result(AGE.b)};
  }
  function simpson(youngWeight=.5){
    probability(youngWeight,'共同年輕層權重');return {weights:[youngWeight,1-youngWeight],e:{young:.9,old:.6,crude:93/110,adjusted:.9*youngWeight+.6*(1-youngWeight)},u:{young:.95,old:.7,crude:82/110,adjusted:.95*youngWeight+.7*(1-youngWeight)}};
  }
  const ONSET=[0,1,2,5,9,7,4,2,1,0];
  function surveillance(mode='onset'){
    if(!['onset','report'].includes(mode))throw new RangeError('請選發病日或通報日');
    const rows=[];ONSET.forEach((count,day)=>{for(let i=0;i<count;i++)rows.push({onset:day+1,report:day+2+i%2});});
    rows.push({onset:null,report:8},{onset:null,report:9},{onset:null,report:10});
    const counts=Array(12).fill(0);for(const r of rows)if(r[mode]!==null)counts[r[mode]-1]++;
    return {mode,counts,total:rows.length,known:counts.reduce((a,b)=>a+b,0),unknown:rows.filter(r=>r[mode]===null).length,rows};
  }
  function completeness(present=24,expected=30){integer(present,'已填欄位');integer(expected,'應填欄位');if(present>expected)throw new RangeError('已填欄位不能超過應填欄位');return {present,expected,fraction:ratio(present,expected)};}
  function sir(beta=.3,gamma=.1,days=80){
    nonnegative(beta,'傳播率參數β');nonnegative(gamma,'移出率參數γ');integer(days,'模擬天數');
    if(beta>2||gamma>2||days>180)throw new RangeError('教學範圍：β與γ最多2／日，時間最多180日');
    const n=1000,dt=.1,steps=days*10;let s=990,i=10,r=0;const points=[{day:0,s,i,r}];
    for(let step=1;step<=steps;step++){const infection=beta*s*i/n*dt,removal=gamma*i*dt;s-=infection;i+=infection-removal;r+=removal;if(step%10===0)points.push({day:step/10,s,i,r});}
    const r0=checked(ratio(beta,gamma),'R0');
    return {beta,gamma,days,n,dt,points,r0,initialRt:r0===null?null:r0*.99,immuneThreshold:gamma>0&&beta>gamma?1-gamma/beta:null};
  }
  function vaccine(vCases=20,vTotal=1000,uCases=80,uTotal=1000){
    const c=comparison(vCases,vTotal-vCases,uCases,uTotal-uCases);
    return {vCases,vTotal,uCases,uTotal,riskV:c.riskE,riskU:c.riskU,rr:c.rr,ve:c.rr===null?null:1-c.rr,arr:c.rd===null?null:-c.rd};
  }
  function screening(n=10000,prevalence=.01,sensitivity=.9,specificity=.95){
    integer(n,'受檢人數');positive(n,'受檢人數');for(const [v,k] of [[prevalence,'參照疾病盛行率'],[sensitivity,'敏感度'],[specificity,'特異度']])probability(v,k);
    const diseased=n*prevalence,healthy=n-diseased,tp=diseased*sensitivity,fn=diseased*(1-sensitivity),tn=healthy*specificity,fp=healthy*(1-specificity);
    return {n,prevalence,sensitivity,specificity,tp,fn,fp,tn,ppv:ratio(tp,tp+fp),npv:ratio(tn,tn+fn),positive:tp+fp};
  }
  function equity(worse=.4,better=.1){probability(worse,'群體甲不良結果風險');probability(better,'群體乙不良結果風險');return {worse,better,gap:worse-better,ratio:ratio(worse,better)};}
  function economics(costA=100000,effectA=1000,costB=120000,effectB=1010){
    for(const [v,n] of [[costA,'A成本'],[effectA,'A效果'],[costB,'B成本'],[effectB,'B效果']])nonnegative(v,n);
    const dc=costB-costA,de=effectB-effectA;let status;
    if(de===0)status=dc===0?'成本與效果相同':dc<0?'同效果，B成本較低':'同效果，B成本較高';
    else if(dc<0&&de>0)status='B嚴格支配A：成本較低且效果較高';
    else if(dc===0&&de>0)status='B同成本且效果較高';
    else if(dc>0&&de<0)status='A嚴格支配B：成本較低且效果較高';
    else if(dc===0&&de<0)status='A同成本且效果較高';
    else if(de>0)status='B增加成本也增加效果，需要門檻、預算與公平判斷';
    else status='B節省成本但減少效果，需要明示取捨';
    return {costA,effectA,costB,effectB,dc,de,icer:checked(ratio(dc,de),'ICER'),status};
  }
  const QUIZ=[
    ['盛行率與發生率的分母一樣嗎？',['一樣，都是人數百分比','不同，發生率需明確的人時','只要有個案數就能算'],1,'先分清既有個案、新個案、基線風險集合與觀察時間。'],
    ['病例對照抽樣的病例比例能直接當人口風險嗎？',['不能，抽樣機制改變了病例比例','可以，所有二乘二表都一樣','把樣本數加倍即可'],0,'控制組來源與抽樣設計決定OR如何解釋，不能從抽樣後比例硬算人口RR。'],
    ['兩地粗死亡率不同，下一步合理的是？',['直接排名醫療品質','只刪掉高齡人口','核對年齡、口徑與共同標準權重'],2,'標準化改善指定結構的可比較性，仍不等於已排除所有因果問題。'],
    ['把所有變數都放入模型，能保證沒有偏差嗎？',['不行，調整碰撞點或中介可能改變問題','可以，變數越多越正確','只有AI才可以保證'],0,'時間順序、目標效果與因果圖協助決定調整集合。'],
    ['通報個案突然上升可能代表什麼？',['一定是傳播加快','也可能是檢測、定義、延遲或回補改變','一定是系統出錯'],1,'監測的觀察機制是訊號的一部分，需要一起調查。'],
    ['理想化SIR的1−1/R0可以直接變成所有地方接種目標嗎？',['任何疫苗都可以','只看人口就可以','不行，還有疫苗終點、效力、接觸及免疫變化'],2,'均質模型的免疫比例閾值與真實接種覆蓋率不是同一件事。'],
    ['聚餐食物A風險比3，是否已證明它是唯一來源？',['沒有，需時間、其他食物、實驗室與環境證據','已經證明，不需再查','只要RR超過2都是因果'],0,'調查是多種證據逐步修正假說，不只選最大的數字。'],
    ['同樣敏感度與特異度，較低盛行率通常怎樣影響PPV？',['PPV一定變100%','PPV可能降低，偽陽性佔比增加','完全沒有影響'],1,'在相同測試條件下，把所有預期人數一起放進二乘二表才看得到。'],
    ['篩檢後診斷存活時間延長，能單獨證明減少死亡嗎？',['可以','只要多診斷就可以','不能，需考慮前置時間與過度診斷等偏差'],2,'重要終點、比較組與整個追蹤照護路徑比單一存活時間更關鍵。'],
    ['健康絕對差距縮小，相對比值會一定縮小嗎？',['不一定，兩種尺度可能不同方向','一定','只要總平均變好就不用看'],0,'公平評估需同時呈現群體、兩種尺度、需求與程序。'],
    ['負的ICER能直接判定政策划算嗎？',['可以，負數永遠最好','不能，要先看成本與效果差的象限','只看效果就好'],1,'省成本且增效果，與省成本但減效果，是不同情境；還有預算與公平。'],
    ['查核到2025已通過大流行協定，能直接寫所有國家已受其拘束嗎？',['可以，採納就是全球生效','只要有新聞就可以','不能，要另查附件、簽署、批准與生效狀態'],2,'2026-11-17時點須查核正式程序和PABS談判狀態，不把不同法律階段混寫。']
  ];
  function quiz(index,choice=null){if(!Number.isInteger(index)||index<0||index>=QUIZ.length)throw new RangeError('題目不存在');const [question,options,answer,why]=QUIZ[index];if(choice!==null&&(!Number.isInteger(choice)||choice<0||choice>2))throw new RangeError('選項不存在');return {question,options:[...options],answer,why,correct:choice===null?null:choice===answer};}
  window.PublicHealthLab=Object.freeze({frequency,comparison,standardize,simpson,surveillance,completeness,sir,vaccine,screening,equity,economics,quiz,quizCount:QUIZ.length});
  const esc=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const fmt=(n,d=3)=>n===null?'未定義':n.toLocaleString('zh-TW',{maximumFractionDigits:d}),pct=n=>n===null?'未定義':fmt(n*100)+'%';
  const compact=n=>Math.abs(n)>=1e6?n.toExponential(2):fmt(n);
  const field=(id,label,value,step='1')=>`<div><label for="${id}">${label}</label><input id="${id}" type="number" value="${value}" step="${step}"></div>`;
  const lab=(n,title,body,note)=>`<article class="public-lab" id="lab-${n}"><header><span class="mono">EXPLORE ${String(n).padStart(2,'0')}</span><h3>${title}</h3></header>${body}<p class="public-lab-note">${note}</p></article>`;
  const output=(id,plot=true)=>`<output id="${id}-result" aria-live="polite"></output>${plot?`<div id="${id}-plot"></div>`:''}`;
  const fields=body=>'<div class="public-fields">'+body+'</div>';
  const text=(x,y,s,anchor='start',color='#e3e9e2')=>`<text x="${x}" y="${y}" text-anchor="${anchor}" fill="${color}" font-size="17">${esc(s)}</text>`;
  const svg=(id,title,desc,body,h=350)=>`<svg class="public-plot" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 ${h}" role="img" aria-labelledby="${id}-title ${id}-desc"><title id="${id}-title">${esc(title)}</title><desc id="${id}-desc">${esc(desc)}</desc>${body}</svg>`;
  function bars(id,title,rows,note){return svg(id,title,'各列依相同比例尺呈現；數值與分母須一起閱讀。未定義不畫數值條。',text(25,35,title)+text(700,58,'共同尺度：0–100%','end','#aab9ae')+rows.map((r,i)=>{const y=75+i*70;return text(25,y+20,r[0])+(r[1]===null?'':`<rect x="240" y="${y}" width="460" height="25" fill="#28392e"/><rect x="240" y="${y}" width="${460*r[1]}" height="25" fill="${i%2?'#9ac8e8':'#b7e89f'}"/>`)+text(700,y+48,pct(r[1]),'end');}).join('')+text(25,75+rows.length*70,note),125+rows.length*70);}
  function curve(s){const max=Math.max(1,...s.counts);return svg('curve','同一份虛構清單，依不同日期分組','發病日未知的個案另列，不填成零或新增一個發病日期。',text(30,35,s.mode==='onset'?'依發病日：31件已知，另3件未知':'依通報日：34件（含發病日未知者）')+s.counts.map((n,i)=>`<rect x="${65+i*53}" y="${260-n/max*180}" width="35" height="${n/max*180}" fill="#9ac8e8"/>`+text(82+i*53,285,String(i+1),'middle')+text(82+i*53,250-n/max*180,String(n),'middle')).join('')+text(30,325,'橫軸為教學日；直條是個案數，不是發生率或即時疫情。'));}
  function sirPlot(m){const x=t=>65+t/Math.max(1,m.days)*630,y=n=>265-n/1000*200;return svg('sir','封閉人口的SIR教學模型','任意參數，沒有真實資料校準、預測區間或政策效果。',text(30,30,'人數：S可感染、I具傳染力、R移出；總數1000')+`<path d="M65 55V265H705" fill="none" stroke="#809789"/>`+[['s','#9ac8e8'],['i','#ead68c'],['r','#b7e89f']].map(([key,color])=>`<path d="${m.points.map((p,i)=>(i?'L':'M')+x(p.day).toFixed(2)+' '+y(p[key]).toFixed(2)).join(' ')}" stroke="${color}" stroke-width="3" fill="none"/>`).join('')+text(25,65,'1000')+text(35,270,'0')+text(65,305,'0日')+text(705,305,m.days+'日','end')+text(30,335,'S藍線 · I黃線 · R綠線；模型移出不等於一定死亡。'));}
  function screeningPlot(s){return svg('screen','預期人數的二乘二表','參照疾病為陽性；人數來自假設盛行率和測試表現，可能為非整數期望值。',`<path d="M25 65H735V270H25ZM255 65V270M500 65V270M25 115H735M25 192H735" fill="none" stroke="#81998b"/>`+text(30,35,'以參照疾病狀態為列，檢測結果為欄')+text(45,100,'參照狀態')+text(280,100,'檢測陽性')+text(520,100,'檢測陰性')+text(45,162,'有疾病')+text(280,162,'TP '+compact(s.tp))+text(520,162,'FN '+compact(s.fn))+text(45,240,'無疾病')+text(280,240,'FP '+compact(s.fp))+text(520,240,'TN '+compact(s.tn))+text(30,315,'預期人數；百萬以上以科學記號顯示，精確值見輸出。'));}
  function economicsPlot(m){const xx=380+Math.sign(m.de)*180,yy=170-Math.sign(m.dc)*100;return svg('economic','增量成本與效果：先看象限','各軸只表示正負方向，不是實際成本與效果的數值比例。',`<path d="M60 170H705M380 50V290" fill="none" stroke="#91a799"/><circle cx="${xx}" cy="${yy}" r="7" fill="#ead68c"/>`+text(395,45,'Δ成本正')+text(395,313,'Δ成本負')+text(60,155,'Δ效果負')+text(705,155,'Δ效果正','end')+text(30,340,'點位只呈現方向；精確差值與ICER見上方輸出。'));}
  window.renderCourseOverview=({course,saved,escapeHTML:e,main,toc,footer})=>{
    const link=n=>course.lessons[n-1].id,start=saved.last||link(1);
    main.innerHTML=`<section class="course-hero" id="intro"><div class="eyebrow">PUBLIC HEALTH & EPIDEMIOLOGY <span>／ 群體、證據與行動</span></div><h1>Health is shared<span class="hero-period">.</span></h1><h2 class="hero-subtitle">從群體差異，<br>走向可檢查的公共行動。</h2><p class="hero-description">從盛行、發生與人時，到研究設計、因果、監測和疫情調查；再走向篩檢、環境、健康公平、體系、政策與全球治理。用圖解看清分母，用案例連起證據與決策。</p><div class="hero-meta"><span><b>20</b> 章主線</span><span><b>120</b> 閱讀單元</span><span><b>60</b> 中文圖解</span><span><b>12</b> 互動學習活動</span></div><div class="hero-actions"><a class="primary-button" href="#${e(start)}">${saved.last?'繼續學習':'從人口健康開始'} ↗</a><a class="text-link" href="#overview/experiments">先看分母如何改變答案 ↓</a></div></section>
    <section id="quick-start" class="public-reading-note"><h2>完整學，也能從一個公共問題開始</h2><p>完整路線依20章前進。快速路線：<a href="#${link(1)}">人口健康</a> → <a href="#${link(9)}">人時與發生率</a> → <a href="#${link(26)}">相對與絕對關聯</a> → <a href="#${link(43)}">監測</a> → <a href="#${link(57)}">群聚調查</a> → <a href="#${link(101)}">政策與資源</a> → <a href="#${link(119)}">整合提案</a>。</p><p>必要統計與因果基礎在課內補足。每單元有原創圖、讀圖任務、情境、表格與可展開解析；核心學習不需寫程式。所有互動使用虛構或假設資料，分開示範數學、資料觀察與可支持的政策結論。</p></section>
    <section id="roadmap"><div class="section-header"><h2>完整學習路線</h2><span>20 CHAPTERS · 120 UNITS</span></div><div class="module-list">${course.groups.map(g=>`<a class="module-row" href="#${course.lessons.find(l=>l.group===g.id).id}"><span class="module-num">${g.number}</span><div><div class="module-name">${e(g.title)}</div><div class="module-description">${e(g.description)}</div></div><span class="module-count">6 UNITS ↗</span></a>`).join('')}</div></section>
    <section id="experiments"><div class="section-header"><h2>用情境與圖表練習</h2><span>12 ACTIVITIES · ORIGINAL CASES</span></div><p class="public-intro">先辨識人口、時間、分母和比較組，再操作數字。空白、零分母與未知各自處理，模型曲線與個人診斷或真實疫情預測分開。</p>
    ${lab(1,'同一社區，三種不同問題',fields(field('freq-pop','基線人口（人）',1000)+field('freq-existing','基線既有個案（人）',100)+field('freq-new','一年內首次新發個案（人）',45)+field('freq-time','實際無病人時（人年）',810,'.1'))+output('freq'),'一年封閉世代且發病／死亡結局均查明。預設810人年包含90人因其他原因死亡退出，詳見原創案例；5%是此情境的實際發病比例。更改輸入需有相符追蹤資料，不能由摘要表自動推算年底盛行率。')}
    ${lab(2,'世代二乘二表：RR、RD與OR',fields(field('cohort-a','曝露組發病 a',40)+field('cohort-b','曝露組未發病 b',160)+field('cohort-c','未曝露組發病 c',20)+field('cohort-d','未曝露組未發病 d',180))+output('cohort'),'此表指定相同追蹤期間的世代資料。病例對照抽樣改變列比例，不能直接拿表內風險當人口風險；OR也不普遍等於RR。')}
    ${lab(3,'年齡結構改變了什麼',fields(field('age-weight','共同標準人口：年輕層權重（0–1）',.8,'.05'))+output('age'),'虛構兩地、兩個年齡層與同一結果時段。共同權重是比較工具，標準化率不是當地實際負擔，也不是已識別的政策效果。')}
    ${lab(4,'Simpson悖論：先看分層，再看合併',fields(field('simpson-weight','兩組共同年輕層權重（0–1）',.5,'.05'))+output('simpson'),'這裡的結果是康復，不是上面的疾病個案。兩年齡層內E康復比例較低，但合併比例較高；重新加權展示組成影響，不保證已排除其他混雜。')}
    ${lab(5,'發病日、通報日與缺失',`<label for="curve-mode">日期欄位</label><select id="curve-mode"><option value="onset" selected>按發病日</option><option value="report">按通報日</option></select>`+output('curve')+fields(field('complete-present','另一份原創表的已填必要欄位',24)+field('complete-expected','應填必要欄位',30))+output('complete',false),'同一虛構清單共34件，3件發病日未知。欄位完整率24／30是另一個資料品質例子，不是個案偵測敏感度或疾病發生率。')}
    ${lab(6,'SIR：看懂模型，不把它當預報',fields(field('sir-beta','β傳播率參數（每日）',.3,'.05')+field('sir-gamma','γ移出率參數（每日）',.1,'.05')+field('sir-days','教學時間（整數日，最多180）',80))+output('sir'),'固定人口1000、初始S＝990、I＝10、R＝0，Euler步長0.1日。均質接觸、固定參數且無出生死亡或外來輸入；移出包含不再參與傳播的人，不專指死亡。')}
    ${lab(7,'疫苗：相對保護與絕對差距',fields(field('ve-vcase','接種組結果個案',20)+field('ve-vtotal','接種組人數',1000)+field('ve-ucase','未接種組結果個案',80)+field('ve-utotal','未接種組人數',1000))+output('ve'),'虛構相同終點與追蹤的比較；VE＝1−風險比。這是點估計示範，未加入信賴區間、混雜或真實疫苗產品資料。')}
    ${lab(8,'盛行率改變篩檢陽性的意義',fields(field('screen-n','受檢人數',10000)+field('screen-prev','參照疾病盛行率（0–1）',.01,'.01')+field('screen-sens','敏感度（0–1）',.9,'.01')+field('screen-spec','特異度（0–1）',.95,'.01'))+output('screen'),'表內為期望人數，輸入改動可產生非整數。參照標準、疾病譜與實施品質均可能影響真實表現；PPV不是整個篩檢計畫的健康效益。')}
    ${lab(9,'差距縮小，比值可能變大',fields(field('equity-worse','群體甲不良結果風險（0–1）',.2,'.01')+field('equity-better','群體乙不良結果風險（0–1）',.04,'.01'))+output('equity'),'固定基線甲40%、乙10%：絕對差30百分點、比值4。比較時保持群體標籤與不良結果定義，不依哪個指標較漂亮才選尺度。')}
    ${lab(10,'成本與效果：先辨象限',fields(field('econ-ca','方案A總成本（成本單位）',100000)+field('econ-ea','方案A總效果（QALY）',1000,'.1')+field('econ-cb','方案B總成本（成本單位）',120000)+field('econ-eb','方案B總效果（QALY）',1010,'.1'))+output('econ'),'假設同一族群、觀點、時間範圍及基準年。ICER以B−A計算；圖只示意差值正負，不給貨幣門檻，也不自動替代預算影響、公平和不確定性評估。')}
    ${lab(11,'同一場聚餐，先算攻擊比例',`<p>原創固定世代：吃食物A者18發病／12未發病；未吃者6發病／24未發病。試著比較兩組，再展開其他調查資訊。</p><button id="outbreak-reveal" class="secondary-button" aria-expanded="false">展開計算與下一步</button><div id="outbreak-analysis" hidden></div>`,'食品名稱、個案與資料皆為虛構。攻擊比例是特定期間的風險，不含人時；最大RR也不自動指出唯一污染來源。')}
    ${lab(12,'把公共宣稱改寫成可檢查的句子','<p id="quiz-count" class="mono"></p><h4 id="quiz-question"></h4><div id="quiz-options" class="public-choices"></div><output id="quiz-feedback" aria-live="polite">先選一個解釋，再讀理由。</output><div class="public-actions"><button id="quiz-next" class="secondary-button" disabled>下一題 →</button><button id="quiz-reset" class="secondary-button">重新開始</button></div>','12題原創概念自測，附原因與回顧提示；沒有個人風險或健康評分。')}</section>
    <section id="atlas" class="health-visual-index"><div class="section-header"><h2>全課圖解索引</h2><span>60 DIAGRAMS</span></div><label for="figure-filter">選擇章節</label><select id="figure-filter"><option value="all" selected>全部圖解</option>${course.groups.map(g=>`<option value="${e(g.id)}">${g.number} ${e(g.title)}</option>`).join('')}</select><p id="figure-count" aria-live="polite"></p><div id="figure-gallery" class="health-visual-grid"></div></section>
    <section id="downloads" class="public-reading-note"><h2>圖解、學習單與原創案例</h2><p>先標出人口、時間、分母和假設，再比較兩種解釋。學習包有圖、練習、解析、名詞與來源，可保留資料夾結構離線閱讀。</p><div class="public-actions"><a class="primary-button" href="${e(course.studyBundle)}" download>下載離線學習包 ↓</a><a class="text-link" href="study/workbook.md">120單元學習單 ↗</a><a class="text-link" href="study/answers.md">參考解析 ↗</a><a class="text-link" href="study/glossary.csv">中英名詞 ↗</a><a class="text-link" href="study/cases.json">原創案例資料 ↗</a></div></section>
    <section id="baseline" class="public-reading-note"><h2>版本、範圍與跨課閱讀</h2><p>2026-11-17核對WHO、CDC與臺灣官方資料，包括當時可用的疾病負擔、環境健康、體系與國際治理文件。資料年、出版年、正式修訂與查核日分開；即時疫情與個人醫療建議另按現行官方資訊取得。</p><p>IHR2024修正、各締約方適用版本，以及大流行協定與PABS程序分開說明。原創教學資料不對真實地區排名，也不把採納、批准與生效混稱；詳見<a href="study/sources.md">來源與版本索引</a>。</p><p>可跨課閱讀<a href="../evidence-health/index.html">實證健康與醫學研究判讀</a>、<a href="../applied-statistics/index.html">應用統計</a>、<a href="../economics/index.html">經濟學</a>及<a href="../metabolic-health/index.html">代謝健康</a>。本課仍提供獨立學習所需的定義與練習。</p></section>${footer}`;
    toc.innerHTML='<div class="toc-title">本頁內容</div><a href="#overview/intro">課程總覽</a><a href="#overview/quick-start">從問題開始</a><a href="#overview/roadmap">學習路線</a><a href="#overview/experiments">互動活動</a><a href="#overview/atlas">圖解索引</a><a href="#overview/downloads">離線學習包</a><a href="#overview/baseline">版本與來源</a>';
    const $=s=>main.querySelector(s),num=id=>{const node=$('#'+id);if(node.value.trim()==='')throw new RangeError('請填寫'+$('label[for="'+id+'"]').textContent);return Number(node.value);};
    const bind=(ids,prefix,calculate,describe,draw)=>{const run=()=>{const result=$('#'+prefix+'-result'),plot=$('#'+prefix+'-plot');try{const value=calculate();result.innerHTML=describe(value);result.dataset.status='ok';if(plot)plot.innerHTML=draw?draw(value):'';}catch(error){result.textContent=error.message;result.dataset.status='error';if(plot)plot.innerHTML='';}};for(const id of ids)$('#'+id).addEventListener('input',run);run();return run;};
    bind(['freq-pop','freq-existing','freq-new','freq-time'],'freq',()=>frequency(num('freq-pop'),num('freq-existing'),num('freq-new'),num('freq-time')),r=>`基線盛行率：${pct(r.prevalence)}；基線無病${fmt(r.atRisk)}人。<br>一年累積發生風險：${pct(r.risk)}；發生率：${fmt(r.rate)}／人年（${fmt(r.rate*100)}／100人年）。`,r=>bars('frequency','不同問題各自的分母',[['基線既有／人口',r.prevalence],['新發／基線無病',r.risk]],'人時率另有時間單位，不放在此百分比軸。'));
    bind(['cohort-a','cohort-b','cohort-c','cohort-d'],'cohort',()=>comparison(num('cohort-a'),num('cohort-b'),num('cohort-c'),num('cohort-d')),r=>`曝露風險${pct(r.riskE)}；未曝露風險${pct(r.riskU)}。<br>RR ${fmt(r.rr)}；RD ${r.rd===null?'未定義':fmt(r.rd*100)+'百分點'}；OR ${fmt(r.or)}。`,r=>bars('cohort','同追蹤期間的世代風險',[['曝露組',r.riskE],['未曝露組',r.riskU]],'空的風險集合列為未定義，不視為0%。（見上方）'));
    bind(['age-weight'],'age',()=>standardize(num('age-weight')),r=>`A粗率${pct(r.a.crude)}；B粗率${pct(r.b.crude)}。<br>共同權重${fmt(r.weights[0])}／${fmt(r.weights[1])}：A標準化${pct(r.a.adjusted)}；B標準化${pct(r.b.adjusted)}。`,r=>bars('age','相同年齡權重後比較',[['A標準化率',r.a.adjusted],['B標準化率',r.b.adjusted]],'權重不改變各地實際年齡層率或粗率。'));
    bind(['simpson-weight'],'simpson',()=>simpson(num('simpson-weight')),r=>`合併康復比例：E ${pct(r.e.crude)}，U ${pct(r.u.crude)}。<br>共同權重後：E ${pct(r.e.adjusted)}，U ${pct(r.u.adjusted)}；兩年齡層內E分別90%／60%，U為95%／70%。`,r=>bars('simpson','康復比例：比較組成與共同標準',[['E合併',r.e.crude],['U合併',r.u.crude],['E共同權重',r.e.adjusted],['U共同權重',r.u.adjusted]],'這裡的高低是康復結果，不是上一例的發病。'));
    const curveRun=()=>{const r=surveillance($('#curve-mode').value);$('#curve-result').textContent=`共${r.total}件；此日期欄位已知${r.known}件、未知${r.unknown}件。未知保留在圖外，沒有填成零。`;$('#curve-result').dataset.status='ok';$('#curve-plot').innerHTML=curve(r);};$('#curve-mode').addEventListener('change',curveRun);curveRun();
    bind(['complete-present','complete-expected'],'complete',()=>completeness(num('complete-present'),num('complete-expected')),r=>`已填${r.present}／應填${r.expected}；欄位完整率${pct(r.fraction)}。無應填欄位時未定義。`);
    bind(['sir-beta','sir-gamma','sir-days'],'sir',()=>sir(num('sir-beta'),num('sir-gamma'),num('sir-days')),r=>{const end=r.points.at(-1);return `模型R0 ${fmt(r.r0)}；初始Rt ${fmt(r.initialRt)}。<br>第${r.days}日：S ${fmt(end.s)}、I ${fmt(end.i)}、R ${fmt(end.r)}，合計${fmt(end.s+end.i+end.r)}。<br>均質理想免疫閾值：${r.immuneThreshold===null?'本例不提供':pct(r.immuneThreshold)}；不是通用接種覆蓋目標。`;},sirPlot);
    bind(['ve-vcase','ve-vtotal','ve-ucase','ve-utotal'],'ve',()=>vaccine(num('ve-vcase'),num('ve-vtotal'),num('ve-ucase'),num('ve-utotal')),r=>`接種組風險${pct(r.riskV)}；未接種組風險${pct(r.riskU)}。<br>VE ${pct(r.ve)}；絕對風險減少${r.arr===null?'未定義':fmt(r.arr*100)+'百分點'}。`,r=>bars('vaccine','特定結果與追蹤下的風險',[['接種組',r.riskV],['未接種組',r.riskU]],'VE點估計未提供不確定性或個別保護承諾。'));
    bind(['screen-n','screen-prev','screen-sens','screen-spec'],'screen',()=>screening(num('screen-n'),num('screen-prev'),num('screen-sens'),num('screen-spec')),r=>`PPV ${pct(r.ppv)}；NPV ${pct(r.npv)}。<br>預期檢測陽性${fmt(r.positive)}人，其中TP ${fmt(r.tp)}、FP ${fmt(r.fp)}；其餘FN ${fmt(r.fn)}、TN ${fmt(r.tn)}。`,screeningPlot);
    bind(['equity-worse','equity-better'],'equity',()=>equity(num('equity-worse'),num('equity-better')),r=>`固定基線：差30百分點、比值4。<br>目前甲−乙差${fmt(r.gap*100)}百分點，甲／乙比值${fmt(r.ratio)}。兩群體的絕對結果也要一起呈現。`,r=>bars('equity','同一不良結果：保留群體標籤',[['群體甲',r.worse],['群體乙',r.better]],'需要與基線、群體需求及公平目標一起解釋。'));
    bind(['econ-ca','econ-ea','econ-cb','econ-eb'],'econ',()=>economics(num('econ-ca'),num('econ-ea'),num('econ-cb'),num('econ-eb')),r=>`B−A：Δ成本${fmt(r.dc)}成本單位；Δ效果${fmt(r.de)} QALY。<br>ICER ${fmt(r.icer)}成本單位／QALY；${r.status}。`,economicsPlot);
    $('#outbreak-reveal').addEventListener('click',()=>{const open=$('#outbreak-analysis').hidden;$('#outbreak-analysis').hidden=!open;$('#outbreak-reveal').setAttribute('aria-expanded',String(open));if(open){const r=comparison(18,12,6,24);$('#outbreak-analysis').innerHTML=`<p>攻擊比例：${pct(r.riskE)} vs ${pct(r.riskU)}；RR ${fmt(r.rr)}、RD ${fmt(r.rd*100)}百分點、OR ${fmt(r.or)}。</p><p>接著核對發病時間、其他食物共食、個案與曝露定義、檢體及環境證據。還未提供的資料保留未知；可前往<a href="#${link(116)}">完整疫情調查專題</a>。</p>`;}});
    let question=0,answered=false;const showQuiz=()=>{const item=quiz(question);answered=false;$('#quiz-count').textContent=`${question+1} / ${QUIZ.length}`;$('#quiz-question').textContent=item.question;$('#quiz-feedback').textContent='先選一個解釋，再讀理由。';$('#quiz-next').disabled=true;$('#quiz-options').innerHTML=item.options.map((s,i)=>`<button class="secondary-button" data-choice="${i}" aria-pressed="false">${esc(s)}</button>`).join('');};
    $('#quiz-options').addEventListener('click',event=>{const b=event.target.closest('[data-choice]');if(!b)return;const item=quiz(question,Number(b.dataset.choice));answered=true;for(const other of $('#quiz-options').querySelectorAll('button'))other.setAttribute('aria-pressed',String(other===b));$('#quiz-feedback').textContent=(item.correct?'概念正確。':'再看一次條件。')+item.why;$('#quiz-next').disabled=question===QUIZ.length-1;});
    $('#quiz-next').addEventListener('click',()=>{if(answered&&question<QUIZ.length-1){question++;showQuiz();}});$('#quiz-reset').addEventListener('click',()=>{question=0;showQuiz();});showQuiz();
    const gallery=()=>{const selected=$('#figure-filter').value,figures=course.visuals.filter(f=>selected==='all'||f.group===selected);$('#figure-count').textContent=`顯示${figures.length}／60張原創圖；每張圖連到兩個不同讀圖任務。`;$('#figure-gallery').innerHTML=figures.map(f=>`<figure class="health-figure"><a href="${e(f.file)}" target="_blank" rel="noopener" aria-label="放大：${e(f.title)}"><img src="${e(f.file)}" alt="${e(f.description)}" width="860" height="520" loading="lazy"></a><figcaption><strong>${e(f.title)}</strong><p>${e(f.note)}</p>${f.lessons.map(id=>`<a class="text-link" href="#${e(id)}">${e(course.lessons.find(l=>l.id===id).title)} ↗</a>`).join(' · ')}</figcaption></figure>`).join('');};$('#figure-filter').addEventListener('change',gallery);gallery();
  };
  window.renderCourseOverview.courseSlug='public-health';
})();
