(function(){
  var s=document.querySelector('.story');
  // #png ile açılınca ölçekleme yok (PNG çıktısı için tam 1080x1920)
  function fit(){if(location.hash=='#png'){document.body.style.display='block';return}
    s.style.transform='scale('+Math.min(innerWidth/1080,innerHeight/1920,1)+')'}
  fit();addEventListener('resize',fit);
  // Kemerdeki renkli yıldızlar: [x, y, boyut, renk, dönüş]
  var renk={k:'#e2231a',s:'#ffc928',y:'#2fb457',m:'#3c8dde',t:'#ff8a1f',p:'#c04bd6'};
  window.yildizlar=function(list){list.forEach(function(a){
    var d=document.createElement('div');d.className='yildiz';
    d.style.cssText='left:'+a[0]+'px;top:'+a[1]+'px;width:'+a[2]+'px;height:'+a[2]+'px;background:'+(renk[a[3]]||a[3])+';transform:rotate('+a[4]+'deg);opacity:'+(a[5]||1);
    s.insertBefore(d,s.firstChild)})};
})();
