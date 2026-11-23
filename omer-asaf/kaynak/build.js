const pptxgen = require('pptxgenjs');
const React = require('react');
const RDS = require('react-dom/server');
const sharp = require('sharp');
const fa = require('react-icons/fa');
const { applyTheme } = require('/root/.claude/skills/synced/e126909c-a6a9-4939-9932-97c68f9725b7_3f08b13f-c5d2-4986-83c1-82f4703ea644/pptx/scripts/apply_theme.js');

const THEME = { name: 'Egitsel Oyunlar', headFontFace: 'Arial', bodyFontFace: 'Calibri',
  colors: { dk1:'14213D', lt1:'FFFFFF', dk2:'0B3D2E', lt2:'EEF3F0',
    accent1:'1F9D55', accent2:'F4B400', accent3:'E53935', accent4:'2A6F97', accent5:'8EC5E6', accent6:'FF7A00',
    hlink:'2A6F97', folHlink:'6D597A' } };
const HEX = THEME.colors;

async function icon(Comp, color, size=256){
  const svg = RDS.renderToStaticMarkup(React.createElement(Comp,{color:'#'+color,size}));
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return 'image/png;base64,'+buf.toString('base64');
}

(async()=>{
  const pres = new pptxgen();
  pres.layout = 'LAYOUT_WIDE'; // 13.33 x 7.5
  pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
  pres.title = 'RKR207 Eğitsel Oyunlar';
  const C = pres.SchemeColor;
  const W = 13.333, H = 7.5;

  // ---------- Layouts ----------
  pres.defineSlideMaster({ title:'KAPAK', background:{ color: HEX.dk2 }, objects:[] });
  pres.defineSlideMaster({ title:'ICERIK', background:{ color: HEX.lt1 },
    objects:[
      { text:{ text:'RKR207 Eğitsel Oyunlar', options:{ x:0.6, y:7.0, w:6, h:0.3, fontSize:10, color:'6B7A72', margin:0, isTextBox:true } } },
    ],
    slideNumber:{ x:12.3, y:7.0, w:0.5, h:0.3, fontSize:10, color:'6B7A72', align:'right' } });

  // ---------- 1. KAPAK ----------
  pres.addSection({ title:'Kapak' });
  let s = pres.addSlide({ masterName:'KAPAK', sectionTitle:'Kapak' });
  // saha çizgileri motifi: büyük orta daire + orta çizgi (sağ yarı)
  s.addShape(pres.shapes.OVAL, { x:8.2, y:1.0, w:5.5, h:5.5, fill:{ type:'none' }, line:{ color:'FFFFFF', width:2, transparency:80 }, objectName:'Saha dairesi' });
  s.addShape(pres.shapes.LINE, { x:10.95, y:0, w:0, h:H, line:{ color:'FFFFFF', width:2, transparency:80 }, objectName:'Orta çizgi' });
  s.addShape(pres.shapes.OVAL, { x:10.8, y:3.6, w:0.3, h:0.3, fill:{ color:'FFFFFF', transparency:70 }, line:{ type:'none' }, objectName:'Orta nokta' });
  // üç renk huni (oyun motifi)
  const cones = [[HEX.accent3,'Kırmızı'],[HEX.accent2,'Sarı'],[HEX.accent1,'Yeşil']];
  // üniversite kimliği
  s.addShape(pres.shapes.OVAL, { x:0.8, y:0.6, w:1.15, h:1.15, fill:{ color:'FFFFFF' }, line:{ type:'none' }, objectName:'Logo zemini' });
  s.addImage({ path:'logo.png', x:0.85, y:0.65, w:1.05, h:1.05, altText:'İstanbul Aydın Üniversitesi logosu', objectName:'Logo' });
  s.addText([
    { text:'İSTANBUL AYDIN ÜNİVERSİTESİ', options:{ fontSize:20, bold:true, color:'FFFFFF', charSpacing:1, breakLine:true } },
    { text:'Spor Bilimleri Fakültesi', options:{ fontSize:15, color:'CFE3D8' } },
  ], { x:2.2, y:0.65, w:7, h:1.05, margin:0, valign:'middle', isTextBox:true, objectName:'Üniversite' });

  cones.forEach((c,i)=> s.addShape(pres.shapes.ISOSCELES_TRIANGLE, { x:0.8+i*0.42, y:2.3, w:0.3, h:0.34, fill:{ color:c[0] }, line:{ type:'none' }, objectName:c[1]+' huni' }));
  s.addText('RKR207  ·  EĞİTSEL OYUNLAR DERSİ', { x:2.2, y:2.25, w:8, h:0.45, fontSize:18, bold:true, color:HEX.accent2, charSpacing:3, margin:0, valign:'middle', isTextBox:true, objectName:'Ders adı' });
  s.addText('HIZ VE ENGEL PARKURU', { x:0.8, y:2.85, w:11.7, h:1.3, fontFace:'Arial', fontSize:50, bold:true, color:'FFFFFF', margin:0, valign:'middle', isTextBox:true, objectName:'Oyun adı' });
  s.addText('Isınma · Ana Oyun · Soğuma  —  10-11 yaş grubu oyun planı', { x:0.8, y:4.2, w:9.6, h:0.5, fontSize:20, color:'CFE3D8', margin:0, isTextBox:true, objectName:'Alt başlık' });

  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:0.8, y:5.3, w:11.73, h:1.35, rectRadius:0.12, fill:{ color:'234F41' }, line:{ type:'none' }, objectName:'Bilgi şeridi' });
  const cells=[['Dersin Öğretim Üyesi','Dr. Öğr. Üyesi Ayla Rezvan Reha',1.1,4.9],['Öğrenci No','B2518.040050',6.3,2.6],['Öğrenci Ad ve Soyadı','Ömer Asaf ÖZEL',9.2,3.2]];
  cells.forEach(([l,v,x,w],i)=>{
    if(i>0) s.addShape(pres.shapes.LINE, { x:x-0.3, y:5.6, w:0, h:0.75, line:{ color:'FFFFFF', width:1, transparency:70 } });
    s.addText([{ text:l, options:{ fontSize:12, color:'CFE3D8', breakLine:true } },{ text:v, options:{ fontSize:19, bold:true, color:'FFFFFF' } }],
      { x, y:5.4, w, h:1.15, margin:0, valign:'middle', isTextBox:true, objectName:l });
  });

  // ---------- 2. ISINMA ----------
  pres.addSection({ title:'Isınma' });
  s = pres.addSlide({ masterName:'ICERIK', sectionTitle:'Isınma' });
  s.addText('01', { x:0.6, y:0.45, w:1.0, h:0.9, fontSize:44, bold:true, color:C.accent1, margin:0, isTextBox:true });
  s.addText('Isınma Oyunu', { x:1.65, y:0.45, w:7, h:0.9, fontFace:'Arial', fontSize:38, bold:true, color:C.text1, margin:0, valign:'middle', isTextBox:true, objectName:'Başlık' });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:10.4, y:0.55, w:2.33, h:0.7, rectRadius:0.35, fill:{ color:C.accent1 }, line:{ type:'none' }, objectName:'Süre rozeti' });
  s.addImage({ data: await icon(fa.FaStopwatch,'FFFFFF'), x:10.6, y:0.7, w:0.4, h:0.4 });
  s.addText('5-7 dakika', { x:11.05, y:0.55, w:1.6, h:0.7, fontSize:18, bold:true, color:'FFFFFF', margin:0, valign:'middle', isTextBox:true });

  // sol: bilgi kartları
  const info = [
    [fa.FaUsers,'Yaş grubu','10-11 yaş'],
    [fa.FaBullseye,'Amaç','Çeviklik, koordinasyon, dikkat ve yön değiştirme becerisini geliştirmek.'],
    [fa.FaToolbox,'Malzemeler','Kırmızı, sarı ve yeşil renkli huniler.'],
  ];
  const cardY=[1.75,3.15,4.95], cardH=[1.1,1.5,1.5];
  for (let i=0;i<3;i++){
    const [ic,lab,val]=info[i];
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:0.6, y:cardY[i], w:4.6, h:cardH[i], rectRadius:0.1, fill:{ color:C.background2 }, line:{ type:'none' }, objectName:lab+' kartı' });
    s.addShape(pres.shapes.OVAL, { x:0.85, y:cardY[i]+0.25, w:0.6, h:0.6, fill:{ color:C.accent1 }, line:{ type:'none' } });
    s.addImage({ data: await icon(ic,'FFFFFF'), x:1.0, y:cardY[i]+0.4, w:0.3, h:0.3 });
    s.addText([
      { text:lab, options:{ fontSize:13, bold:true, color:C.accent1, breakLine:true } },
      { text:val, options:{ fontSize:15, color:C.text1 } },
    ], { x:1.65, y:cardY[i]+0.15, w:3.4, h:cardH[i]-0.3, margin:0, valign:'top', isTextBox:true });
  }
  // malzeme huni ikonları
  cones.forEach((c,i)=> s.addShape(pres.shapes.ISOSCELES_TRIANGLE, { x:1.65+i*0.45, y:6.0, w:0.3, h:0.32, fill:{ color:c[0] }, line:{ type:'none' } }));

  // sağ: renk komut kartları + oynanış
  s.addText('Oyunun Oynanışı', { x:5.7, y:1.7, w:7, h:0.45, fontSize:22, bold:true, color:C.text1, margin:0, isTextBox:true });
  const cmds=[[HEX.accent1,'YEŞİL','Hafif tempoda koş'],[HEX.accent2,'SARI','Yavaş yürü'],[HEX.accent3,'KIRMIZI','Olduğun yerde dur']];
  cmds.forEach((c,i)=>{
    const x=5.7+i*2.4;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y:2.3, w:2.25, h:1.15, rectRadius:0.1, fill:{ color:c[0] }, line:{ type:'none' }, objectName:c[1]+' komutu' });
    s.addText([{ text:c[1], options:{ fontSize:18, bold:true, color: i===1?HEX.dk1:'FFFFFF', breakLine:true } },{ text:c[2], options:{ fontSize:14, color: i===1?HEX.dk1:'FFFFFF' } }],
      { x:x+0.2, y:2.3, w:1.95, h:1.15, margin:0, valign:'middle', isTextBox:true });
  });
  const steps=['Çocuklar oyun alanına dağılır.','Öğretmen renkleri söyleyerek komut verir.','Yeşil denildiğinde hafif tempoda koşarlar.','Sarı denildiğinde yavaş yürürler.','Kırmızı denildiğinde oldukları yerde dururlar.','Öğretmen zaman zaman yön değiştirme ve çift ayak sıçrama gibi ek komutlar verir.'];
  const stepColors=[HEX.dk2,HEX.dk2,HEX.accent1,'C99400',HEX.accent3,HEX.dk2];
  steps.forEach((t,i)=>{
    const y=3.65+i*0.5;
    s.addShape(pres.shapes.OVAL, { x:5.7, y:y+0.04, w:0.38, h:0.38, fill:{ color:stepColors[i] }, line:{ type:'none' } });
    s.addText(String(i+1), { x:5.7, y:y+0.04, w:0.38, h:0.38, fontSize:13, bold:true, color:'FFFFFF', align:'center', valign:'middle', margin:0, isTextBox:true });
    s.addText(t, { x:6.25, y, w:6.5, h:0.46, fontSize:15, color:C.text1, margin:0, valign:'middle', isTextBox:true });
  });

  // ---------- 3. ANA OYUN (VİDEO) ----------
  pres.addSection({ title:'Ana Oyun' });
  s = pres.addSlide({ masterName:'ICERIK', sectionTitle:'Ana Oyun' });
  s.addText('02', { x:0.6, y:0.45, w:1.0, h:0.9, fontSize:44, bold:true, color:C.accent6, margin:0, isTextBox:true });
  s.addText([{ text:'Ana Oyun: ', options:{ color:C.accent6 } },{ text:'Hız ve Engel Parkuru', options:{ color:C.text1 } }], { x:1.65, y:0.45, w:8.6, h:0.9, fontFace:'Arial', fontSize:34, bold:true, color:C.text1, margin:0, valign:'middle', isTextBox:true, objectName:'Başlık' });
  // video: 854x476 (1.794) -> 8.8 x 4.905
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:2.17, y:1.5, w:9.0, h:5.105, rectRadius:0.12, fill:{ color:C.text1 }, line:{ type:'none' }, objectName:'Video çerçevesi' });
  s.addMedia({ type:'video', path:'ana_oyun.mp4', cover:'data:image/png;base64,'+require('fs').readFileSync('poster.png').toString('base64'), x:2.27, y:1.6, w:8.8, h:4.905, objectName:'Ana oyun videosu' });

  // ---------- 4. SOĞUMA ----------
  pres.addSection({ title:'Soğuma' });
  s = pres.addSlide({ masterName:'ICERIK', sectionTitle:'Soğuma' });
  s.background = { color:'EAF4FA' };
  s.addText('03', { x:0.6, y:0.45, w:1.0, h:0.9, fontSize:44, bold:true, color:C.accent4, margin:0, isTextBox:true });
  s.addText([{ text:'Soğuma Oyunu: ', options:{ color:C.accent4 } },{ text:'Sakinleşen Bedenler', options:{ color:C.text1 } }], { x:1.65, y:0.45, w:8.6, h:0.9, fontFace:'Arial', fontSize:34, bold:true, margin:0, valign:'middle', isTextBox:true, objectName:'Başlık' });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:10.4, y:0.55, w:2.33, h:0.7, rectRadius:0.35, fill:{ color:C.accent4 }, line:{ type:'none' }, objectName:'Süre rozeti' });
  s.addImage({ data: await icon(fa.FaStopwatch,'FFFFFF'), x:10.6, y:0.7, w:0.4, h:0.4 });
  s.addText('4-5 dakika', { x:11.05, y:0.55, w:1.6, h:0.7, fontSize:18, bold:true, color:'FFFFFF', margin:0, valign:'middle', isTextBox:true });

  // üstte üç bilgi kartı yan yana
  const info2=[[fa.FaUsers,'Yaş grubu','10-11 yaş'],[fa.FaBullseye,'Amaç','Vücudu dinlendirmek, nefes kontrolünü sağlamak ve kasları gevşetmek.'],[fa.FaToolbox,'Malzemeler','Gerekmiyor.']];
  const iw=[2.9,5.6,3.0], ix=[0.6,3.75,9.6];
  for (let i=0;i<3;i++){
    const [ic,lab,val]=info2[i];
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:ix[i], y:1.7, w:iw[i], h:1.3, rectRadius:0.1, fill:{ color:'FFFFFF' }, line:{ type:'none' }, shadow:{ type:'outer', color:'000000', opacity:0.08, blur:6, offset:2, angle:90 }, objectName:lab+' kartı' });
    s.addShape(pres.shapes.OVAL, { x:ix[i]+0.25, y:1.95, w:0.55, h:0.55, fill:{ color:C.accent4 }, line:{ type:'none' } });
    s.addImage({ data: await icon(ic,'FFFFFF'), x:ix[i]+0.39, y:2.09, w:0.27, h:0.27 });
    s.addText([{ text:lab, options:{ fontSize:13, bold:true, color:C.accent4, breakLine:true } },{ text:val, options:{ fontSize:15, color:C.text1 } }],
      { x:ix[i]+0.95, y:1.85, w:iw[i]-1.15, h:1.0, margin:0, valign:'top', isTextBox:true });
  }
  // altta: daire üzerinde akış (motif: daire düzeni)
  s.addText('Oyunun Oynanışı', { x:0.6, y:3.3, w:6, h:0.45, fontSize:22, bold:true, color:C.text1, margin:0, isTextBox:true });
  const st2=[[fa.FaCircleNotch,'Çocuklar oyun alanında geniş bir daire oluşturur.'],[fa.FaCommentDots,'Öğretmen sakin bir ses tonuyla komutlar verir.'],[fa.FaWalking,'Herkes yavaşça yürümeye başlar.'],[fa.FaSyncAlt,'Ardından omuzlarını daireler çizerek hareket ettirir.'],[fa.FaWind,'Kollarını yukarı kaldırıp derin nefes alır, yavaşça indirirken nefes verir.'],[fa.FaChild,'Son olarak boyunlarını zorlamadan sağa ve sola çevirir, kollarını ve bacaklarını hafifçe esnetir.']];
  for (let i=0;i<6;i++){
    const col=i%3, row=Math.floor(i/3);
    const x=0.6+col*4.1, y=3.9+row*1.5;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w:3.9, h:1.3, rectRadius:0.1, fill:{ color:'FFFFFF' }, line:{ type:'none' }, objectName:'Adım '+(i+1) });
    s.addShape(pres.shapes.OVAL, { x:x+0.2, y:y+0.2, w:0.5, h:0.5, fill:{ color:C.accent5 }, line:{ type:'none' } });
    s.addImage({ data: await icon(st2[i][0], HEX.accent4), x:x+0.32, y:y+0.32, w:0.26, h:0.26 });
    s.addText(String(i+1), { x:x+0.2, y:y+0.78, w:0.5, h:0.35, fontSize:16, bold:true, color:C.accent4, align:'center', margin:0, isTextBox:true });
    s.addText(st2[i][1], { x:x+0.85, y:y+0.1, w:2.9, h:1.1, fontSize:14, color:C.text1, margin:0, valign:'middle', isTextBox:true });
  }

  await pres.writeFile({ fileName:'RKR207_Egitsel_Oyunlar.pptx' });
  await applyTheme('RKR207_Egitsel_Oyunlar.pptx', THEME);
})();
