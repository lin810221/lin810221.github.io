/* Local deterministic laboratories: illustrative calculations, no training API. */
(() => {
  'use strict';
  const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const fmt=x=>Number(x.toFixed(6)).toLocaleString('en-US',{maximumFractionDigits:6});
  function masked(probabilities,mask){
    if(probabilities.length!==mask.length||!mask.some(Boolean)||probabilities.some(x=>!(x>0&&x<=1)))throw new RangeError('invalid targets');
    const n=mask.filter(Boolean).length;return {count:n,loss:-probabilities.reduce((s,p,i)=>s+(mask[i]?Math.log(p):0),0)/n};
  }
  function lora(input,output,rank,alpha){
    if(![input,output,rank].every(x=>Number.isInteger(x)&&x>0)||!(alpha>0))throw new RangeError('invalid dimensions');
    return {base:input*output,adapter:rank*(input+output),scale:alpha/rank,rsScale:alpha/Math.sqrt(rank)};
  }
  function quantize(values,bits){
    if(!Number.isInteger(bits)||bits<2||bits>8||!values.length)throw new RangeError('invalid quantizer');
    const qmax=2**(bits-1)-1,scale=Math.max(...values.map(Math.abs),1e-12)/qmax;
    const codes=values.map(x=>Math.max(-qmax,Math.min(qmax,Math.round(x/scale))));
    const reconstructed=codes.map(x=>x*scale),mse=values.reduce((s,x,i)=>s+(x-reconstructed[i])**2,0)/values.length;
    return {scale,codes,reconstructed,mse};
  }
  function memory(base,adapters,bits,activationGiB){
    if([base,adapters,activationGiB].some(x=>!Number.isFinite(x)||x<0)||![4,8,16,32].includes(bits))throw new RangeError('invalid memory');
    return {base:base*bits/8,states:adapters*16,activation:activationGiB*2**30};
  }
  function aggregate(a,b){if(!(a>0&&b>0))throw new RangeError('empty batch');return (a+3*b)/(a+b);}
  function dpo(policy,reference,beta){
    if(!(beta>0))throw new RangeError('invalid beta');const z=beta*(policy-reference);
    return {z,loss:Math.max(-z,0)+Math.log1p(Math.exp(-Math.abs(z))),preference:1/(1+Math.exp(-z))};
  }
  const softmax=(xs,t)=>{const m=Math.max(...xs),a=xs.map(x=>Math.exp((x-m)/t)),sum=a.reduce((s,x)=>s+x,0);return a.map(x=>x/sum);};
  function kd(temperature){
    if(!(temperature>0))throw new RangeError('invalid temperature');
    const teacher=softmax([2,0,-2],temperature),student=softmax([1,0,-1],temperature);
    return {teacher,student,loss:temperature**2*teacher.reduce((s,p,i)=>s+p*Math.log(p/student[i]),0)};
  }
  function budget(rows,epochs,batch,accumulation){
    if(![rows,epochs,batch,accumulation].every(x=>Number.isInteger(x)&&x>0))throw new RangeError('invalid budget');
    const microbatches=Math.ceil(rows/batch);return {microbatches:microbatches*epochs,updates:Math.ceil(microbatches/accumulation)*epochs,exposures:rows*epochs};
  }
  window.FinetuningLab={masked,lora,quantize,memory,aggregate,dpo,kd,budget};
  const slider=(id,label,min,max,step,value)=>`<label for="${id}">${label}<output id="${id}-value" for="${id}">${value}</output><input id="${id}" type="range" min="${min}" max="${max}" step="${step}" value="${value}"></label>`;
  const equation=tex=>`<span class="math-source" data-display="false" data-tex="${esc(tex)}">$${esc(tex)}$</span>`;
  function bars(values,title){
    return `<svg class="tf-plot" viewBox="0 0 500 180" role="img"><title>${esc(title)}</title>${values.map((v,i)=>`<rect x="${50+i*140}" y="${150-v*120}" width="85" height="${v*120}" fill="${['#b8e895','#89c9e8','#eebc79'][i%3]}"/><text x="${92+i*140}" y="173" font-size="17" text-anchor="middle" fill="#e5e9e2">${fmt(v)}</text>`).join('')}</svg>`;
  }
  function laboratories(){return `<section class="tf-labs" id="mechanism-labs"><h2>把公式變成能操作的實驗</h2><p>下列為確定性算例，不訓練模型、不連線、不讀取你的資料。每個實驗都標明假設；完整Python主線另有真實套件訓練。</p>
    <article class="tf-lab"><h3>監督遮罩與loss分母</h3><p>兩個user位置機率固定為0.9，assistant位置可調；預設只監督assistant。</p>${slider('ft-p1','第一個assistant target機率',.05,1,.05,.5)}${slider('ft-p2','第二個assistant target機率',.05,1,.05,.25)}<label class="tf-check" for="ft-user"><input type="checkbox" id="ft-user">把兩個user位置也納入loss</label><div id="ft-mask-output" class="tf-output" aria-live="polite"></div></article>
    <article class="tf-lab"><h3>LoRA的參數與縮放</h3><p>固定輸入、輸出維度皆4096；只計一個線性層的A與B，不含其他層及bias。</p>${slider('ft-rank','Rank',1,64,1,8)}${slider('ft-alpha','Alpha',1,128,1,16)}<div id="ft-lora-output" class="tf-output" aria-live="polite"></div></article>
    <article class="tf-lab"><h3>均勻量化的重建誤差</h3><p>固定權重為−0.9、−0.3、0、0.2、0.7、1，使用對稱均勻量化；這不是NF4。</p>${slider('ft-bits','位元數',2,8,1,4)}<div id="ft-quant-output" class="tf-output" aria-live="polite"></div></article>
    <article class="tf-lab"><h3>記憶體的分項預算</h3><p>70億參數基底；adapter權重、梯度及Adam兩狀態皆FP32。未計量化metadata、暫存、master copy或allocator。</p><label for="ft-base-bits">基底儲存位元<select id="ft-base-bits"><option value="4" selected>4 bits</option><option value="8">8 bits</option><option value="16">16 bits</option><option value="32">32 bits</option></select></label>${slider('ft-adapters','可訓練參數（百萬）',1,64,1,8)}${slider('ft-activation','Activation（GiB）',0,16,.5,1)}<div id="ft-memory-output" class="tf-output" aria-live="polite"></div></article>
    <article class="tf-lab"><h3>不等長microbatch的正確平均</h3><p>A平均loss為1、B為3。調整有效target數；比較全token平均與批次等權平均。</p>${slider('ft-count-a','A有效target',1,20,1,2)}${slider('ft-count-b','B有效target',1,20,1,8)}<div id="ft-acc-output" class="tf-output" aria-live="polite"></div></article>
    <article class="tf-lab"><h3>DPO的相對偏好</h3><p>固定reference偏好差為1，調整policy偏好差與beta。分數為回答序列log機率加總的差。</p>${slider('ft-gap','Policy偏好差',-5,6,.25,3)}${slider('ft-beta','Beta',.05,2,.05,.2)}<div id="ft-dpo-output" class="tf-output" aria-live="polite"></div></article>
    <article class="tf-lab"><h3>蒸餾溫度與軟分布</h3><p>固定teacher logits為[2,0,−2]、student為[1,0,−1]。同詞表、同位置，顯示教師分布與含溫度平方的KL。</p>${slider('ft-temperature','溫度',.5,6,.5,2)}<div id="ft-kd-output" class="tf-output" aria-live="polite"></div></article>
    <article class="tf-lab"><h3>資料曝光與更新次數</h3><p>固定每epoch 120筆、單程序、每批4筆，尾端累積群也做一次更新；不計packing與drop-last。</p>${slider('ft-epochs','Epochs',1,10,1,3)}${slider('ft-accumulation','梯度累積批數',1,16,1,4)}<div id="ft-budget-output" class="tf-output" aria-live="polite"></div></article></section>`;}
  function mount(){
    const q=s=>document.querySelector(s),v=id=>Number(q('#'+id).value);
    const listen=(ids,fn)=>{const update=()=>{for(const id of ids){const o=q('#'+id+'-value');if(o)o.textContent=q('#'+id).value;}fn();window.LearningNotesMath?.render(q('#mechanism-labs'));};ids.forEach(id=>q('#'+id).addEventListener(q('#'+id).type==='checkbox'||q('#'+id).tagName==='SELECT'?'change':'input',update));update();};
    listen(['ft-p1','ft-p2','ft-user'],()=>{const u=q('#ft-user').checked,r=masked([.9,.9,v('ft-p1'),v('ft-p2')],[u,u,true,true]);q('#ft-mask-output').innerHTML=bars([v('ft-p1'),v('ft-p2')],'兩個assistant target的正確條件機率')+`<p>有效target ${r.count}；平均NLL <strong id="ft-mask-loss">${fmt(r.loss)}</strong>。${equation(String.raw`-\frac{\sum_t m_t\log p_t}{\sum_t m_t}`)}</p>`;});
    listen(['ft-rank','ft-alpha'],()=>{const r=lora(4096,4096,v('ft-rank'),v('ft-alpha'));q('#ft-lora-output').innerHTML=`<p>基底 ${r.base.toLocaleString('en-US')}；adapter <strong id="ft-lora-count">${r.adapter.toLocaleString('en-US')}</strong>（${fmt(r.adapter/r.base*100)}%）。</p><p>標準縮放 ${fmt(r.scale)}；rsLoRA縮放 ${fmt(r.rsScale)}。${equation(String.raw`P=r(d_{in}+d_{out})`)}</p>`;});
    listen(['ft-bits'],()=>{const r=quantize([-.9,-.3,0,.2,.7,1],v('ft-bits'));q('#ft-quant-output').innerHTML=`<p>整數碼 [${r.codes.join(', ')}]</p><p>重建 [${r.reconstructed.map(fmt).join(', ')}]</p><p>Scale ${fmt(r.scale)}；MSE <strong id="ft-quant-mse">${fmt(r.mse)}</strong>。此例不含metadata容量。</p>`;});
    listen(['ft-base-bits','ft-adapters','ft-activation'],()=>{const bits=v('ft-base-bits'),r=memory(7e9,v('ft-adapters')*1e6,bits,v('ft-activation'));q('#ft-memory-output').innerHTML=`<p>基底 ${fmt(r.base/2**30)} GiB；adapter四份狀態 ${fmt(r.states/2**30)} GiB；activation ${fmt(r.activation/2**30)} GiB。</p><p>已列項目小計 <strong id="ft-memory-total">${fmt((r.base+r.states+r.activation)/2**30)}</strong> GiB。這不是GPU容量建議。</p>`;});
    listen(['ft-count-a','ft-count-b'],()=>{q('#ft-acc-output').innerHTML=`<p>全token平均 <strong id="ft-acc-loss">${fmt(aggregate(v('ft-count-a'),v('ft-count-b')))}</strong>；批次等權平均固定為2。${equation(String.raw`\frac{n_A\bar\ell_A+n_B\bar\ell_B}{n_A+n_B}`)}</p>`;});
    listen(['ft-gap','ft-beta'],()=>{const r=dpo(v('ft-gap'),1,v('ft-beta'));q('#ft-dpo-output').innerHTML=`<p>相對logit ${fmt(r.z)}；loss <strong id="ft-dpo-loss">${fmt(r.loss)}</strong>；pair preference機率 ${fmt(r.preference)}。</p>${equation(String.raw`-\log\sigma(\beta(\Delta_\theta-\Delta_{ref}))`)}<p>低loss不證明事實正確。</p>`;});
    listen(['ft-temperature'],()=>{const r=kd(v('ft-temperature'));q('#ft-kd-output').innerHTML=bars(r.teacher,'蒸餾教師的三類機率')+`<p>學生 [${r.student.map(fmt).join(', ')}]；KD loss <strong id="ft-kd-loss">${fmt(r.loss)}</strong>。</p>${equation(String.raw`\tau^2D_{KL}(p^T_\tau\Vert p^S_\tau)`)}`;});
    listen(['ft-epochs','ft-accumulation'],()=>{const r=budget(120,v('ft-epochs'),4,v('ft-accumulation'));q('#ft-budget-output').innerHTML=`<p>資料曝光 ${r.exposures} 筆；microbatch ${r.microbatches}；optimizer updates <strong id="ft-budget-updates">${r.updates}</strong>。</p><p>樣本數不能直接替代有效target數；scheduler依真正更新計步。</p>`;});
  }
  window.renderCourseOverview=({course,saved,escapeHTML,main,toc,footer})=>{
    const modules=course.groups.map(g=>`<a class="module-row" href="#${course.lessons.find(l=>l.group===g.id).id}"><span class="module-num">${g.number}</span><span><strong class="module-name">${escapeHTML(g.title)}</strong><small class="module-description">${escapeHTML(g.description)}</small></span><span class="module-count">6 單元</span></a>`).join('');
    main.innerHTML=`<section class="course-hero tf-hero"><div class="eyebrow">THE MODEL ADAPTATION GUIDE <span>／ 從資料，到可驗證的改變</span></div><h1>Adapt.<br>Evaluate.<br><span class="accent">Deliver.</span></h1><p class="tf-tagline">讓模型學會任務，<br>也知道改變了什麼。</p><p class="hero-description">從微調與RAG的選擇開始，親手檢查資料、聊天模板與監督token。以SFT、LoRA及DPO走完訓練、保留評估、續訓與成品交付；再深入QLoRA、蒸餾、領域適應及遺忘。</p><div class="tf-stats"><span><strong>12</strong> 章</span><span><strong>72</strong> 單元</span><span><strong>24</strong> 中文圖解</span><span><strong>24</strong> Python範例</span><span><strong>8</strong> 互動實驗</span></div><div class="hero-actions"><a class="tf-button primary" href="#001-adaptation-map">從模型適應開始</a><a class="tf-button" href="examples.zip" download>下載完整實作</a></div><p class="tf-baseline">2026-11-25查核 · Python 3.15.2 · PyTorch 2.15.0<br>Transformers 5.24.1 · PEFT 0.22.0 · TRL 1.18.2<br>CPU主線使用本地小模型與原創合成資料，不需API或外部權重。GPU、分散式與託管微調另列條件。</p></section><section id="learning-paths"><h2>從你的起點進入</h2><div class="tf-routes"><div><h3>第一次學微調</h3><p>先決定任務與資料，再逐token看懂模型在學什麼。</p><a href="#001-adaptation-map">策略、資料與模板</a></div><div><h3>完成LoRA工程</h3><p>從矩陣與梯度走到真實PEFT、成品與數值驗證。</p><a href="#025-lora-matrices">拆開LoRA</a></div><div><h3>深入模型適應</h3><p>在SFT基準上研究偏好、蒸餾、領域與保留能力。</p><a href="#043-sft-preferences">進入偏好學習</a></div></div><p>跨課閱讀：<a href="../transformer/index.html">Transformer與LLM原理</a>解釋架構；<a href="../pytorch/index.html">PyTorch</a>補張量與最佳化；<a href="../rag/index.html">RAG</a>深入檢索證據；<a href="../mcp/index.html">MCP</a>與<a href="../langgraph/index.html">LangGraph</a>處理工具與Agent執行。本課保留微調需要的完整工程主線。</p></section><section id="course-map"><h2>從選方法，走到交付</h2><div class="module-list">${modules}</div></section>${laboratories()}<section id="figure-atlas"><h2>原創中文圖解</h2><p>圖例區分資訊、計算與更新方向；數字均為標明假設的教學案例。點選可放大。</p><div class="tf-atlas">${course.visuals.map(f=>`<a href="${f.file}" target="_blank" rel="noopener"><img src="${f.file}" alt="${escapeHTML(f.alt)}" loading="lazy"><span>${escapeHTML(f.title)}</span></a>`).join('')}</div></section><section id="learning-resources"><h2>下載與實作</h2><p>程式包包含核心、24個入口、測試與完整鎖版；學習包包含72份題目與解析、術語、圖解和來源。目前完成 ${saved.completed.length} / 72。</p><div class="tf-resource-links"><a href="examples.zip" download>完整Python程式包</a><a href="study-pack.zip" download>圖解與學習單</a><a href="#072-sources">版本與驗證界線</a></div></section>${footer}`;
    toc.innerHTML=`<div class="toc-label">本頁目錄</div><div class="toc-links">${[['learning-paths','學習路線'],['course-map','十二章地圖'],['mechanism-labs','互動算例'],['figure-atlas','中文圖解'],['learning-resources','下載與來源']].map(([id,label])=>`<a href="#overview/${id}">${label}</a>`).join('')}</div>`;mount();
  };
  window.renderCourseOverview.courseSlug='finetuning';
})();
