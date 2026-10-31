(() => {
const box=document.getElementById('case-lightbox');
const image=box.querySelector('img');
const close=box.querySelector('button');
let previousFocus=null;
function hide(){ if(box.hidden)return;box.hidden=true;image.removeAttribute('src');if(previousFocus)previousFocus.focus(); }
document.querySelectorAll('[data-case-zoom]').forEach(b=>b.addEventListener('click',()=>{previousFocus=b;image.src=b.dataset.caseZoom;image.alt=b.querySelector('img')?.alt||'Project image';box.hidden=false;close.focus();}));
document.querySelectorAll('.case-thumbnails').forEach(strip=>{
  const media=strip.closest('.case-media');
  const hero=media.querySelector('.case-image-open');
  strip.addEventListener('click',event=>{
    const thumb=event.target.closest('[data-gallery-src]');
    if(!thumb || !strip.contains(thumb))return;
    const src=thumb.dataset.gallerySrc;
    hero.dataset.caseZoom=src;
    const mainImage=hero.querySelector('img');
    mainImage.src=src;
    mainImage.alt=thumb.getAttribute('aria-label');
    strip.querySelectorAll('.case-thumb').forEach(b=>{
      const active=b===thumb;
      b.classList.toggle('is-active',active);
      b.setAttribute('aria-pressed',String(active));
    });
  });
});
close.addEventListener('click',hide);
box.addEventListener('click',(e)=>{if(e.target===box)hide()});
document.addEventListener('keydown',(e)=>{if(!box.hidden && e.key==='Escape'){e.stopImmediatePropagation();hide();}if(!box.hidden && e.key==='Tab'){e.preventDefault();close.focus();}},true);
})();
