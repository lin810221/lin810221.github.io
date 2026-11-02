/* Original numerical teaching labs. JavaScript calculations, not a SciPy runtime. */
(() => {
  'use strict';
  const ink='#dcc7a3',blue='#9fd3db',purple='#c8afd6',fmt=x=>x===null?'未定義':Number(x.toFixed(4)).toString();
  function finite(x,min=1){if(x.length<min||x.some(v=>!Number.isFinite(v)))throw new RangeError('Finite observations required');}
  const mean=x=>x.reduce((a,b)=>a+b,0)/x.length;
  function quantile(values,p){finite(values);if(p<0||p>1)throw new RangeError('Probability required');const x=[...values].sort((a,b)=>a-b),i=(x.length-1)*p,a=Math.floor(i);return x[a]+(x[Math.min(a+1,x.length-1)]-x[a])*(i-a);}
  function describe(x){finite(x,2);const m=mean(x),variance=x.reduce((s,v)=>s+(v-m)**2,0)/(x.length-1);return {n:x.length,mean:m,median:quantile(x,.5),sd:Math.sqrt(variance),q1:quantile(x,.25),q3:quantile(x,.75)};}
  function histogram(values,bins,low,high){
    finite(values);if(!Number.isInteger(bins)||bins<1||!Number.isFinite(low)||!Number.isFinite(high)||low>=high||values.some(x=>x<low||x>high))throw new RangeError('Invalid histogram bounds');
    const counts=Array(bins).fill(0),width=(high-low)/bins;values.forEach(x=>counts[Math.min(bins-1,Math.floor((x-low)/width))]++);return {counts,width,density:counts.map(n=>n/(values.length*width))};
  }
  function binomial(n,p){
    if(!Number.isInteger(n)||n<1||n>100||!Number.isFinite(p)||p<0||p>1)throw new RangeError('Invalid binomial parameters');
    if(p===0)return Array.from({length:n+1},(_,k)=>k===0?1:0);if(p===1)return Array.from({length:n+1},(_,k)=>k===n?1:0);
    let choose=1;return Array.from({length:n+1},(_,k)=>{if(k)choose*= (n-k+1)/k;return choose*p**k*(1-p)**(n-k);});
  }
  function rng(seed){let state=seed>>>0;return ()=>{state=(Math.imul(state,1664525)+1013904223)>>>0;return (state+.5)/4294967296;};}
  function normalDraw(random){return Math.sqrt(-2*Math.log(random()))*Math.cos(2*Math.PI*random());}
  function sampling(n,repetitions=600){
    if(!Number.isInteger(n)||n<1||n>200||!Number.isInteger(repetitions)||repetitions<2)throw new RangeError('Invalid simulation size');
    const random=rng(117),means=Array.from({length:repetitions},()=>{let total=0;for(let i=0;i<n;i++)total-=Math.log(random());return total/n;});return {means,summary:describe(means),theoreticalSE:1/Math.sqrt(n)};
  }
  const pdf=x=>Math.exp(-x*x/2)/Math.sqrt(2*Math.PI);
  function cdf(x){
    if(x===Infinity)return 1;if(x===-Infinity)return 0;if(!Number.isFinite(x))throw new RangeError('Finite z required');if(x===0)return .5;
    const z=Math.abs(x),t=1/(1+.2316419*z),tail=pdf(z)*t*(.319381530+t*(-.356563782+t*(1.781477937+t*(-1.821255978+t*1.330274429))));return x>0?1-tail:tail;
  }
  function inverseNormal(p){if(!(p>0&&p<1))throw new RangeError('Probability strictly between zero and one required');let low=-10,high=10;for(let i=0;i<65;i++){const mid=(low+high)/2;if(cdf(mid)<p)low=mid;else high=mid;}return (low+high)/2;}
  function coverage(n,level,seed=19,repetitions=120){
    if(!Number.isInteger(n)||n<2||n>1000||!Number.isInteger(repetitions)||repetitions<1||!(level>0&&level<1))throw new RangeError('Invalid coverage design');
    const random=rng(seed),se=10/Math.sqrt(n),critical=inverseNormal((1+level)/2),half=critical*se;
    const intervals=Array.from({length:repetitions},()=>{const estimate=50+se*normalDraw(random);return {estimate,low:estimate-half,high:estimate+half,hit:Math.abs(estimate-50)<=half};});
    return {intervals,se,half,covered:intervals.filter(x=>x.hit).length,repetitions,level};
  }
  function power(n,delta,alpha=.05){
    if(!Number.isInteger(n)||n<1||!Number.isFinite(delta)||!(alpha>0&&alpha<1))throw new RangeError('Invalid known-sigma power design');
    const shift=delta*Math.sqrt(n),critical=inverseNormal(1-alpha/2);return {shift,critical,power:cdf(-critical-shift)+1-cdf(critical-shift)};
  }
  function anova(groups){
    if(groups.length<2)throw new RangeError('At least two groups required');groups.forEach(g=>finite(g,2));
    const all=groups.flat(),grand=mean(all),means=groups.map(mean),between=groups.reduce((s,g,i)=>s+g.length*(means[i]-grand)**2,0),within=groups.reduce((s,g,i)=>s+g.reduce((a,x)=>a+(x-means[i])**2,0),0),total=between+within;
    return {grand,means,between,within,total,dfBetween:groups.length-1,dfWithin:all.length-groups.length,F:within>0?(between/(groups.length-1))/(within/(all.length-groups.length)):null,eta:total?between/total:null};
  }
  function ols(x,y){
    finite(x,3);finite(y,3);if(x.length!==y.length)throw new RangeError('Matched pairs required');const mx=mean(x),my=mean(y),sxx=x.reduce((s,v)=>s+(v-mx)**2,0),syy=y.reduce((s,v)=>s+(v-my)**2,0),sxy=x.reduce((s,v,i)=>s+(v-mx)*(y[i]-my),0);
    if(!sxx)throw new RangeError('Predictor must vary');const slope=sxy/sxx,intercept=my-slope*mx,residuals=x.map((v,i)=>y[i]-intercept-slope*v),sse=residuals.reduce((s,e)=>s+e*e,0);
    return {slope,intercept,residuals,sse,r:syy?sxy/Math.sqrt(sxx*syy):null,r2:syy?1-sse/syy:null,slopeSE:Math.sqrt(sse/(x.length-2)/sxx)};
  }
  function alpha(items){
    if(items.length<3||!items[0]||items[0].length<2||items.some(r=>r.length!==items[0].length))throw new RangeError('Complete rectangular item matrix required');finite(items.flat());
    const k=items[0].length,totalVariance=describe(items.map(r=>r.reduce((a,b)=>a+b,0))).sd**2,itemVariances=Array.from({length:k},(_,j)=>describe(items.map(r=>r[j])).sd**2);
    return {value:totalVariance>0?k/(k-1)*(1-itemVariances.reduce((a,b)=>a+b,0)/totalVariance):null,totalVariance,itemVariances};
  }
  window.AppliedStatisticsLab={quantile,describe,histogram,binomial,sampling,cdf,inverseNormal,coverage,power,anova,ols,alpha};
  const slider=(id,name,min,max,step,value)=>`<label for="${id}">${name}<output id="${id}-value"></output><input id="${id}" type="range" min="${min}" max="${max}" step="${step}" value="${value}"></label>`;
  const stat=(name,id)=>`<div class="as-stat"><small>${name}</small><output id="${id}"></output></div>`;
  function lab(id,title,number,subtitle,intro,body,caption){return `<section id="${id}"><div class="section-header"><h2>${title}</h2><span>LAB ${number} · ${subtitle}</span></div><p class="as-intro">${intro}</p><div class="as-lab"><div class="as-lab-head"><span>${subtitle}</span><b>COMPUTE · OBSERVE · EXPLAIN</b></div><div class="as-body">${body}<p class="as-caption">${caption}</p></div></div></section>`;}
  function overview({course,saved,escapeHTML:e,main,toc,footer}){
    const last=saved.last||course.lessons[0].id;
    main.innerHTML=`<section id="intro" class="course-hero"><div class="eyebrow">THE APPLIED STATISTICS GUIDE <span>／ 從資料，到有依據的判斷</span></div><h1 class="as-title">Applied Statistics<span class="hero-period">.</span></h1><h2 class="hero-subtitle">看見資料中的差異，<br>也看清結論的不確定。</h2><p class="hero-description">依你的十章目錄，從圖表、量數與機率，走到區間、檢定、ANOVA、迴歸與問卷。每個方法都連著問題、條件、計算與解讀，讓軟體結果成為可以檢查的推理。</p><div class="hero-meta"><span><b>10</b> 章主線</span><span><b>70</b> 個閱讀單元</span><span><b>40</b> 份 Python 範例</span><span><b>8</b> 個互動實驗</span></div><div class="hero-actions"><a class="primary-button" href="#${last}">${saved.last?'繼續學習':'從緒論開始'} <span aria-hidden="true">↗</span></a><a class="text-link" href="#overview/coverage-lab">先看一次信賴區間 ↗</a></div><div class="as-path"><span>ASK</span><i>→</i><span>MEASURE</span><i>→</i><span>INFER</span><i>→</i><span>EXPLAIN</span></div></section>`+
    lab('description-lab','一個離群值，哪些量數先改變？','01','DESCRIBE','保留九筆數值，只拉動最後一筆。平均、中位、樣本SD與分箱會如何回應？',
      `<div class="as-controls">${slider('desc-last','最後一筆數值',8,40,1,9)}${slider('desc-bins','0–40 的等寬箱數',3,10,1,5)}</div><div id="desc-plot"></div><div class="as-stats">${stat('MEAN','desc-mean')}${stat('MEDIAN','desc-median')}${stat('SAMPLE SD','desc-sd')}</div><p id="desc-note" class="as-note" aria-live="polite"></p>`,
      '資料為 [2,3,4,4,5,6,7,8,最後一筆]；柱高為次數，最後箱包含右界40。直方圖和平均／中位垂線都由當下數值計算，沒有將旗標自動當成刪除規則。')+
    lab('binomial-lab','成功率與樣本數，如何改變次數分布？','02','BINOMIAL','固定獨立、同成功率的二元試驗模型，觀察成功次數與「至少 k 次」的機率。',
      `<div class="as-controls">${slider('bin-n','試驗次數 n',1,30,1,10)}${slider('bin-p','成功率 p',.05,.95,.05,.3)}${slider('bin-k','至少成功 k 次',0,10,1,4)}</div><div id="bin-plot"></div><div class="as-stats">${stat('E(X) = np','bin-mean')}${stat('SD(X)','bin-sd')}${stat('P(X ≥ k)','bin-tail')}</div><p class="as-note" id="bin-note" aria-live="polite"></p>`,
      '每個柱是精確二項公式的數值計算，選定尾端以淺藍顯示。這裡沒有把不放回抽樣或群集觀察當作獨立二項；相關差異見第4、5章。')+
    lab('sampling-lab','右偏資料的平均，會長成什麼形狀？','03','SAMPLING DISTRIBUTION','每次由均值1、SD1的指數母體抽 n 筆，取平均；反覆600次，畫出600個平均的分布。',
      `${slider('sampling-n','每份樣本的 n',1,100,1,1)}<div id="sampling-plot"></div><div class="as-stats">${stat('MEAN OF 600 MEANS','sampling-mean')}${stat('SIMULATED SE','sampling-se')}${stat('THEORETICAL 1/√n','sampling-theory')}</div><p class="as-note" id="sampling-note" aria-live="polite"></p>`,
      'JavaScript 使用固定seed的偽隨機模擬，每次都重算真實樣本平均。n與重複次數600不同；這只示範此指數母體，沒有宣稱n=30是所有分布的通關門檻。')+
    lab('coverage-lab','95%信賴，指的是哪個95%？','04','INTERVAL COVERAGE','真母體平均固定50、σ已知為10。反覆抽樣並建立平均的Z區間，看哪些區間包含同一個真值。',
      `<div class="as-controls">${slider('ci-n','每份樣本 n',5,200,5,25)}<label for="ci-level">中央雙側信賴水準<select id="ci-level"><option value=".95" selected>95%</option><option value=".90">90%</option><option value=".99">99%</option></select></label></div><div id="ci-plot"></div><div class="as-stats">${stat('COVERED / 120','ci-covered')}${stat('OBSERVED COVERAGE','ci-rate')}${stat('INTERVAL HALF-WIDTH','ci-width')}</div><div class="as-actions"><span>顯示120個區間中的前40個</span><button id="ci-redraw" class="secondary-button">換一組重複抽樣 ↻</button></div><p class="as-note" id="ci-note" aria-live="polite"></p>`,
      '正態母體下，直接由精確的樣本平均分布生成估計值，數學上等同抽n筆後取平均。共用相同標準化抽樣時，改n只縮放寬度，覆蓋比例不必改變；按鈕才換seed。它不是95%個別觀察的範圍。')+
    lab('power-lab','同樣的差異，樣本數如何影響檢定力？','05','ERRORS & POWER','雙側Z檢定、σ已知為1。橙線為H₀下的Z，淺藍為指定真差異下的Z；陰影是拒絕區中的替代分布。',
      `<div class="as-controls">${slider('power-n','樣本數 n',5,200,5,30)}${slider('power-delta','真差異 δ（原單位）',-1,1,.05,.5)}<label for="power-alpha">事前 α<select id="power-alpha"><option value=".05" selected>0.05</option><option value=".01">0.01</option><option value=".10">0.10</option></select></label></div><div id="power-plot"></div><div class="as-stats">${stat('CRITICAL |Z|','power-critical')}${stat('POWER = 1 − β','power-value')}${stat('β AT THIS δ','power-beta')}</div><p class="as-note" id="power-note" aria-live="polite"></p>`,
      '以標準常態CDF計算的理論power，數值近似誤差約10⁻⁷；不是未知σ的t檢定。δ=0時拒絕機率回到α。p值本身不是H₀為真的機率。')+
    lab('anova-lab','ANOVA 的 F，來自哪兩種變動？','06','SUMS OF SQUARES','三組各三筆，以共享組內尺度改變分散，並移動第二組平均。把平方和拆解與實際點圖一起看。',
      `<div class="as-controls">${slider('anova-middle','第二組平均',2,6,.1,4)}${slider('anova-spread','各組內偏差尺度',.5,3,.1,1)}</div><div id="anova-plot"></div><div class="as-stats">${stat('BETWEEN SS','anova-between')}${stat('WITHIN SS','anova-within')}${stat('F (df = 2, 6)','anova-f')}</div><p class="as-note" id="anova-note" aria-live="polite"></p>`,
      '各組為中心 + [−s,0,s]，中心依序2、可調、6；這是描述分解及傳統F算術，不是隨機取得的研究證據。η²是組間SS／總SS，不自動代表因果解釋比例。')+
    lab('regression-lab','一個點，能把迴歸線拉多遠？','07','CORRELATION & OLS','只移動最後一個 y，重新計算最小平方線、殘差與相關。實線是擬合，虛線是各筆殘差。',
      `${slider('reg-last','x = 8 時的最後一筆 y',2,24,.5,11)}<div id="reg-plot"></div><div class="as-stats">${stat('SLOPE b₁','reg-slope')}${stat('PEARSON r','reg-r')}${stat('R²','reg-r2')}</div><p class="as-note" id="reg-note" aria-live="polite"></p>`,
      '固定八對資料，含截距OLS。畫面顯示樣本內擬合，沒有宣稱因果、外部預測或模型假設成立；完整係數與預測區間見第9章。')+
    lab('reliability-lab','反向題沒轉回來，alpha 會如何變？','08','QUESTIONNAIRE SCORING','六位虛構填答者、三題1–5。第三題是反向題，切換計分再核對總分變異與alpha。',
      `<div class="as-controls"><label for="alpha-reverse" class="as-check"><input id="alpha-reverse" type="checkbox"> 依規則將第三題轉為 6 − 原值</label>${slider('alpha-last','最後一位的第二題',1,5,1,4)}</div><div id="alpha-table"></div><div class="as-stats">${stat('CRONBACH α','alpha-value')}${stat('TOTAL SCORE VARIANCE','alpha-total')}${stat('SUM ITEM VARIANCES','alpha-items')}</div><p class="as-note" id="alpha-note" aria-live="polite"></p>`,
      '使用樣本variance的原始alpha公式，不將負alpha裁成0。這六人只為算術示意；高alpha不證明單因子、效度或代表性，正式合成CSV示範在第10章。')+
    `<section id="roadmap"><div class="section-header"><h2>十章主線，保留你的學習脈絡</h2><span>10 CHAPTERS + APPENDICES</span></div><div class="module-list">${course.groups.map(g=>{const lessons=course.lessons.filter(l=>l.group===g.id);return `<a class="module-row" href="#${lessons[0].id}"><span class="module-num">${e(g.number)}</span><div><div class="module-name">${e(g.title)}</div><div class="module-description">${e(g.description)}</div></div><span class="module-count">${lessons.length} UNITS ↗</span></a>`;}).join('')}</div></section><div class="reading-note" id="before-start"><strong>開始之前</strong><br>適合從零建立統計基礎、希望能讀懂資料分析結果的讀者。原節號保留，每章有習題解答；第十章使用Python，不含SPSS操作。<br>2026-11-02查核SciPy1.18.1與statsmodels0.15.0，Python3.13實測60項測試；全部範例使用自製資料，安裝後離線執行。<br>八個實驗在瀏覽器以JavaScript計算，並非SciPy執行環境。進度與筆記儲存在目前瀏覽器。</div><p class="as-bridge"><a href="examples.zip" download>下載40份Python範例與完整問卷資料 ↗</a> · <a href="examples/README.md">安裝與資料字典</a><br>搭配 <a href="../machine-learning/index.html">機器學習</a> 理解預測與選模；機率論與數理統計仍保留各自獨立課程。</p>${footer}`;
    const links=[['intro','課程介紹'],['description-lab','量數與離群值'],['binomial-lab','二項分配'],['sampling-lab','抽樣分配'],['coverage-lab','信賴區間覆蓋'],['power-lab','型I／II與檢定力'],['anova-lab','ANOVA分解'],['regression-lab','相關與迴歸'],['reliability-lab','反向題與alpha'],['roadmap','完整十章目錄'],['before-start','版本與閱讀方式']];
    toc.innerHTML=`<h2 class="toc-label">本頁導覽</h2><div class="toc-links">${links.map(([id,title])=>`<a href="#overview/${id}">${title}</a>`).join('')}</div><div class="toc-tip"><p>先問什麼，再決定怎麼算。</p><p><kbd>Ctrl</kbd> + <kbd>K</kbd> 搜尋全部單元</p></div>`;mount(main);
  }
  function chart(content,label){return `<svg class="as-plot" viewBox="0 0 560 285" role="img" aria-label="${label}"><title>${label}</title>${content}</svg>`;}
  function bars(h,low,high,label,lines=[]){
    const maximum=Math.max(1,...h.counts),width=470/h.counts.length,x=v=>50+(v-low)*470/(high-low),y=v=>240-v*210/maximum;
    return chart(`<path d="M50 25V240H520" stroke="#536050"/>${h.counts.map((n,i)=>`<rect x="${50+i*width+1}" y="${y(n)}" width="${Math.max(1,width-2)}" height="${240-y(n)}" fill="${ink}" fill-opacity=".5"/>`).join('')}${[0,maximum].map(v=>`<text x="8" y="${y(v)+4}">${fmt(v)}</text>`).join('')}${[low,(low+high)/2,high].map(v=>`<text x="${x(v)-8}" y="262">${fmt(v)}</text>`).join('')}${lines.map(l=>`<path d="M${x(l.value)} 22V240" stroke="${l.color}" stroke-width="2" stroke-dasharray="4 4"/>`).join('')}`,label);
  }
  function mount(main){
    const q=s=>main.querySelector(s),value=id=>Number(q('#'+id).value),out=(id,v)=>{q('#'+id).textContent=v;};
    function drawDescription(){
      const last=value('desc-last'),bins=value('desc-bins'),values=[2,3,4,4,5,6,7,8,last],d=describe(values),h=histogram(values,bins,0,40);
      out('desc-last-value',last);out('desc-bins-value',bins);out('desc-mean',fmt(d.mean));out('desc-median',fmt(d.median));out('desc-sd',fmt(d.sd));
      q('#desc-plot').innerHTML=bars(h,0,40,'九筆資料的次數直方圖，橙色平均與藍色中位',[{value:d.mean,color:ink},{value:d.median,color:blue}]);out('desc-note',`九筆值：${values.join(', ')}。平均（橙線）${fmt(d.mean)}，中位（藍線）${fmt(d.median)}。分位採linear插值，IQR = ${fmt(d.q3-d.q1)}；所有箱的次數和仍為9。`);
    }
    function drawBinomial(){
      const n=value('bin-n'),p=value('bin-p');q('#bin-k').max=String(n);if(value('bin-k')>n)q('#bin-k').value=String(n);const k=value('bin-k'),weights=binomial(n,p),maximum=Math.max(...weights),w=470/(n+1),y=v=>240-210*v/maximum;
      out('bin-n-value',n);out('bin-p-value',fmt(p));out('bin-k-value',k);out('bin-mean',fmt(n*p));out('bin-sd',fmt(Math.sqrt(n*p*(1-p))));out('bin-tail',fmt(weights.slice(k).reduce((a,b)=>a+b,0)));
      q('#bin-plot').innerHTML=chart(`<path d="M45 25V240H525" stroke="#536050"/>${weights.map((v,i)=>`<rect x="${50+i*w}" y="${y(v)}" width="${Math.max(2,w-2)}" height="${240-y(v)}" fill="${i>=k?blue:ink}" fill-opacity=".7"/>`).join('')}<text x="8" y="28">${fmt(maximum)}</text><text x="50" y="263">0</text><text x="500" y="263">${n} 次</text>`,'二項成功次數分布與選定右尾');out('bin-note',`P(X ≥ ${k}) 含 ${k} 本身；全部 ${n+1} 個機率加總為 ${fmt(weights.reduce((a,b)=>a+b,0))}。`);
    }
    function drawSampling(){
      const n=value('sampling-n'),a=sampling(n),low=Math.min(...a.means),high=Math.max(...a.means),h=histogram(a.means,24,low,high);
      out('sampling-n-value',n);out('sampling-mean',fmt(a.summary.mean));out('sampling-se',fmt(a.summary.sd));out('sampling-theory',fmt(a.theoreticalSE));q('#sampling-plot').innerHTML=bars(h,low,high,'指數母體的600次樣本平均分布',[{value:1,color:blue}]);out('sampling-note',`每份樣本 ${n} 筆，共600份；圖中每一筆是一個平均。藍線為固定母體均值1，橫軸依此批平均範圍自動縮放，請一併看尺度與SE。`);
    }
    let ciSeed=19;
    function drawCoverage(){
      const n=value('ci-n'),level=value('ci-level'),a=coverage(n,level,ciSeed),extent=Math.max(10,a.half*1.8),x=v=>50+(v-(50-extent))*470/(2*extent);
      out('ci-n-value',n);out('ci-covered',`${a.covered} / ${a.repetitions}`);out('ci-rate',(100*a.covered/a.repetitions).toFixed(1)+'%');out('ci-width',fmt(a.half));
      q('#ci-plot').innerHTML=chart(`<defs><clipPath id="as-ci-clip"><rect x="50" y="10" width="470" height="245"/></clipPath></defs><path d="M${x(50)} 10V253" stroke="${blue}" stroke-dasharray="4 4"/><g clip-path="url(#as-ci-clip)">${a.intervals.slice(0,40).map((v,i)=>{const y=14+i*6;return `<path d="M${x(v.low)} ${y}H${x(v.high)}" stroke="${v.hit?ink:purple}" stroke-width="1.5"/><circle cx="${x(v.estimate)}" cy="${y}" r="1.8" fill="${v.hit?ink:purple}"/>`;}).join('')}</g><text x="50" y="276">${fmt(50-extent)}</text><text x="265" y="276">μ = 50</text><text x="485" y="276">${fmt(50+extent)}</text>`,'前40個平均信賴區間與固定母體均值50');out('ci-note',`橙色區間包含真μ，紫色未包含；統計涵蓋全部120次，不只圖上40次。SE = ${fmt(a.se)}。有限120次的實際比例不必恰好等於 ${(100*level).toFixed(0)}%。`);
    }
    function drawPower(){
      const n=value('power-n'),delta=value('power-delta'),alpha0=value('power-alpha'),a=power(n,delta,alpha0),extent=Math.max(4.5,Math.abs(a.shift)+4),x=v=>50+(v+extent)*470/(2*extent),y=v=>240-v*500;
      const curve=m=>Array.from({length:241},(_,i)=>{const z=-extent+i*2*extent/240;return [z,pdf(z-m)];}),path=points=>points.map((p,i)=>`${i?'L':'M'}${x(p[0])} ${y(p[1])}`).join(' ');
      const alternative=curve(a.shift),tails=[alternative.filter(p=>p[0]<=-a.critical),alternative.filter(p=>p[0]>=a.critical)].filter(p=>p.length>1);
      q('#power-plot').innerHTML=chart(`<path d="M50 240H520" stroke="#536050"/>${tails.map(p=>`<path d="M${x(p[0][0])} 240 ${path(p).replace(/^M/,'L')} L${x(p[p.length-1][0])} 240Z" fill="${blue}" fill-opacity=".18"/>`).join('')}<path d="${path(curve(0))}" stroke="${ink}" stroke-width="2" fill="none"/><path d="${path(alternative)}" stroke="${blue}" stroke-width="2" fill="none"/>${[-a.critical,a.critical].map(z=>`<path d="M${x(z)} 30V240" stroke="${purple}" stroke-dasharray="3 4"/>`).join('')}<text x="50" y="266">${fmt(-extent)}</text><text x="${x(0)-4}" y="266">0</text><text x="475" y="266">${fmt(extent)}</text>`,'虛無與指定替代下的Z分布及雙側拒絕區');
      out('power-n-value',n);out('power-delta-value',fmt(delta));out('power-critical',fmt(a.critical));out('power-value',(a.power*100).toFixed(1)+'%');out('power-beta',((1-a.power)*100).toFixed(1)+'%');out('power-note',`H₀真時型I錯誤率為事前 α = ${alpha0}。在指定 δ = ${fmt(delta)} 下，Z均值偏移 ${fmt(a.shift)}，power才是目前顯示的數值。`);
    }
    function drawAnova(){
      const center=value('anova-middle'),spread=value('anova-spread'),groups=[2,center,6].map(m=>[-spread,0,spread].map(d=>m+d)),a=anova(groups),x=i=>130+i*150,y=v=>245-(v+1)*24;
      out('anova-middle-value',fmt(center));out('anova-spread-value',fmt(spread));out('anova-between',fmt(a.between));out('anova-within',fmt(a.within));out('anova-f',fmt(a.F));
      q('#anova-plot').innerHTML=chart(`<path d="M50 ${y(a.grand)}H520" stroke="${blue}" stroke-dasharray="4 4"/>${groups.map((g,i)=>`<path d="M${x(i)-22} ${y(mean(g))}H${x(i)+22}" stroke="${ink}" stroke-width="3"/>${g.map((v,j)=>`<circle cx="${x(i)+(j-1)*12}" cy="${y(v)}" r="5" fill="${ink}" fill-opacity=".7"/>`).join('')}<text x="${x(i)-12}" y="269">G${i+1}</text>`).join('')}<text x="10" y="25">y</text>`,'三組觀察點、組平均及整體平均');out('anova-note',`SS總 = ${fmt(a.total)} = ${fmt(a.between)} + ${fmt(a.within)}；df總8 = 2 + 6。η² = ${fmt(a.eta)}。藍色虛線為總平均 ${fmt(a.grand)}。`);
    }
    function drawRegression(){
      const x=[1,2,3,4,5,6,7,8],y=[2,3,5,4,7,8,8,value('reg-last')],a=ols(x,y),sx=v=>50+(v-1)*470/7,sy=v=>240-v*8;
      out('reg-last-value',fmt(y[7]));out('reg-slope',fmt(a.slope));out('reg-r',fmt(a.r));out('reg-r2',fmt(a.r2));
      q('#reg-plot').innerHTML=chart(`<path d="M50 25V240H520" stroke="#536050"/><path d="M${sx(1)} ${sy(a.intercept+a.slope)}L${sx(8)} ${sy(a.intercept+a.slope*8)}" stroke="${ink}" stroke-width="2"/>${x.map((v,i)=>`<path d="M${sx(v)} ${sy(y[i])}V${sy(a.intercept+a.slope*v)}" stroke="${blue}" stroke-dasharray="3 4"/><circle cx="${sx(v)}" cy="${sy(y[i])}" r="5" fill="${i===7?ink:blue}"/>`).join('')}<text x="50" y="265">1</text><text x="510" y="265">8</text><text x="10" y="25">y</text>`,'八筆成對資料的OLS線與殘差');out('reg-note',`ŷ = ${fmt(a.intercept)} + ${fmt(a.slope)}x；SSE = ${fmt(a.sse)}，斜率的傳統SE = ${fmt(a.slopeSE)}。只有最後一筆y改變，模型仍會重新調整全部預測。`);
    }
    function drawAlpha(){
      const original=[[1,1,5],[1,2,4],[2,2,4],[4,4,2],[4,5,1],[5,value('alpha-last'),1]],reverse=q('#alpha-reverse').checked,items=original.map(r=>[r[0],r[1],reverse?6-r[2]:r[2]]),a=alpha(items);
      out('alpha-last-value',value('alpha-last'));out('alpha-value',fmt(a.value));out('alpha-total',fmt(a.totalVariance));out('alpha-items',fmt(a.itemVariances.reduce((a,b)=>a+b,0)));
      q('#alpha-table').innerHTML=`<div class="as-table-wrap"><table class="as-table"><thead><tr><th>人</th><th>Q1</th><th>Q2</th><th>Q3原值</th><th>Q3計分</th><th>總分</th></tr></thead><tbody>${items.map((row,i)=>`<tr><th>${i+1}</th><td>${row[0]}</td><td>${row[1]}</td><td>${original[i][2]}</td><td>${row[2]}</td><td>${row.reduce((a,b)=>a+b,0)}</td></tr>`).join('')}</tbody></table></div>`;out('alpha-note',reverse?'已統一題目方向。alpha描述此資料的內部一致性；即使很高，也不能證明內容、效度或單因子。':'第三題尚未反向，與前兩題方向相反。先依量表規則正確計分，再討論內部一致性。');
    }
    const bind=(ids,fn,event='input')=>ids.forEach(id=>q('#'+id).addEventListener(event,fn));
    bind(['desc-last','desc-bins'],drawDescription);bind(['bin-n','bin-p','bin-k'],drawBinomial);bind(['sampling-n'],drawSampling);bind(['ci-n'],drawCoverage);bind(['ci-level'],drawCoverage,'change');q('#ci-redraw').addEventListener('click',()=>{ciSeed+=7;drawCoverage();});
    bind(['power-n','power-delta'],drawPower);bind(['power-alpha'],drawPower,'change');bind(['anova-middle','anova-spread'],drawAnova);bind(['reg-last'],drawRegression);bind(['alpha-last'],drawAlpha);bind(['alpha-reverse'],drawAlpha,'change');
    drawDescription();drawBinomial();drawSampling();drawCoverage();drawPower();drawAnova();drawRegression();drawAlpha();
  }
  overview.courseSlug='applied-statistics';window.renderCourseOverview=overview;
})();
