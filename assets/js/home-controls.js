(() => {
 const projects=document.getElementById('projects-scroll');
 const expertise=document.getElementById('expertise-strip');
 document.querySelectorAll('[data-scroll]').forEach(button=>button.addEventListener('click',()=>{
  if(!projects) return;
  const first=projects.querySelector('.tile');
  const second=projects.querySelectorAll('.tile')[3];
  const step=second&&first?second.offsetTop-first.offsetTop:projects.clientHeight;
  projects.scrollBy({top:(button.dataset.scroll==='up'?-1:1)*step,behavior:'smooth'});
 }));

 if(expertise){
  const originals=[...expertise.querySelectorAll('.expertise-card')];
  if(originals.length>1){
   // Three identical sequences give both directions continuous adjacent cards.
   // A position correction occurs only between equivalent cards, never a jump
   // from the last card to the first across the visible carousel.
   const cloneCard=(card)=>{
    const clone=card.cloneNode(true);
    clone.setAttribute('aria-hidden','true');
    clone.querySelectorAll('[tabindex],a,button,input,select,textarea').forEach(el=>el.setAttribute('tabindex','-1'));
    return clone;
   };
   const before=document.createDocumentFragment();
   const after=document.createDocumentFragment();
   originals.forEach(card=>{before.appendChild(cloneCard(card));after.appendChild(cloneCard(card));});
   expertise.prepend(before);
   expertise.append(after);
   const step=()=>{
    const cards=expertise.querySelectorAll('.expertise-card');
    return cards[1].offsetLeft-cards[0].offsetLeft;
   };
   const cycle=()=>step()*originals.length;
   const teleport=(left)=>{
    const behavior=expertise.style.scrollBehavior;
    const snap=expertise.style.scrollSnapType;
    expertise.style.scrollBehavior='auto';
    expertise.style.scrollSnapType='none';
    expertise.scrollLeft=left;
    // Force recalculation before restoring snap, avoiding an intermediate snap.
    void expertise.offsetWidth;
    expertise.style.scrollSnapType=snap;
    expertise.style.scrollBehavior=behavior;
   };
   let settleTimer;
   const normalize=()=>{
    const length=cycle();
    if(length<=0)return;
    const x=expertise.scrollLeft;
    if(x<length-1)teleport(x+length);
    else if(x>=2*length-1)teleport(x-length);
   };
   // Initialize to the middle copy with all original cards in natural order.
   teleport(cycle());
   expertise.addEventListener('scroll',()=>{
    clearTimeout(settleTimer);
    settleTimer=setTimeout(normalize,160);
   },{passive:true});
   document.querySelectorAll('[data-expertise]').forEach(button=>button.addEventListener('click',()=>{
    const direction=button.dataset.expertise==='left'?-1:1;
    expertise.scrollBy({left:direction*step(),behavior:'smooth'});
   }));
   // Recenter after responsive grid widths change without changing visible items.
   let previousStep=step();
   window.addEventListener('resize',()=>{
    const updatedStep=step();
    if(Math.abs(updatedStep-previousStep)<0.5)return;
    const centerIndex=(expertise.scrollLeft/previousStep)-originals.length;
    previousStep=updatedStep;
    teleport((originals.length+centerIndex)*updatedStep);
    normalize();
   });
  }
 }
})();
// Open existing patent, publication, recommendation and certificate panels.
document.querySelectorAll('.highlight-card[data-target]').forEach(button => {
 button.addEventListener('click', () => {
  if (typeof openPanel === 'function') openPanel(button.dataset.target);
 });
});
