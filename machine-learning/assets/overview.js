/* Original deterministic numerical labs. Browser uses JS, not scikit-learn. */
(() => {
  'use strict';
  const f=value=>value===null?'—':Number(value.toFixed(4)).toString();
  const palette=['#9fd3db','#e5c185','#c8afd6'];
  const regressionPoints=[[-3,-4.6],[-2,-3.2],[-1,-1.4],[0,1.4],[1,2.6],[2,4.8],[3,7.4]];
  const labels=[1,0,1,0,1,0,0,1],scores=[.95,.85,.7,.6,.55,.35,.2,.4];
  const featureValues=Array.from({length:20},(_,i)=>i<16?i:i+24);
  const treeRows=Array.from({length:8},(_,i)=>({x:i+1,y:[0,0,0,1,0,1,1,1][i]}));
  const clusterPoints=[[-3,-2.2],[-2.5,-1.8],[-3.2,-1.4],[-2.4,-2.5],[-.2,2.7],[.4,3.1],[-.5,3.3],[.2,2.3],[2.8,-1.5],[3.4,-2],[2.5,-2.5],[3.3,-2.8]];
  function finite(values){if(!values.length||values.some(v=>!Number.isFinite(v)))throw new RangeError('Finite nonempty values required');}
  function regression(points,w,b){
    finite([w,b,...points.flat()]);if(points.length<2)throw new RangeError('At least two points');
    const mean=points.reduce((s,p)=>s+p[1],0)/points.length,sse=points.reduce((s,[x,y])=>s+(w*x+b-y)**2,0),variance=points.reduce((s,p)=>s+(p[1]-mean)**2,0);
    return {mse:sse/points.length,mae:points.reduce((s,[x,y])=>s+Math.abs(w*x+b-y),0)/points.length,r2:variance?1-sse/variance:null};
  }
  function ols(points){
    finite(points.flat());if(points.length<2)throw new RangeError('At least two points');
    const mx=points.reduce((s,p)=>s+p[0],0)/points.length,my=points.reduce((s,p)=>s+p[1],0)/points.length,den=points.reduce((s,p)=>s+(p[0]-mx)**2,0);
    if(!den)throw new RangeError('Feature has no variation');
    const w=points.reduce((s,p)=>s+(p[0]-mx)*(p[1]-my),0)/den;return {w,b:my-w*mx};
  }
  function metrics(y,p,t,fnCost=5,fpCost=1){
    finite([...p,t,fnCost,fpCost]);if(y.length!==p.length||!y.length||y.some(v=>v!==0&&v!==1)||p.some(v=>v<0||v>1)||fnCost<0||fpCost<0)throw new RangeError('Invalid labels, scores or costs');
    let tp=0,fp=0,fn=0,tn=0;y.forEach((v,i)=>{const positive=p[i]>=t;if(v&&positive)tp++;else if(positive)fp++;else if(v)fn++;else tn++;});
    return {tp,fp,fn,tn,precision:tp+fp?tp/(tp+fp):0,recall:tp+fn?tp/(tp+fn):0,cost:fn*fnCost+fp*fpCost};
  }
  function bestThreshold(y,p,fnCost,fpCost){
    const candidates=[...new Set([0,...p,1.01])].sort((a,b)=>a-b);let best=null;
    for(const threshold of candidates){const r=metrics(y,p,threshold,fnCost,fpCost);if(best===null||r.cost<best.cost)best={threshold,cost:r.cost};}return best;
  }
  function foldStats(values,fold,leaked=false){
    finite(values);if(values.length%5||!Number.isInteger(fold)||fold<0||fold>=5)throw new RangeError('Five equal folds required');
    const width=values.length/5,validation=values.map((_,i)=>i).filter(i=>Math.floor(i/width)===fold),train=values.map((_,i)=>i).filter(i=>!validation.includes(i)),fit=leaked?values.map((_,i)=>i):train;
    const mean=fit.reduce((s,i)=>s+values[i],0)/fit.length,scale=Math.sqrt(fit.reduce((s,i)=>s+(values[i]-mean)**2,0)/fit.length)||1;
    return {train,validation,fit,mean,scale,validationMeanZ:validation.reduce((s,i)=>s+(values[i]-mean)/scale,0)/validation.length};
  }
  function gini(y){if(!y.length)return 0;if(y.some(v=>v!==0&&v!==1))throw new RangeError('Binary labels required');const p=y.reduce((a,b)=>a+b,0)/y.length;return 2*p*(1-p);}
  function split(rows,threshold){
    if(!rows.length)throw new RangeError('Rows required');
    finite([threshold,...rows.map(r=>r.x)]);const left=rows.filter(r=>r.x<=threshold),right=rows.filter(r=>r.x>threshold),parent=gini(rows.map(r=>r.y)),weighted=(left.length*gini(left.map(r=>r.y))+right.length*gini(right.map(r=>r.y)))/rows.length;
    return {left,right,parent,weighted,gain:left.length&&right.length?parent-weighted:null};
  }
  const distance=(a,b)=>(a[0]-b[0])**2+(a[1]-b[1])**2;
  function assign(points,centers){if(!centers.length)throw new RangeError('Centers required');finite([...points.flat(),...centers.flat()]);return points.map(p=>centers.reduce((best,c,i)=>distance(p,c)<distance(p,centers[best])?i:best,0));}
  const inertia=(points,centers,assignment)=>points.reduce((s,p,i)=>s+distance(p,centers[assignment[i]]),0);
  function lloyd(points,centers){
    const assignment=assign(points,centers),counts=centers.map((_,k)=>assignment.filter(label=>label===k).length);
    const next=centers.map((center,k)=>counts[k]?[0,1].map(axis=>points.reduce((s,p,i)=>s+(assignment[i]===k?p[axis]:0),0)/counts[k]):[...center]);
    return {centers:next,assignment,counts,inertia:inertia(points,next,assignment),changed:next.some((p,i)=>distance(p,centers[i])>1e-16)};
  }
  window.MachineLearningLab={regression,ols,metrics,bestThreshold,foldStats,gini,split,assign,lloyd,inertia};
  const stat=(name,id)=>`<div class="ml-stat"><small>${name}</small><output id="${id}"></output></div>`;
  const slider=(id,name,min,max,step,value)=>`<label for="${id}">${name}<output id="${id}-value"></output><input id="${id}" type="range" min="${min}" max="${max}" step="${step}" value="${value}"></label>`;
  function overview({course,saved,escapeHTML:e,main,toc,footer}){
    const last=saved.last||course.lessons[0].id;
    main.innerHTML=`<section class="course-hero" id="intro"><div class="eyebrow">THE COMPLETE MACHINE LEARNING GUIDE <span>／ 從資料到可靠預測</span></div><h1 class="ml-title">Machine Learning<span class="hero-period">.</span></h1><h2 class="hero-subtitle">讓資料學出規則，<br>也讓結果經得起檢驗。</h2><p class="hero-description">從第一個預測問題，走進回歸、分類、樹與集成，再探索沒有標籤的資料。親手建立完整流程，學會問出分數背後更重要的問題。</p><div class="hero-meta"><span><b>60</b> 個完整章節</span><span><b>30</b> 份 Python 範例</span><span><b>5</b> 個互動實驗室</span><span><b>1.9.1</b> scikit-learn</span></div><div class="hero-actions"><a class="primary-button" href="#${last}">${saved.last?'繼續學習':'從第一章開始'} <span aria-hidden="true">→</span></a><a class="text-link" href="#overview/regression-lab">先親手調整一個模型 ↓</a></div><div class="ml-path"><span>DEFINE</span><i>→</i><span>LEARN</span><i>→</i><span>VALIDATE</span><i>→</i><span>DELIVER</span></div></section>
    <section id="regression-lab"><div class="section-header"><h2>一條線，如何接近資料？</h2><span>LAB 01 · REGRESSION</span></div><p class="ml-intro">調整權重與偏移，看殘差、MSE 與 MAE 如何改變；再用最小平方法求出這七個點的最佳直線。</p><div class="ml-lab"><div class="ml-lab-head"><span>ŷ = w·x + b</span><b>HANDMADE DATA</b></div><div class="ml-body"><div class="ml-controls">${slider('reg-w','斜率 w',-1,4,.01,.5)}${slider('reg-b','偏移 b',-2,3,.01,0)}</div><div id="reg-plot"></div><div class="ml-stats">${stat('MEAN SQUARED ERROR','reg-mse')}${stat('MEAN ABSOLUTE ERROR','reg-mae')}${stat('R²','reg-r2')}</div><div class="ml-actions"><span class="mono">虛線為每一筆的垂直殘差</span><button id="reg-fit" class="secondary-button">套用最小平方法 →</button></div><p id="reg-note" class="ml-note"></p><p class="ml-caption">瀏覽器直接計算單變數最小平方解；資料為自訂數字，不是現實任務成績。Python 對照在第 13、27 章。</p></div></div></section>
    <section id="threshold-lab"><div class="section-header"><h2>哪個門檻，符合你的成本？</h2><span>LAB 02 · DECISIONS</span></div><p class="ml-intro">八筆手工驗證分數，改變門檻與漏報成本。precision、recall 與總成本，可能指向不同選擇。</p><div class="ml-lab"><div class="ml-lab-head"><span>COST = c_FN × FN + 1 × FP</span><b>FIXED VALIDATION SCORES</b></div><div class="ml-body"><div class="ml-controls">${slider('decision-threshold','接受門檻',0,1.01,.01,.5)}${slider('decision-fn','漏掉正例的單筆成本',1,10,1,5)}</div><div id="decision-rows" class="ml-score-grid"></div><div id="decision-confusion" class="ml-confusion" aria-live="polite"></div><div class="ml-stats">${stat('PRECISION','decision-precision')}${stat('RECALL','decision-recall')}${stat('TOTAL COST','decision-cost')}</div><div class="ml-actions"><span class="mono">FP 單筆成本固定為 1</span><button id="decision-optimize" class="secondary-button">依這組驗證資料選最低成本 →</button></div><p id="decision-note" class="ml-note"></p><p class="ml-caption">只調整決策，未重新訓練模型。真實專案以 validation／內部 CV 選門檻，再做 final test；第 31–33 章完整說明。</p></div></div></section>
    <section id="cv-lab"><div class="section-header"><h2>這一折，scaler 看過哪些資料？</h2><span>LAB 03 · LEAKAGE</span></div><p class="ml-intro">五折、二十筆特徵。最後四筆刻意有分布偏移，切換正確與洩漏流程，直接檢查 fit 統計的差異。</p><div class="ml-lab"><div class="ml-lab-head"><span>FIT ON TRAIN · TRANSFORM VALIDATION</span><b>5 FOLDS</b></div><div class="ml-body"><div class="ml-controls">${slider('cv-fold','目前驗證折',1,5,1,5)}<label for="cv-policy">前處理政策<select id="cv-policy"><option value="safe" selected>只在這一折 train fit</option><option value="leaked">錯誤：先用全資料 fit</option></select></label></div><div class="ml-key"><span><b>青色</b> train</span><span><b class="validation-key">金色</b> validation</span><span>虛線：validation 也被拿來 fit</span></div><div id="cv-rows" class="ml-folds"></div><div class="ml-stats">${stat('ROWS USED TO FIT','cv-count')}${stat('FITTED MEAN','cv-mean')}${stat('VAL MEAN AFTER SCALING','cv-zmean')}</div><div id="cv-pipeline" class="ml-pipeline"></div><p id="cv-note" class="ml-note"></p><p class="ml-caption">這個實驗只算前處理統計，沒有訓練分類器或杜撰樂觀分數。將整條 Pipeline 交給 CV，才能讓每折重新 fit；見第 8、28 章。</p></div></div></section>
    <section id="tree-lab"><div class="section-header"><h2>一個分裂，改善了多少？</h2><span>LAB 04 · DECISION TREES</span></div><p class="ml-intro">八筆樣本、兩種類別。移動切點，按左右樣本數加權 Gini，觀察貪婪分裂的依據。</p><div class="ml-lab"><div class="ml-lab-head"><span>WEIGHTED GINI REDUCTION</span><b>ONE SPLIT</b></div><div class="ml-body">${slider('tree-threshold','左分支條件：x ≤ threshold',1.5,7.5,1,3.5)}<div id="tree-plot" style="margin-top:20px"></div><div class="ml-stats">${stat('PARENT GINI','tree-parent')}${stat('WEIGHTED CHILD GINI','tree-weighted')}${stat('GINI REDUCTION','tree-gain')}</div><div id="tree-root" class="ml-tree-root"></div><div id="tree-children" class="ml-tree-children"></div><p id="tree-note" class="ml-note"></p><p class="ml-caption">這裡計算固定樣本的一層分裂，沒有建立完整 sklearn 樹。實際模型與剪枝在第 21、22 章。</p></div></div></section>
    <section id="cluster-lab"><div class="section-header"><h2>沒有答案，中心如何移動？</h2><span>LAB 05 · KMEANS</span></div><p class="ml-intro">每一步先指派最近中心，再移到群內平均。比較群數與初始位置，看看目標值下降是否等於唯一答案。</p><div class="ml-lab"><div class="ml-lab-head"><span>ASSIGN → UPDATE → REPEAT</span><b>LLOYD ITERATIONS</b></div><div class="ml-body"><div class="ml-controls"><label for="cluster-k">中心數 K<select id="cluster-k"><option value="3" selected>3 個中心</option><option value="2">2 個中心</option></select></label><label for="cluster-init">初始位置<select id="cluster-init"><option value="spread" selected>分散的初始位置</option><option value="crowded">較擁擠的初始位置</option></select></label></div><div id="cluster-plot"></div><div class="ml-stats">${stat('ITERATION','cluster-iteration')}${stat('INERTIA','cluster-inertia')}${stat('SAMPLES','cluster-samples')}</div><div id="cluster-centers" class="ml-centers" aria-live="polite"></div><div class="ml-actions"><button id="cluster-reset" class="secondary-button">↺ 重設中心</button><button id="cluster-step" class="secondary-button">執行指派與更新 →</button></div><p id="cluster-note" class="ml-note"></p><p class="ml-caption">十二個手工點，直接實作 Lloyd 兩步驟；十字為中心。空群保留原中心並提示，與 sklearn 完整重設策略不同。完整 KMeans 範例見第 38 章。</p></div></div></section>
    <section id="roadmap"><div class="section-header"><h2>從觀念到可交付的學習流程</h2><span>10 MODULES · 60 CHAPTERS</span></div><div class="module-list">${course.groups.map(g=>{const lessons=course.lessons.filter(l=>l.group===g.id);return `<a class="module-row" href="#${lessons[0].id}"><span class="module-num">${g.number}</span><div><div class="module-name">${e(g.title)}</div><div class="module-description">${e(g.description)}</div></div><span class="module-count">${lessons.length} CHAPTERS ↗</span></a>`;}).join('')}</div></section><div class="reading-note" id="before-start"><strong>開始之前</strong><br>適合有基本 Python 經驗、想完整學習機器學習的讀者。必要數學從頭解釋，範例以 CPU、合成資料與原創短文離線執行。<br>2026-10-30 查核最新穩定版 scikit-learn 1.9.1；已在 Python 3.11 與相容數值依賴執行 45 項測試。互動實驗是 JavaScript 數學，不在網頁執行 Python。<br>進度與筆記獨立保存在此瀏覽器，無跨裝置同步。</div><p class="ml-bridge"><a href="examples.zip" download>下載完整 Python 範例包 ↓</a> · <a href="examples/README.md">安裝與執行說明</a><br>接著可學 <a href="../pytorch/index.html">PyTorch 實作工程</a>、<a href="../embedding/index.html">Embedding 與表示學習</a>，將同一套評估思維帶往更多應用。</p>${footer}`;
    toc.innerHTML=`<h2 class="toc-label">本頁導覽</h2><div class="toc-links">${[['intro','關於這份教學'],['regression-lab','回歸與誤差'],['threshold-lab','門檻與成本'],['cv-lab','CV 與資料洩漏'],['tree-lab','決策樹分裂'],['cluster-lab','KMeans 迭代'],['roadmap','完整學習路線'],['before-start','版本與開始之前']].map(([id,title])=>`<a href="#overview/${id}">${title}</a>`).join('')}</div><div class="toc-tip"><p>先定義問題，再比較模型。</p><p><kbd>Ctrl</kbd> + <kbd>K</kbd> 搜尋全部章節</p></div>`;
    mount(main);
  }
  function mount(main){
    const q=s=>main.querySelector(s),value=id=>Number(q('#'+id).value);
    function drawRegression(){
      const w=value('reg-w'),b=value('reg-b'),r=regression(regressionPoints,w,b),x=v=>45+(v+3.5)*450/7,y=v=>260-(v+8)*240/18;
      q('#reg-w-value').textContent=f(w);q('#reg-b-value').textContent=f(b);q('#reg-mse').textContent=f(r.mse);q('#reg-mae').textContent=f(r.mae);q('#reg-r2').textContent=f(r.r2);
      const grid=[-6,-2,2,6,10].map(v=>`<path d="M45 ${y(v)}H495" stroke="#273029"/><text class="ml-axis" x="17" y="${y(v)+3}">${v}</text>`).join('')+[-3,-2,-1,0,1,2,3].map(v=>`<path d="M${x(v)} 20V260" stroke="#273029"/><text class="ml-axis" x="${x(v)-3}" y="279">${v}</text>`).join('');
      q('#reg-plot').innerHTML=`<svg class="ml-plot" viewBox="0 0 540 300" role="img" aria-label="七個資料點、預測直線與垂直殘差"><title>調整斜率與偏移觀察誤差</title><defs><clipPath id="ml-reg-clip"><rect x="45" y="20" width="450" height="240"/></clipPath></defs>${grid}<g clip-path="url(#ml-reg-clip)"><path d="M${x(-3.5)} ${y(w*-3.5+b)}L${x(3.5)} ${y(w*3.5+b)}" stroke="#e5c185" stroke-width="2"/>${regressionPoints.map(([a,c])=>`<path d="M${x(a)} ${y(c)}V${y(w*a+b)}" stroke="#9fd3db" stroke-dasharray="3 4" opacity=".6"/><circle cx="${x(a)}" cy="${y(c)}" r="4.5" fill="#9fd3db"/>`).join('')}</g><text class="ml-axis" x="507" y="279">x</text><text class="ml-axis" x="18" y="12">y</text></svg>`;
      q('#reg-note').textContent=`目前 ŷ = ${f(w)}x ${b<0?'−':'+'} ${f(Math.abs(b))}。MSE 最小的直線仍有非零誤差，因為這些點含手工擾動。`;
    }
    function drawDecision(){
      const t=value('decision-threshold'),cost=value('decision-fn'),r=metrics(labels,scores,t,cost,1);
      q('#decision-threshold-value').textContent=f(t);q('#decision-fn-value').textContent=cost;
      q('#decision-rows').innerHTML=scores.map((p,i)=>{const decision=p>=t,error=Number(decision)!==labels[i];return `<div class="ml-score ${error?'error':''}"><div class="score-top"><span>#${i+1}</span><b>${p.toFixed(2)}</b></div><div class="score-bar"><span style="width:${p*100}%"></span></div><small>真值 ${labels[i]} ／ 預測 ${Number(decision)}<br>${error?(labels[i]?'FN · 漏報':'FP · 誤報'):'判斷正確'}</small></div>`;}).join('');
      q('#decision-confusion').innerHTML=['tp','fp','fn','tn'].map(k=>`<div>${k.toUpperCase()}<strong>${r[k]}</strong></div>`).join('');
      q('#decision-precision').textContent=(r.precision*100).toFixed(1)+'%';q('#decision-recall').textContent=(r.recall*100).toFixed(1)+'%';q('#decision-cost').textContent=r.cost;
      const best=bestThreshold(labels,scores,cost,1);q('#decision-note').textContent=`目前成本 ${r.fn} × ${cost} + ${r.fp} × 1 = ${r.cost}。這組驗證資料的最低成本為 ${best.cost}，門檻 ${f(best.threshold)}；成本相同時選較低門檻。`;
    }
    function drawFold(){
      const fold=value('cv-fold')-1,leaked=q('#cv-policy').value==='leaked',r=foldStats(featureValues,fold,leaked);
      q('#cv-fold-value').textContent=fold+1;q('#cv-count').textContent=r.fit.length;q('#cv-mean').textContent=f(r.mean);q('#cv-zmean').textContent=f(r.validationMeanZ);
      q('#cv-rows').innerHTML=featureValues.map((v,i)=>`<div class="ml-row ${r.validation.includes(i)?'validation':''} ${leaked&&r.validation.includes(i)?'leaked':''}"><small>#${i+1}</small>${v}</div>`).join('');
      q('#cv-pipeline').innerHTML=`<span>${leaked?'20 筆全資料':'16 筆 train'} fit scaler</span>→<span>transform train / val</span>→<span>train fit model</span>→<span>val evaluate</span>`;
      q('#cv-note').textContent=leaked?'錯誤流程：驗證特徵已影響 mean 與 scale，打破未見資料邊界。這不需要讀取 y 也會發生。':`正確流程：只看 train 的 16 筆，fit mean = ${f(r.mean)}。validation 可以不是零均值，因為它沒有重新 fit。`;
    }
    function drawTree(){
      const threshold=value('tree-threshold'),r=split(treeRows,threshold),x=v=>50+(v-1)*440/7;
      q('#tree-threshold-value').textContent=f(threshold);q('#tree-parent').textContent=f(r.parent);q('#tree-weighted').textContent=f(r.weighted);q('#tree-gain').textContent=f(r.gain);
      q('#tree-plot').innerHTML=`<svg class="ml-plot" viewBox="0 0 540 130" role="img" aria-label="八個樣本與可移動的分裂閾值"><title>x 小於等於門檻向左，其他向右</title><path d="M38 77H504" stroke="#3e493e"/><path d="M${x(threshold)} 18V95" stroke="#b5e99b" stroke-dasharray="3 4"/>${treeRows.map(p=>`<circle cx="${x(p.x)}" cy="77" r="8" fill="${palette[p.y]}"/><text x="${x(p.x)-3}" y="108">${p.x}</text><text x="${x(p.x)-3}" y="56">${p.y}</text>`).join('')}</svg>`;
      q('#tree-root').textContent=`父節點 8 筆 ／ class 0: 4、class 1: 4 ／ Gini ${f(r.parent)}`;
      q('#tree-children').innerHTML=[['左分支',r.left],['右分支',r.right]].map(([title,rows])=>{const positive=rows.reduce((sum,p)=>sum+p.y,0);return `<div class="ml-tree-child"><b>${title} · ${rows.length} 筆</b><br>class 0: ${rows.length-positive} ／ class 1: ${positive}<br>Gini ${f(gini(rows.map(p=>p.y)))}<div class="ml-tree-bars"><span style="width:${100*(rows.length-positive)/rows.length}%"></span><span style="width:${100*positive/rows.length}%"></span></div></div>`;}).join('');
      q('#tree-note').textContent=`加權子節點 Gini = ${r.left.length}/8 × ${f(gini(r.left.map(p=>p.y)))} + ${r.right.length}/8 × ${f(gini(r.right.map(p=>p.y)))} = ${f(r.weighted)}。每次較佳分裂不保證整棵樹全域最佳。`;
    }
    let cluster;
    function resetCluster(){
      const k=value('cluster-k'),crowded=q('#cluster-init').value==='crowded';
      const centers=k===3?(crowded?[[-4,-3],[-2,-2],[4,1]]:[[-4,-3],[0,0],[4,-3]]):(crowded?[[-4,-3],[-2,-2]]:[[-4,-3],[4,3]]);
      const assignment=assign(clusterPoints,centers);cluster={centers,assignment,iteration:0,stable:false,counts:centers.map((_,i)=>assignment.filter(k=>k===i).length),inertia:inertia(clusterPoints,centers,assignment)};drawCluster();
    }
    function drawCluster(){
      const x=v=>45+(v+5)*450/10,y=v=>260-(v+4)*240/8;
      q('#cluster-plot').innerHTML=`<svg class="ml-plot" viewBox="0 0 540 290" role="img" aria-label="十二個手工點的KMeans指派與中心位置"><title>線連到目前指派中心，十字為中心</title>${[-4,-2,0,2,4].map(v=>`<path d="M${x(v)} 20V260M45 ${y(v)}H495" stroke="#273029"/><text class="ml-axis" x="${x(v)-3}" y="278">${v}</text>`).join('')}${clusterPoints.map((p,i)=>`<path d="M${x(p[0])} ${y(p[1])}L${x(cluster.centers[cluster.assignment[i]][0])} ${y(cluster.centers[cluster.assignment[i]][1])}" stroke="${palette[cluster.assignment[i]]}" opacity=".25"/><circle cx="${x(p[0])}" cy="${y(p[1])}" r="4.5" fill="${palette[cluster.assignment[i]]}"/>`).join('')}${cluster.centers.map((p,i)=>`<circle cx="${x(p[0])}" cy="${y(p[1])}" r="11" fill="#111412" stroke="${palette[i]}"/><path d="M${x(p[0])-6} ${y(p[1])}h12M${x(p[0])} ${y(p[1])-6}v12" stroke="${palette[i]}" stroke-width="1.5"/>`).join('')}</svg>`;
      q('#cluster-iteration').textContent=cluster.iteration;q('#cluster-inertia').textContent=f(cluster.inertia);q('#cluster-samples').textContent=clusterPoints.length;
      q('#cluster-centers').innerHTML=cluster.centers.map((p,i)=>`<div class="ml-center"><b style="color:${palette[i]}">CLUSTER ${i}</b><output>[${p.map(f).join(', ')}]<br>${cluster.counts[i]} 筆</output></div>`).join('');
      q('#cluster-step').disabled=cluster.stable;q('#cluster-step').textContent=cluster.stable?'中心已穩定 ✓':'執行指派與更新 →';
      q('#cluster-note').textContent=cluster.counts.includes(0)?'本輪有空群，保留其舊中心。空群策略與初始位置都可能影響結果。':cluster.stable?'中心不再變動，這組初始值已收斂。仍可能是局部解；換初始位置與 K 再比較。':cluster.iteration?`已完成第 ${cluster.iteration} 輪：依舊中心指派，再取群內平均；目前 inertia 使用本輪指派與新中心。`:'起點：依目前初始中心指派。執行一次，觀察中心移動及 inertia。';
    }
    ['w','b'].forEach(id=>q('#reg-'+id).addEventListener('input',drawRegression));q('#reg-fit').addEventListener('click',()=>{const best=ols(regressionPoints);q('#reg-w').value=best.w.toFixed(2);q('#reg-b').value=best.b.toFixed(2);drawRegression();});
    ['#decision-threshold','#decision-fn'].forEach(id=>q(id).addEventListener('input',drawDecision));q('#decision-optimize').addEventListener('click',()=>{q('#decision-threshold').value=bestThreshold(labels,scores,value('decision-fn'),1).threshold;drawDecision();});
    q('#cv-fold').addEventListener('input',drawFold);q('#cv-policy').addEventListener('change',drawFold);q('#tree-threshold').addEventListener('input',drawTree);
    ['#cluster-k','#cluster-init'].forEach(id=>q(id).addEventListener('change',resetCluster));q('#cluster-reset').addEventListener('click',resetCluster);q('#cluster-step').addEventListener('click',()=>{if(cluster.stable)return;const next=lloyd(clusterPoints,cluster.centers);cluster={...next,iteration:cluster.iteration+1,stable:!next.changed};drawCluster();});
    drawRegression();drawDecision();drawFold();drawTree();resetCluster();
  }
  overview.courseSlug='machine-learning';window.renderCourseOverview=overview;
})();
