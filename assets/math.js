/* Explicit, idempotent fallback for authors building without Node pre-render. */
(() => {
  'use strict';
  function render(root){
    if(!root)return;
    for(const element of root.querySelectorAll('.math-source,.math-block')){
      if(element.querySelector('.katex'))continue;
      const display=element.dataset.display==='true'||element.classList.contains('math-block');
      const text=element.textContent.trim();
      const tex=element.dataset.tex??(display?text.slice(2,-2).trim():text.slice(1,-1));
      if(!window.katex){element.dataset.mathPending='true';continue;}
      try{window.katex.render(tex,element,{displayMode:display,throwOnError:true,trust:false,strict:'ignore'});element.dataset.rendered='katex';delete element.dataset.mathPending;delete element.dataset.mathError;}
      catch(error){element.dataset.mathError='true';element.textContent='公式無法顯示：'+tex;console.error('Formula error',tex,error);}
    }
  }
  window.LearningNotesMath={render};
})();
