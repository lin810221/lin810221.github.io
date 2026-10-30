/* Browser numerical demonstrations. These do not execute PyTorch or Python. */
(() => {
  'use strict';
  const format = value => Number(value.toFixed(4)).toString();
  function broadcast(a,b){
    if(!a.length||!b.length||[...a,...b].some(n=>!Number.isInteger(n)||n<1))throw new RangeError('Positive dimensions required');
    const size=Math.max(a.length,b.length),left=Array(size-a.length).fill(1).concat(a),right=Array(size-b.length).fill(1).concat(b);
    return left.map((n,i)=>{if(n!==right[i]&&n!==1&&right[i]!==1)throw new RangeError('Incompatible shapes');return Math.max(n,right[i]);});
  }
  function gradient(x,w,b,target){
    if([x,w,b,target].some(n=>!Number.isFinite(n)))throw new RangeError('Finite values required');
    const prediction=w*x+b,error=prediction-target,loss=error*error;
    return {prediction,error,loss,dw:2*error*x,db:2*error};
  }
  function batching(n,batch,accumulate,drop=false){
    if([n,batch,accumulate].some(v=>!Number.isInteger(v)||v<1))throw new RangeError('Positive integer budgets required');
    const sizes=[];
    for(let start=0;start<n;start+=batch){const size=Math.min(batch,n-start);if(size===batch||!drop)sizes.push(size);}
    const count=sizes.reduce((a,b)=>a+b,0),losses=sizes.map((_,i)=>i+1),groups=[];
    for(let i=0;i<sizes.length;i+=accumulate)groups.push(sizes.slice(i,i+accumulate).reduce((a,b)=>a+b,0));
    return {sizes,count,groups,dropped:n-count,weighted:count?sizes.reduce((sum,size,i)=>sum+size*losses[i],0)/count:null,naive:losses.length?losses.reduce((a,b)=>a+b,0)/losses.length:null};
  }
  window.PyTorchLab={broadcast,gradient,batching};
  const stat=(label,id)=>`<div class="torch-stat"><small>${label}</small><output id="${id}"></output></div>`;
  const slider=(id,label,min,max,step,value)=>`<label for="${id}">${label}<output id="${id}-value"></output><input id="${id}" type="range" min="${min}" max="${max}" step="${step}" value="${value}"></label>`;
  function overview({course,saved,escapeHTML:e,main,toc,footer}){
    const last=saved.last||course.lessons[0].id;
    main.innerHTML=`<section class="course-hero" id="intro"><div class="eyebrow">PYTORCH ENGINEERING <span>／ 從數值到模型</span></div><h1 class="torch-title">PyTorch<span class="hero-period">.</span></h1><h2 class="hero-subtitle">讓每一次更新，<br>都有你理解的理由。</h2><p class="hero-description">從第一個 Tensor 開始，親手寫出資料載入、反向傳播與完整訓練流程。再把模型變成可以驗證、保存、恢復與交付的實作。</p><div class="hero-meta"><span><b>48</b> 個完整章節</span><span><b>24</b> 份 Python 範例</span><span><b>4</b> 個互動實驗室</span><span><b>2.15.0</b> 最新穩定版基準</span></div><div class="hero-actions"><a class="primary-button" href="#${last}">${saved.last?'繼續學習':'從第一章開始'} <span aria-hidden="true">→</span></a><a class="text-link" href="#overview/shape-lab">先探索 Tensor 的形狀 ↓</a></div><div class="torch-path"><span>TENSORS</span><i>→</i><span>GRADIENTS</span><i>→</i><span>TRAINING</span><i>→</i><span>ENGINEERING</span></div></section>
    <section id="shape-lab"><div class="section-header"><h2>能相減，就代表比對正確嗎？</h2><span>LAB 01 · SHAPES</span></div><p class="torch-intro">預測固定為 [N,1]。改變答案的形狀，看逐樣本誤差如何意外變成兩兩比較。</p><div class="torch-lab"><div class="torch-lab-head"><span>BROADCASTING · PREDICTION − TARGET</span><b>NUMERICAL DEMO</b></div><div class="torch-padded"><div class="torch-controls">${slider('shape-size','樣本數 N',2,6,1,4)}<label for="shape-target">答案 target 的 shape<select id="shape-target"><option value="flat" selected>[N] · 一維向量</option><option value="column">[N,1] · 保留尾軸</option></select></label></div><div class="torch-stats">${stat('PREDICTION','shape-prediction')}${stat('TARGET','shape-answer')}${stat('RESULT','shape-result')}</div><div class="torch-matrix-wrap"><div id="shape-matrix" class="torch-matrix" aria-live="polite"></div></div><p class="torch-note" id="shape-note"></p><p class="torch-caption">predᵢ = i+1、targetⱼ = j+0.5，索引從 0 開始。框線標示同一筆樣本；完整 PyTorch 對照在第 5、6 章。</p></div></div></section>
    <section id="gradient-lab"><div class="section-header"><h2>梯度，指向哪裡？</h2><span>LAB 02 · AUTOGRAD</span></div><p class="torch-intro">調整 y = wx + b，親手對照平方誤差與 chain rule。這裡的導數由公式計算；實際 backward 範例在第 8 章。</p><div class="torch-lab"><div class="torch-lab-head"><span>FORWARD VALUES · BACKWARD DERIVATIVES</span><b>ANALYTIC GRADIENTS</b></div><div class="torch-padded"><div class="torch-controls">${slider('grad-x','輸入 x',1,5,.5,3)}${slider('grad-w','權重 w',-3,3,.1,2)}${slider('grad-b','偏移 b',-2,2,.1,0)}${slider('grad-target','目標 target',0,12,.5,10)}</div><div id="gradient-graph"></div><div class="torch-stats">${stat('SQUARED ERROR','grad-loss')}${stat('∂L / ∂w','grad-dw')}${stat('∂L / ∂b','grad-db')}</div><p class="torch-note" id="grad-note"></p><p class="torch-caption">負梯度更新 w ← w − η·∂L/∂w。只觀察局部方向不能保證任意學習率都下降。</p></div></div></section>
    <section id="step-lab"><div class="section-header"><h2>backward 後，權重變了嗎？</h2><span>LAB 03 · TRAIN STEP</span></div><p class="torch-intro">逐步執行一次 scalar SGD。再取消清梯度，觀察第二輪如何意外沿用上一輪的 .grad。</p><div class="torch-lab"><div class="torch-lab-head"><span>x = 3 · target = 10 · lr = 0.01</span><b>ONE PARAMETER</b></div><div class="torch-padded"><div class="torch-steps" id="step-track"></div><pre class="torch-state" id="step-state" aria-live="polite"></pre><label class="torch-check" for="step-clear"><input type="checkbox" id="step-clear" checked>每輪開始執行 zero_grad（可取消比較）</label><div class="torch-actions"><button id="step-reset" class="secondary-button">↺ 重設實驗</button><button id="step-next" class="secondary-button">執行下一步 →</button></div><p class="torch-note" id="step-note"></p><p class="torch-caption">使用固定公式模擬 state，沒有呼叫 optimizer。每次 backward 會累加到梯度緩衝；完整 Python 迴圈在第 20 章。</p></div></div></section>
    <section id="batch-lab"><div class="section-header"><h2>最後一批，該佔多少權重？</h2><span>LAB 04 · BATCHES</span></div><p class="torch-intro">改變資料量與 batch，看尾批、丟樣本與有效更新群組。示意各批 loss mean 固定為 1、2、3…，比較平均方法。</p><div class="torch-lab"><div class="torch-lab-head"><span>TAIL BATCH · SAMPLE-WEIGHTED MEAN</span><b>COUNT THE SAMPLES</b></div><div class="torch-padded"><div class="torch-controls">${slider('batch-n','資料總數',2,24,1,10)}${slider('batch-size','每批上限',2,8,1,4)}${slider('batch-accumulate','每次更新最多累積幾批',1,4,1,2)}<label class="torch-check" for="batch-drop"><input id="batch-drop" type="checkbox">drop_last · 丟棄不滿一批</label></div><div id="batch-tiles" class="torch-batches"></div><div class="torch-stats">${stat('SAMPLES USED / TOTAL','batch-count')}${stat('WEIGHTED MEAN','batch-weighted')}${stat('MEAN OF BATCH MEANS','batch-naive')}</div><div class="torch-groups" id="batch-groups" aria-live="polite"></div><p class="torch-note" id="batch-note"></p><p class="torch-caption">此處只示範未加權、每筆一個 loss 的分類契約。token mask／class weight 需另推分母。真實尾批等價測試在第 36 章。</p></div></div></section>
    <section id="roadmap"><div class="section-header"><h2>循序建立自己的訓練工程</h2><span>8 MODULES · 48 CHAPTERS</span></div><div class="module-list">${course.groups.map(group=>{const lessons=course.lessons.filter(l=>l.group===group.id);return `<a class="module-row" href="#${lessons[0].id}"><span class="module-num">${group.number}</span><div><div class="module-name">${e(group.title)}</div><div class="module-description">${e(group.description)}</div></div><span class="module-count">${lessons.length} CHAPTERS ↗</span></a>`;}).join('')}</div></section><div class="reading-note" id="before-start"><strong>開始之前</strong><br>適合有基本 Python 經驗、想完整學習 PyTorch 的讀者。從 CPU 開始，合成資料不需下載；GPU／多程序另列條件。網頁示範使用 JavaScript 數學，Python 範例使用真正 PyTorch。<br>版本查核：2026-10-30，最新穩定版 2.15.0。已在 2.15.0+cpu 執行 40 項測試；CUDA、DDP 通訊與 Inductor 效能需另行驗證。<br>進度與筆記保存於此瀏覽器，無跨裝置同步。</div><p class="torch-links"><a href="examples.zip" download>下載完整 Python 範例包 ↓</a> · <a href="examples/README.md">安裝與執行說明</a><br>想把學習到的表示用於搜尋、分類與推薦，可接著讀 <a href="../embedding/index.html">Embedding 與表示學習 ↗</a>。</p>${footer}`;
    toc.innerHTML=`<h2 class="toc-label">本頁導覽</h2><div class="toc-links">${[['intro','關於這份教學'],['shape-lab','Shape 與廣播'],['gradient-lab','梯度的方向'],['step-lab','更新的五個步驟'],['batch-lab','尾批與累積'],['roadmap','完整學習路線'],['before-start','版本與開始之前']].map(([id,label])=>`<a href="#overview/${id}">${label}</a>`).join('')}</div><div class="toc-tip"><p>先寫出預期的 shape 與數字，再執行核對。</p><p><kbd>Ctrl</kbd> + <kbd>K</kbd> 搜尋全部章節</p></div>`;
    mount(main);
  }
  function mount(main){
    const q=selector=>main.querySelector(selector),value=id=>Number(q('#'+id).value);
    function shape(){
      const n=value('shape-size'),column=q('#shape-target').value==='column',result=broadcast([n,1],column?[n,1]:[n]);
      q('#shape-size-value').textContent=n;q('#shape-prediction').textContent=`[${n},1]`;q('#shape-answer').textContent=column?`[${n},1]`:`[${n}]`;q('#shape-result').textContent=`[${result}]`;
      const matrix=q('#shape-matrix');matrix.style.gridTemplateColumns=`repeat(${column?1:n},minmax(0,1fr))`;
      matrix.innerHTML=Array.from({length:n},(_,i)=>Array.from({length:column?1:n},(_,j)=>{const target=column?i:j;return `<span class="torch-cell ${i===target?'diagonal':''}"><small>${i},${target}</small>${format(i+1-target-.5)}</span>`;}).join('')).join('');
      q('#shape-note').textContent=column?`正確逐樣本比較：${n} 個誤差，各筆 pred 與自己的 target 相減。`:`產生 ${n*n} 個誤差。每一列預測和所有答案相減；即使程式可運算，也已改變訓練目標。`;
    }
    function grad(){
      const x=value('grad-x'),w=value('grad-w'),b=value('grad-b'),target=value('grad-target'),g=gradient(x,w,b,target);
      ['x','w','b','target'].forEach(id=>{q('#grad-'+id+'-value').textContent=format(value('grad-'+id));});
      q('#grad-loss').textContent=format(g.loss);q('#grad-dw').textContent=format(g.dw);q('#grad-db').textContent=format(g.db);
      q('#gradient-graph').innerHTML=`<svg class="torch-graph" viewBox="0 0 540 175" role="img" aria-label="y等於wx加b，平方誤差及其導數"><title>前向值與反向導數</title><path d="M130 65H208M330 65H403" stroke="#66705d"/><path d="m198 60 10 5-10 5m195-10 10 5-10 5" fill="none" stroke="#66705d"/><rect x="15" y="30" width="115" height="70" rx="7" fill="#1b211d" stroke="#3b463b"/><rect x="208" y="30" width="122" height="70" rx="7" fill="#1b211d" stroke="#3b463b"/><rect x="403" y="30" width="122" height="70" rx="7" fill="#1b211d" stroke="#75613e"/><text x="30" y="52" class="graph-hint">PARAMETERS</text><text x="30" y="76">w=${format(w)} b=${format(b)}</text><text x="222" y="52" class="graph-hint">y = w·${format(x)} + b</text><text x="222" y="76">y = ${format(g.prediction)}</text><text x="417" y="52" class="graph-hint">L = (y − ${format(target)})²</text><text x="417" y="76">L = ${format(g.loss)}</text><text x="333" y="127" class="derivative">∂L/∂y = ${format(2*g.error)}</text><text x="125" y="151" class="derivative">∂L/∂w = ∂L/∂y · x = ${format(g.dw)}</text></svg>`;
      q('#grad-note').textContent=g.dw<0?'∂L/∂w 為負：足夠小的負梯度更新會增加 w。':g.dw>0?'∂L/∂w 為正：足夠小的負梯度更新會減少 w。':'此點 ∂L/∂w = 0；本例已命中目標。';
    }
    const actions=['zero_grad','forward','loss','backward','step'];
    let state;
    function reset(){state={phase:0,updates:0,w:2,prediction:null,loss:null,grad:null};q('#step-clear').checked=true;drawStep('起點：權重 w=2，尚未 forward。');}
    function drawStep(note){
      q('#step-track').innerHTML=actions.map((name,i)=>`<div class="torch-step ${state.phase===i?'current':i<state.phase?'done':''}" ${state.phase===i?'aria-current="step"':''}>${i+1} · ${name}</div>`).join('');
      q('#step-state').textContent=JSON.stringify({w:Number(state.w.toFixed(6)),prediction:state.prediction,loss:state.loss,grad:state.grad,optimizer_updates:state.updates},null,2);
      q('#step-next').textContent=state.phase===5?'開始下一輪更新 →':`執行 ${actions[state.phase]} →`;
      q('#step-note').textContent=note;
    }
    q('#step-next').addEventListener('click',()=>{
      if(state.phase===5)state.phase=0;
      let note='';
      switch(state.phase){
        case 0:if(q('#step-clear').checked){state.grad=null;note='清除 .grad；參數 w 保持原值。';}else note='略過 zero_grad；上一輪 .grad 會在下一次 backward 被繼續累加。';state.prediction=null;state.loss=null;break;
        case 1:state.prediction=Number((state.w*3).toFixed(6));note='forward 算出預測，尚未計算梯度或更新參數。';break;
        case 2:state.loss=Number(((state.prediction-10)**2).toFixed(6));note='得到 scalar loss，權重仍未更新。';break;
        case 3:state.grad=Number(((state.grad??0)+2*(state.prediction-10)*3).toFixed(6));note='backward 將導數累加到 .grad；w 仍未改變。';break;
        case 4:state.w=Number((state.w-.01*state.grad).toFixed(6));state.updates++;note='SGD step 讀取 .grad 更新 w。這裡 prediction 與 loss 仍是更新前 forward 的值。';break;
      }
      state.phase++;drawStep(note);
    });
    q('#step-reset').addEventListener('click',reset);
    function batch(){
      const n=value('batch-n'),size=value('batch-size'),acc=value('batch-accumulate'),r=batching(n,size,acc,q('#batch-drop').checked);
      ['n','size','accumulate'].forEach(id=>{q('#batch-'+id+'-value').textContent=value('batch-'+id);});
      q('#batch-tiles').innerHTML=r.sizes.map((count,i)=>`<div class="torch-batch"><strong>${count} 筆</strong><span>BATCH ${i+1}<br>mean loss = ${i+1}</span></div>`).join('')||'<p class="torch-note">沒有完整 batch，這輪沒有樣本。</p>';
      q('#batch-count').textContent=`${r.count} / ${n}`;q('#batch-weighted').textContent=r.weighted===null?'—':format(r.weighted);q('#batch-naive').textContent=r.naive===null?'—':format(r.naive);
      q('#batch-groups').textContent=r.groups.length?`每次 optimizer step 的實際樣本數：${r.groups.join(' → ')} ／ 共 ${r.groups.length} 次更新`:'沒有有效更新群組。';
      q('#batch-note').textContent=`使用 ${r.count} 筆，丟棄 ${r.dropped} 筆。${r.weighted!==null&&Math.abs(r.weighted-r.naive)>1e-9?'直接平均 batch mean 會改變尾批權重。':'本設定兩種平均相同，仍需以實際樣本數定義分母。'} 累積時每組以本組樣本總數加權。`;
    }
    ['#shape-size','#shape-target'].forEach(id=>q(id).addEventListener(id==='#shape-target'?'change':'input',shape));
    ['x','w','b','target'].forEach(id=>q('#grad-'+id).addEventListener('input',grad));
    ['n','size','accumulate'].forEach(id=>q('#batch-'+id).addEventListener('input',batch));q('#batch-drop').addEventListener('change',batch);
    shape();grad();reset();batch();
  }
  overview.courseSlug='pytorch';window.renderCourseOverview=overview;
})();
