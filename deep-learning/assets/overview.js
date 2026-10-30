/* Deterministic browser mathematics and a real small JS MLP; no Torch runtime. */
(() => {
  'use strict';
  const cyan='#b3d9c4',amber='#e5c185',purple='#c8afd6',fmt=x=>Number(x.toFixed(4)).toString();
  function finite(values){if(!values.length||values.some(x=>!Number.isFinite(x)))throw new RangeError('Finite values required');}
  const sigmoid=x=>x>=0?1/(1+Math.exp(-x)):Math.exp(x)/(1+Math.exp(x));
  function activation(name,x){
    finite([x]);
    if(name==='sigmoid'){const y=sigmoid(x);return {y,derivative:y*(1-y)};}
    if(name==='tanh'){const y=Math.tanh(x);return {y,derivative:1-y*y};}
    if(name==='relu')return {y:Math.max(0,x),derivative:x>0?1:0};
    throw new RangeError('Unknown activation');
  }
  const xorX=[[0,0],[0,1],[1,0],[1,1]],xorY=[0,1,1,0];
  function newNetwork(){
    let seed=17;
    const random=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed/4294967296)*2-1;};
    return {w:Array.from({length:8},()=>[random(),random()]),b:Array(8).fill(0),v:Array.from({length:8},random),c:0,steps:0};
  }
  function forward(net,x){
    const h=net.w.map((w,j)=>Math.tanh(w[0]*x[0]+w[1]*x[1]+net.b[j])),z=h.reduce((s,a,j)=>s+a*net.v[j],net.c);
    return {h,z,p:sigmoid(z)};
  }
  function xorLoss(net){return xorX.reduce((s,x,i)=>{const {z}=forward(net,x);return s+(Math.max(z,0)-z*xorY[i]+Math.log1p(Math.exp(-Math.abs(z))))/4;},0);}
  function train(net,steps=200,lr=.5){
    if(!Number.isInteger(steps)||steps<1||steps>4000||!(lr>0&&lr<=1))throw new RangeError('Invalid training budget');
    for(let step=0;step<steps;step++){
      const dw=net.w.map(()=>[0,0]),db=net.b.map(()=>0),dv=net.v.map(()=>0);let dc=0;
      xorX.forEach((x,i)=>{
        const {h,p}=forward(net,x),dz=(p-xorY[i])/4;dc+=dz;
        h.forEach((a,j)=>{dv[j]+=a*dz;const dh=net.v[j]*dz*(1-a*a);db[j]+=dh;dw[j][0]+=dh*x[0];dw[j][1]+=dh*x[1];});
      });
      net.w.forEach((w,j)=>{w[0]-=lr*dw[j][0];w[1]-=lr*dw[j][1];net.b[j]-=lr*db[j];net.v[j]-=lr*dv[j];});net.c-=lr*dc;net.steps++;
    }
    return xorLoss(net);
  }
  const image=[[0,0,1,0,0],[0,1,3,1,0],[1,2,5,2,1],[0,1,3,1,0],[0,0,1,0,0]];
  const edge=[[1,0,-1],[1,0,-1],[1,0,-1]],blur=Array.from({length:3},()=>Array(3).fill(1/9));
  function convolution(data,kernel){
    if(!data.length||!kernel.length||!data[0]?.length||!kernel[0]?.length||data.some(r=>r.length!==data[0].length)||kernel.some(r=>r.length!==kernel[0].length)||data.length<kernel.length||data[0].length<kernel[0].length)throw new RangeError('Rectangular input and fitting kernel required');
    finite([...data.flat(),...kernel.flat()]);
    return Array.from({length:data.length-kernel.length+1},(_,r)=>Array.from({length:data[0].length-kernel[0].length+1},(_,c)=>kernel.reduce((sum,row,i)=>sum+row.reduce((s,v,j)=>s+v*data[r+i][c+j],0),0)));
  }
  function normalize(data,mode,epsilon=1e-5){
    if(!data.length||!data[0]?.length||data.some(r=>r.length!==data[0].length)||!['batch','layer'].includes(mode)||!Number.isFinite(epsilon)||epsilon<=0)throw new RangeError('Invalid normalization shape or policy');
    finite(data.flat());const rows=data.length,cols=data[0].length;
    const groups=mode==='batch'?Array.from({length:cols},(_,c)=>data.map(r=>r[c])):data;
    const means=groups.map(a=>a.reduce((s,x)=>s+x,0)/a.length),variances=groups.map((a,i)=>a.reduce((s,x)=>s+(x-means[i])**2,0)/a.length);
    return {means,variances,values:Array.from({length:rows},(_,r)=>Array.from({length:cols},(_,c)=>{const axis=mode==='batch'?c:r;return (data[r][c]-means[axis])/Math.sqrt(variances[axis]+epsilon);} ))};
  }
  const qk=[[1,0],[0,1],[1,1]];
  function attention(q,k,v,causal=true,temperature=1){
    if(!q.length||!k.length||!q[0]?.length||k.length!==v.length||q.some(r=>r.length!==q[0].length)||k.some(r=>r.length!==q[0].length)||!Number.isFinite(temperature)||temperature<=0||typeof causal!=='boolean')throw new RangeError('Invalid attention shape or temperature');
    finite([...q.flat(),...k.flat(),...v]);
    const weights=q.map((row,i)=>{
      const scores=k.map((key,j)=>causal&&j>i?-Infinity:row.reduce((s,x,d)=>s+x*key[d],0)/Math.sqrt(row.length)/temperature),maximum=Math.max(...scores);
      if(!Number.isFinite(maximum))throw new RangeError('No allowed key');
      const exp=scores.map(s=>Math.exp(s-maximum)),total=exp.reduce((a,b)=>a+b,0);return exp.map(e=>e/total);
    });
    return {weights,outputs:weights.map(row=>row.reduce((s,w,j)=>s+w*v[j],0))};
  }
  function diffusion(clean,noise,step,total=30){
    if(clean.length!==noise.length||!Number.isInteger(total)||total<2||!Number.isInteger(step)||step<1||step>total)throw new RangeError('Invalid diffusion schedule');
    finite([...clean,...noise]);let abar=1;
    for(let t=0;t<step;t++)abar*=1-(.03+(.2-.03)*t/(total-1));
    const signal=Math.sqrt(abar),sigma=Math.sqrt(1-abar);return {abar,signal,sigma,values:clean.map((x,i)=>signal*x+sigma*noise[i])};
  }
  window.DeepLearningLab={activation,newNetwork,forward,xorLoss,train,convolution,normalize,attention,diffusion};
  const slider=(id,name,min,max,step,value)=>`<label for="${id}">${name}<output id="${id}-value"></output><input id="${id}" type="range" min="${min}" max="${max}" step="${step}" value="${value}"></label>`;
  const select=(id,name,items)=>`<label for="${id}">${name}<select id="${id}">${items.map(([value,label],i)=>`<option value="${value}"${i?'':' selected'}>${label}</option>`).join('')}</select></label>`;
  const stat=(name,id)=>`<div class="dl-stat"><small>${name}</small><output id="${id}"></output></div>`;
  function section(id,title,number,subtitle,intro,body,caption){return `<section id="${id}"><div class="section-header"><h2>${title}</h2><span>LAB ${number} · ${subtitle}</span></div><p class="dl-intro">${intro}</p><div class="dl-lab"><div class="dl-lab-head"><span>${subtitle}</span><b>LIVE MATHEMATICS</b></div><div class="dl-body">${body}<p class="dl-caption">${caption}</p></div></div></section>`;}
  function overview({course,saved,escapeHTML:e,main,toc,footer}){
    const last=saved.last||course.lessons[0].id;
    main.innerHTML=`<section class="course-hero" id="intro"><div class="eyebrow">THE DEEP LEARNING FIELD GUIDE <span>／ 從一個神經元開始</span></div><h1 class="dl-title">Deep Learning<span class="hero-period">.</span></h1><h2 class="hero-subtitle">理解每一層的轉換，<br>也理解學習為何發生。</h2><p class="hero-description">從手算一次反向傳播，到卷積、序列、Attention 與生成模型。把公式化成可檢查的數字，親手看見表示如何學習、梯度如何流動，以及模型何時值得相信。</p><div class="hero-meta"><span><b>72</b> 個循序章節</span><span><b>42</b> 份 Python 範例</span><span><b>6</b> 個互動實驗</span><span><b>2.15.0</b> PyTorch</span></div><div class="hero-actions"><a class="primary-button" href="#${last}">${saved.last?'繼續學習':'從第一章開始'} <span aria-hidden="true">↗</span></a><a class="text-link" href="#overview/gradient-lab">先看一次梯度如何流動 ↗</a></div><div class="dl-path"><span>REPRESENT</span><i>→</i><span>DIFFERENTIATE</span><i>→</i><span>LEARN</span><i>→</i><span>VERIFY</span></div></section>`+
    section('gradient-lab','一層導數，如何影響二十層？','01','ACTIVATIONS & GRADIENTS','改變輸入與函數，觀察數值、局部導數和重複相乘。曲線與虛線分別表示函數和導數。',
      `<div class="dl-controls">${select('act-kind','激活函數',[['sigmoid','Sigmoid'],['tanh','Tanh'],['relu','ReLU']])}${slider('act-x','每層的局部輸入 z',-6,6,.1,0)}${slider('act-depth','鏈長 L',1,20,1,10)}</div><div id="act-plot"></div><div class="dl-stats">${stat('φ(z)','act-y')}${stat('LOCAL DERIVATIVE','act-d')}${stat('DERIVATIVE PRODUCT','act-chain')}</div><p class="dl-note" id="act-note" aria-live="polite"></p>`,
      '這是每層權重皆為 1、局部導數相同的假設性鏈乘，並未逐層重新計算輸入。ReLU 在 0 的導數依 PyTorch 慣例取 0。真實深網還包含各層 Jacobian；詳見第 12、23 章。')+
    section('xor-lab','四個點，真的訓練一個小網路','02','A TRAINABLE MLP','同為 1 的兩個角要分開，單一直線做不到。這裡真的以手寫梯度更新 2 → 8 → 1 Tanh 網路，觀察決策區域如何改變。',
      `<div id="xor-plot"></div><div class="dl-stats">${stat('FULL-BATCH UPDATES','xor-steps')}${stat('TRAIN BCE','xor-loss')}${stat('CORRECT / 4','xor-correct')}</div><div id="xor-predictions" class="dl-predictions" aria-live="polite"></div><div class="dl-actions"><button id="xor-reset" class="secondary-button">重設相同初始化</button><button id="xor-train" class="secondary-button">訓練 200 步 →</button></div><p class="dl-note">色塊為 p(y=1)：紫色偏 0、綠色偏 1；圓點標出四筆訓練標籤。固定初始化、全批次梯度下降，lr = 0.5，上限 4,000 步。</p>`,
      '這是 JavaScript 真實小型訓練，沒有呼叫 Torch。四筆同時用於訓練與顯示，沒有驗證集，因此只證明能擬合 XOR。Python 實作見第 7 章。')+
    section('convolution-lab','把卷積拆成九次乘法','03','KERNEL SCANNER','移動 3 × 3 視窗，看局部輸入、共享 kernel 與輸出格。選擇邊緣或平均核，直接核對加總。',
      `<div class="dl-controls">${select('conv-kernel','共享 kernel',[['edge','左右差分'],['blur','3 × 3 平均']])}${slider('conv-position','輸出格索引（由左至右）',0,8,1,0)}</div><div class="dl-matrices"><div><h3>輸入 5 × 5</h3><div id="conv-input"></div></div><div><h3>Kernel 3 × 3</h3><div id="conv-filter"></div></div><div><h3>輸出 3 × 3</h3><div id="conv-output"></div></div></div><div class="dl-equation" id="conv-products" aria-live="polite"></div><p class="dl-note" id="conv-note"></p>`,
      '使用 cross-correlation 慣例，kernel 不翻轉，stride 1、padding 0、bias 0，與此設定的 Conv2d 相同。只顯示單輸入／輸出 channel；更多通道還要沿 channel 加總，見第 31 章。')+
    section('normalization-lab','改一個數字，哪些輸出跟著變？','04','NORMALIZATION AXES','每列是一筆樣本，每欄是一個特徵。改左上角輸入，對照 BatchNorm 跨樣本與 LayerNorm 跨特徵的統計範圍。',
      `<div class="dl-controls">${select('norm-mode','正規化方式',[['batch','BatchNorm：每一欄'],['layer','LayerNorm：每一列']])}${slider('norm-delta','左上角額外加值 Δ',-3,8,.1,2)}</div><div class="dl-matrices two"><div><h3>原始輸入 X</h3><div id="norm-input"></div></div><div><h3>正規化輸出</h3><div id="norm-output"></div></div></div><div class="dl-stats">${stat('FIRST GROUP MEAN','norm-mean')}${stat('FIRST GROUP VARIANCE','norm-var')}${stat('Δ OUTPUT [1,0]','norm-other')}</div><p class="dl-note" id="norm-note" aria-live="polite"></p>`,
      '訓練態數學示意，使用母體變異數、ε = 0.00001、γ = 1、β = 0。未模擬 BatchNorm 的 running buffers 或 eval 行為；Torch 的完整語意與實測在第 28、29 章。')+
    section('attention-lab','Attention 能不能偷看未來？','05','Q · K · V · MASK','Q 與 K 固定，只改最後一個 token 的 V。切換 causal mask，觀察較早位置的輸出是否受影響。',
      `<div class="dl-controls">${slider('attn-query','觀察 query 位置',1,3,1,1)}${slider('attn-temperature','額外溫度 τ',.3,2,.1,1)}${slider('attn-future','最後一個 V 額外加值',-6,6,.5,0)}<label class="dl-check" for="attn-causal"><input id="attn-causal" type="checkbox" checked> 啟用 causal mask（僅允許現在與過去）</label></div><div class="dl-attention-layout"><div><h3>每列是 query，每欄是 key</h3><div id="attn-weights"></div></div><div id="attn-vectors" class="dl-equation"></div></div><div class="dl-stats">${stat('SELECTED OUTPUT','attn-out')}${stat('ROW WEIGHT SUM','attn-sum')}${stat('CHANGE FROM ΔV = 0','attn-change')}</div><p class="dl-note" id="attn-note" aria-live="polite"></p>`,
      'logits = QKᵀ / √2 / τ；V 為 [1,2,4+Δ]，沒有 dropout。這裡的 mask 表示「允許哪些位置」，不沿用特定 Torch API 的 bool 慣例。MHA 與 SDPA 的差異詳見第 44 章。')+
    section('diffusion-lab','加噪之後，訊號還剩多少？','06','FORWARD DIFFUSION','同一份資料、同一份固定噪音，沿時間改變訊號與噪音係數。實線是 xₜ，虛線保留乾淨 x₀ 作對照。',
      `${slider('noise-step','時間 t（數學索引由 1 開始）',1,30,1,1)}<div id="noise-plot"></div><div class="dl-stats">${stat('ᾱₜ','noise-abar')}${stat('SIGNAL √ᾱₜ','noise-signal')}${stat('NOISE √(1−ᾱₜ)','noise-sigma')}</div><p class="dl-note" id="noise-note" aria-live="polite"></p>`,
      '僅計算前向加噪閉式公式，並未訓練或執行反向生成；固定 ε 適合比較係數，不代表一條逐步採樣的 Markov 軌跡。β 從 0.03 線性到 0.2，共 30 步。實際訓練並採樣的 1D DDPM 在第 52 章。')+
    `<section id="roadmap"><div class="section-header"><h2>從原理，走到可以驗證的模型</h2><span>12 MODULES · 72 CHAPTERS</span></div><div class="module-list">${course.groups.map(g=>{const lessons=course.lessons.filter(l=>l.group===g.id);return `<a class="module-row" href="#${lessons[0].id}"><span class="module-num">${g.number}</span><div><div class="module-name">${e(g.title)}</div><div class="module-description">${e(g.description)}</div></div><span class="module-count">${lessons.length} CHAPTERS ↗</span></a>`;}).join('')}</div></section><div class="reading-note" id="before-start"><strong>開始之前</strong><br>適合已具備基本 Python、想完整理解深度學習的讀者。數學從必要的向量、導數與機率補起，每章包含例子、練習與解答。<br>2026-10-30 查核最新穩定版 PyTorch 2.15.0，已在 Python 3.11 / CPU 執行 55 項測試。所有 Python 範例使用合成資料，安裝後可離線執行。<br>六個網頁實驗使用 JavaScript；CPU 玩具結果不代表真實任務效果。進度與筆記儲存在目前瀏覽器。</div><p class="dl-bridge"><a href="examples.zip" download>下載完整 Python 範例 ↗</a> · <a href="examples/README.md">安裝與執行說明</a><br>搭配 <a href="../pytorch/index.html">PyTorch 實作工程</a> 掌握程式與訓練流程；以 <a href="../machine-learning/index.html">機器學習</a> 補足資料、選模與評估。</p>${footer}`;
    const links=[['intro','關於這門課'],['gradient-lab','激活與梯度'],['xor-lab','訓練 XOR 網路'],['convolution-lab','卷積視窗'],['normalization-lab','正規化範圍'],['attention-lab','Attention 與未來'],['diffusion-lab','Diffusion 加噪'],['roadmap','完整學習路線'],['before-start','版本與先備知識']];
    toc.innerHTML=`<h2 class="toc-label">本頁導覽</h2><div class="toc-links">${links.map(([id,title])=>`<a href="#overview/${id}">${title}</a>`).join('')}</div><div class="toc-tip"><p>先算一個數字，再解釋整個模型。</p><p><kbd>Ctrl</kbd> + <kbd>K</kbd> 搜尋全部章節</p></div>`;
    mount(main);
  }
  function table(values,marked=()=>false,label='數值矩陣'){
    return `<table class="dl-matrix" aria-label="${label}"><tbody>${values.map((row,r)=>`<tr>${row.map((v,c)=>`<td${marked(r,c)?' class="marked"':''}>${fmt(v)}</td>`).join('')}</tr>`).join('')}</tbody></table>`;
  }
  function linePlot(series,min,max,label){
    const x=(i,n)=>45+i*480/(n-1),y=v=>235-(v-min)*210/(max-min);
    return `<svg class="dl-plot" viewBox="0 0 560 270" role="img" aria-label="${label}"><title>${label}</title>${[min,(min+max)/2,max].map(v=>`<path d="M45 ${y(v)}H525" stroke="#29382e"/><text x="4" y="${y(v)+4}">${fmt(v)}</text>`).join('')}${series.map(s=>`<path d="${s.values.map((v,i)=>`${i?'L':'M'}${x(i,s.values.length)} ${y(v)}`).join(' ')}" fill="none" stroke="${s.color}" stroke-width="2"${s.dashed?' stroke-dasharray="5 5"':''}/>`).join('')}<text x="45" y="260">${series.map(s=>s.name).join(' · ')}</text></svg>`;
  }
  function mount(main){
    const q=s=>main.querySelector(s),val=id=>Number(q('#'+id).value),out=(id,value)=>{q('#'+id).textContent=value;};
    function drawActivation(){
      const kind=q('#act-kind').value,x=val('act-x'),depth=val('act-depth'),a=activation(kind,x),chain=a.derivative**depth;
      out('act-x-value',fmt(x));out('act-depth-value',depth);out('act-y',fmt(a.y));out('act-d',fmt(a.derivative));out('act-chain',chain===0?'0':chain.toExponential(3));
      const inputs=Array.from({length:121},(_,i)=>-6+i/10),scaleY=v=>225-(v+1.1)*190/7.3,scaleX=v=>45+(v+6)*40;
      q('#act-plot').innerHTML=`<svg class="dl-plot" viewBox="0 0 560 270" role="img" aria-label="激活函數與局部導數"><title>綠色為函數，橙色虛線為導數</title><path d="M45 ${scaleY(0)}H525M285 22V235" stroke="#39463a"/>${[-6,-3,0,3,6].map(v=>`<text x="${scaleX(v)-6}" y="252">${v}</text>`).join('')}${['y','derivative'].map((key,i)=>`<path d="${inputs.map((v,j)=>`${j?'L':'M'}${scaleX(v)} ${scaleY(activation(kind,v)[key])}`).join(' ')}" fill="none" stroke="${i?amber:cyan}" stroke-width="2"${i?' stroke-dasharray="5 4"':''}/>`).join('')}<path d="M${scaleX(x)} 22V235" stroke="${purple}" stroke-dasharray="2 4"/><circle cx="${scaleX(x)}" cy="${scaleY(a.y)}" r="4" fill="${cyan}"/></svg>`;
      out('act-note',`假設 ${depth} 層的局部導數都為 ${fmt(a.derivative)}，導數乘積為 ${chain===0?'0':chain.toExponential(3)}。權重與不同層輸入尚未納入。`);
    }
    let net=newNetwork();
    function drawXor(){
      const p=xorX.map(x=>forward(net,x).p);out('xor-steps',net.steps);out('xor-loss',fmt(xorLoss(net)));out('xor-correct',`${p.filter((v,i)=>Number(v>=.5)===xorY[i]).length} / 4`);
      q('#xor-predictions').innerHTML=p.map((v,i)=>`<div><small>[${xorX[i]}] → ${xorY[i]}</small><output>${fmt(v)}</output></div>`).join('');
      const low=-.25,span=1.5,cells=24;
      let blocks='';for(let r=0;r<cells;r++)for(let c=0;c<cells;c++){
        const x=low+(c+.5)*span/cells,y=low+(cells-r-.5)*span/cells,p=forward(net,[x,y]).p;
        blocks+=`<rect x="${100+c*15}" y="${20+r*9}" width="15.2" height="9.2" fill="rgb(${Math.round(168+11*p)},${Math.round(135+82*p)},${Math.round(193+3*p)})" fill-opacity=".7"/>`;
      }
      const sx=x=>100+(x-low)*360/span,sy=y=>236-(y-low)*216/span;
      q('#xor-plot').innerHTML=`<svg class="dl-plot" viewBox="0 0 560 275" role="img" aria-label="小型神經網路的XOR決策區域"><title>四點標籤與目前網路的正類機率色塊</title>${blocks}${xorX.map((x,i)=>`<circle cx="${sx(x[0])}" cy="${sy(x[1])}" r="11" fill="#121c16" stroke="${xorY[i]?cyan:purple}" stroke-width="2"/><text x="${sx(x[0])-4}" y="${sy(x[1])+4}" fill="${xorY[i]?cyan:purple}">${xorY[i]}</text>`).join('')}<text x="100" y="263">x₁ →　色塊顯示模型 p(y=1)</text><text x="10" y="25">x₂ ↑</text></svg>`;
      q('#xor-train').disabled=net.steps>=4000;
    }
    function drawConvolution(){
      const position=val('conv-position'),row=Math.floor(position/3),col=position%3,kernel=q('#conv-kernel').value==='blur'?blur:edge,values=convolution(image,kernel);
      out('conv-position-value',`${position} → [${row},${col}]`);
      q('#conv-input').innerHTML=table(image,(r,c)=>r>=row&&r<row+3&&c>=col&&c<col+3,'卷積輸入與目前視窗');
      q('#conv-filter').innerHTML=table(kernel,()=>false,'共享卷積kernel');q('#conv-output').innerHTML=table(values,(r,c)=>r===row&&c===col,'卷積輸出');
      const terms=kernel.flatMap((line,i)=>line.map((w,j)=>`${image[row+i][col+j]} × (${fmt(w)})`));
      out('conv-products',terms.join(' + ')+` = ${fmt(values[row][col])}`);out('conv-note',`輸出 [${row},${col}] 讀取輸入 row ${row}–${row+2}、column ${col}–${col+2}，與同一個 kernel 逐項乘加。`);
    }
    const normBase=[[1,2,3],[4,8,6],[7,8,9]];
    function drawNorm(){
      const mode=q('#norm-mode').value,delta=val('norm-delta'),data=normBase.map(r=>[...r]);data[0][0]+=delta;
      const a=normalize(data,mode),base=normalize(normBase,mode),affected=(r,c)=>mode==='batch'?c===0:r===0;
      out('norm-delta-value',fmt(delta));q('#norm-input').innerHTML=table(data,(r,c)=>r===0&&c===0,'改變左上角的輸入');q('#norm-output').innerHTML=table(a.values,affected,'正規化統計影響的範圍');
      out('norm-mean',fmt(a.means[0]));out('norm-var',fmt(a.variances[0]));out('norm-other',fmt(a.values[1][0]-base.values[1][0]));
      out('norm-note',mode==='batch'?'每欄跨三筆樣本計算統計。左上角改變會影響同欄其他樣本，綠格標示這一欄。':'每列內三個特徵計算統計。左上角改變只影響第一筆樣本，第二筆的 [1,0] 保持不變。');
    }
    function drawAttention(){
      const query=val('attn-query')-1,temp=val('attn-temperature'),delta=val('attn-future'),causal=q('#attn-causal').checked,v=[1,2,4+delta],a=attention(qk,qk,v,causal,temp),base=attention(qk,qk,[1,2,4],causal,temp);
      out('attn-query-value',query+1);out('attn-temperature-value',fmt(temp));out('attn-future-value',fmt(delta));
      q('#attn-weights').innerHTML=`<table class="dl-matrix dl-heatmap" aria-label="三個query對三個key的Attention權重"><thead><tr><th>Q / K</th><th>1</th><th>2</th><th>3</th></tr></thead><tbody>${a.weights.map((row,i)=>`<tr${i===query?' class="selected"':''}><th>${i+1}</th>${row.map((w,j)=>`<td style="background:rgba(179,217,196,${w*.55})">${causal&&j>i?'禁止':fmt(w)}</td>`).join('')}</tr>`).join('')}</tbody></table>`;
      out('attn-vectors',`Q = K = [[1,0],[0,1],[1,1]]\nV = [${v.map(fmt).join(', ')}]\n輸出 = [${a.outputs.map(fmt).join(', ')}]`);
      out('attn-out',fmt(a.outputs[query]));out('attn-sum',fmt(a.weights[query].reduce((s,w)=>s+w,0)));out('attn-change',fmt(a.outputs[query]-base.outputs[query]));
      out('attn-note',causal&&query<2?`query ${query+1} 禁止讀取第 3 個 V，所以改最後 V 不影響此輸出。`:`query ${query+1} 可以讀取第 3 個 V，改值量會依該 key 的權重傳到輸出。`);
    }
    const clean=[-1,-.7,.4,1,.5,-.5,.2,.8],noise=[-.4,1.2,-.8,.3,1,-.6,.5,-1.1];
    function drawDiffusion(){
      const step=val('noise-step'),a=diffusion(clean,noise,step);out('noise-step-value',`${step} / 30`);out('noise-abar',fmt(a.abar));out('noise-signal',fmt(a.signal));out('noise-sigma',fmt(a.sigma));
      q('#noise-plot').innerHTML=linePlot([{name:'x₀ 乾淨（虛線）',values:clean,color:amber,dashed:true},{name:'xₜ 加噪（實線）',values:a.values,color:cyan}],-1.8,1.8,'固定噪音下的前向Diffusion係數比較');
      out('noise-note',`xₜ = ${fmt(a.signal)} x₀ + ${fmt(a.sigma)} ε。給定 x₀ 的條件噪音變異數為 ${fmt(1-a.abar)}；目前曲線只是同一 ε 的八個固定座標。`);
    }
    const bind=(ids,fn,event='input')=>ids.forEach(id=>q('#'+id).addEventListener(event,fn));
    bind(['act-x','act-depth'],drawActivation);bind(['act-kind'],drawActivation,'change');
    q('#xor-train').addEventListener('click',()=>{train(net,Math.min(200,4000-net.steps));drawXor();});q('#xor-reset').addEventListener('click',()=>{net=newNetwork();drawXor();});
    bind(['conv-position'],drawConvolution);bind(['conv-kernel'],drawConvolution,'change');bind(['norm-delta'],drawNorm);bind(['norm-mode'],drawNorm,'change');
    bind(['attn-query','attn-temperature','attn-future'],drawAttention);bind(['attn-causal'],drawAttention,'change');bind(['noise-step'],drawDiffusion);
    drawActivation();drawXor();drawConvolution();drawNorm();drawAttention();drawDiffusion();
  }
  overview.courseSlug='deep-learning';window.renderCourseOverview=overview;
})();
