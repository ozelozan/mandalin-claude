(function(){
  var s=document.querySelector('.story');
  function fit(){s.style.transform='scale('+Math.min(innerWidth/1080,innerHeight/1920,1)+')'}
  fit();addEventListener('resize',fit);
  // [x, y, boyut, renk, donus]
  window.yildizlar=function(list){list.forEach(function(a){
    var d=document.createElement('div');d.className='yildiz';
    d.style.cssText='left:'+a[0]+'px;top:'+a[1]+'px;width:'+a[2]+'px;height:'+a[2]+'px;background:'+a[3]+';transform:rotate('+a[4]+'deg)';
    s.insertBefore(d,s.firstChild.nextSibling)})};
})();
