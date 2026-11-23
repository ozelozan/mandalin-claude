const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell, WidthType,
  AlignmentType, ShadingType, BorderStyle, LevelFormat, PageBreak, HeadingLevel, Footer, PageNumber, VerticalAlign } = require('docx');

const NAVY='14213D', GREEN='1F7A4A', BLUE='2A6F97', MUTED='5B6770';
const FONT='Calibri', HFONT='Arial';
const CW = 9638; // A4 text width with 1" margins (11906-2*1134) -> use 2cm margins
const none = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const noBorders = { top:none, bottom:none, left:none, right:none };
const thin = (c)=>({ style: BorderStyle.SINGLE, size: 4, color: c });

const P = (runs, opts={}) => new Paragraph({ children: Array.isArray(runs)?runs:[runs], ...opts });
const T = (text, o={}) => new TextRun({ text, font: o.font||FONT, size: o.size||24, bold: o.bold, color: o.color, italics: o.italics, allCaps: o.caps });
const center = (runs, after=0, before=0) => P(runs, { alignment: AlignmentType.CENTER, spacing: { before, after } });

// ---------- Cover (follows sample cover order) ----------
const cover = [
  center([new ImageRun({ type:'png', data: fs.readFileSync('logo.png'), transformation:{ width:150, height:150 }, altText:{ title:'Logo', description:'İstanbul Aydın Üniversitesi logosu', name:'logo' } })], 360, 1200),
  center(T('İSTANBUL AYDIN ÜNİVERSİTESİ', { size:32, bold:true, color:NAVY, font:HFONT }), 60),
  center(T('Spor Bilimleri Fakültesi', { size:26, color:NAVY }), 900),
  center(T('RKR207 EĞİTSEL OYUNLAR DERSİ', { size:28, bold:true, color:GREEN, font:HFONT }), 600),
  center(T('“Hız ve Engel Parkuru”', { size:44, bold:true, color:NAVY, font:HFONT }), 120),
  center(T('10-11 Yaş Grubu İçin Isınma ve Soğuma Oyunları', { size:26, italics:true, color:MUTED }), 1600),
  center([T('Dersin Öğretim Üyesi: ', { size:24, color:MUTED }), T('Dr. Öğr. Üyesi Ayla Rezvan Reha', { size:24, bold:true, color:NAVY })], 120),
  center([T('Öğrenci No: ', { size:24, color:MUTED }), T('B2518.040050', { size:24, bold:true, color:NAVY })], 120),
  center([T('Öğrenci Ad ve Soyadı: ', { size:24, color:MUTED }), T('Ömer Asaf ÖZEL', { size:24, bold:true, color:NAVY })], 0),
  P(new PageBreak()),
];

// ---------- helpers for game sections ----------
function sectionTitle(no, title, color){
  return [
    P(T(no, { size:22, bold:true, color, font:HFONT, caps:true }), { spacing:{ after:40 } }),
    new Paragraph({ heading: HeadingLevel.HEADING_1, children:[ new TextRun({ text:title }) ] }),
  ];
}
function infoTable(rows, color, tint){
  const w1=2600, w2=CW-w1;
  return new Table({ width:{ size:CW, type:WidthType.DXA }, columnWidths:[w1,w2],
    rows: rows.map(([k,v])=> new TableRow({ children:[
      new TableCell({ width:{ size:w1, type:WidthType.DXA }, shading:{ type:ShadingType.CLEAR, color:'auto', fill:tint },
        borders:{ top:thin('FFFFFF'), bottom:thin('FFFFFF'), left:none, right:none }, verticalAlign: VerticalAlign.CENTER,
        margins:{ top:120, bottom:120, left:180, right:120 }, children:[ P(T(k,{ bold:true, color })) ] }),
      new TableCell({ width:{ size:w2, type:WidthType.DXA },
        borders:{ top:thin('E3E7EA'), bottom:thin('E3E7EA'), left:none, right:none }, verticalAlign: VerticalAlign.CENTER,
        margins:{ top:120, bottom:120, left:180, right:120 }, children:[ P(T(v,{ color:'1F2933' })) ] }),
    ]}))
  });
}
const h2 = (text, color) => new Paragraph({ heading: HeadingLevel.HEADING_2, children:[ new TextRun({ text, color }) ] });
const step = (ref, text) => new Paragraph({ numbering:{ reference:ref, level:0 }, spacing:{ after:120, line:300 }, children:[ T(text) ] });

// ---------- Warm-up ----------
const cmdW = Math.floor(CW/3);
const cmdCell = (fill, label, desc, dark) => new TableCell({ width:{ size:cmdW, type:WidthType.DXA }, shading:{ type:ShadingType.CLEAR, color:'auto', fill },
  borders:{ top:thin('FFFFFF'), bottom:thin('FFFFFF'), left:{ style:BorderStyle.SINGLE, size:24, color:'FFFFFF' }, right:{ style:BorderStyle.SINGLE, size:24, color:'FFFFFF' } },
  margins:{ top:160, bottom:160, left:160, right:160 }, verticalAlign: VerticalAlign.CENTER,
  children:[ center(T(label,{ bold:true, size:26, color: dark?NAVY:'FFFFFF', font:HFONT }),40), center(T(desc,{ size:22, color: dark?NAVY:'FFFFFF' })) ] });

const warm = [
  ...sectionTitle('Bölüm 1', 'Isınma Oyunu', GREEN),
  infoTable([
    ['Süre','5-7 dakika'],
    ['Yaş grubu','10-11 yaş'],
    ['Amaç','Çeviklik, koordinasyon, dikkat ve yön değiştirme becerisini geliştirmek.'],
    ['Malzemeler','Kırmızı, sarı ve yeşil renkli huniler.'],
  ], GREEN, 'E6F2EB'),
  h2('Renk Komutları', NAVY),
  new Table({ width:{ size:cmdW*3, type:WidthType.DXA }, columnWidths:[cmdW,cmdW,cmdW], rows:[ new TableRow({ children:[
    cmdCell('1F9D55','YEŞİL','Hafif tempoda koş'), cmdCell('F4B400','SARI','Yavaş yürü', true), cmdCell('E53935','KIRMIZI','Olduğun yerde dur') ] }) ] }),
  h2('Oyunun Oynanışı', NAVY),
  ...['Çocuklar oyun alanına dağılır.','Öğretmen renkleri söyleyerek komut verir.','Yeşil denildiğinde hafif tempoda koşarlar.','Sarı denildiğinde yavaş yürürler.','Kırmızı denildiğinde oldukları yerde dururlar.','Öğretmen zaman zaman yön değiştirme ve çift ayak sıçrama gibi ek komutlar verir.'].map(t=>step('warm',t)),
  P(new PageBreak()),
];

// ---------- Cool-down ----------
const cool = [
  ...sectionTitle('Bölüm 2', 'Soğuma Oyunu: Sakinleşen Bedenler', BLUE),
  infoTable([
    ['Süre','4-5 dakika'],
    ['Yaş grubu','10-11 yaş'],
    ['Amaç','Vücudu dinlendirmek, nefes kontrolünü sağlamak ve kasları gevşetmek.'],
    ['Malzemeler','Gerekmiyor.'],
  ], BLUE, 'E4EFF6'),
  h2('Oyunun Oynanışı', NAVY),
  ...['Çocuklar oyun alanında geniş bir daire oluşturur.','Öğretmen sakin bir ses tonuyla komutlar verir.','Herkes yavaşça yürümeye başlar.','Ardından omuzlarını daireler çizerek hareket ettirir.','Kollarını yukarı kaldırıp derin nefes alır, yavaşça indirirken nefes verir.','Son olarak boyunlarını zorlamadan sağa ve sola çevirir, kollarını ve bacaklarını hafifçe esnetir.'].map(t=>step('cool',t)),
];

const numCfg = (ref, color) => ({ reference: ref, levels:[{ level:0, format:LevelFormat.DECIMAL, text:'%1.', alignment:AlignmentType.LEFT,
  style:{ paragraph:{ indent:{ left:500, hanging:400 } }, run:{ bold:true, color, font:FONT } } }] });

const doc = new Document({
  creator: 'Ömer Asaf ÖZEL', title: 'RKR207 Eğitsel Oyunlar - Hız ve Engel Parkuru',
  styles: { default: { document: { run: { font: FONT, size: 24 } } },
    paragraphStyles: [
      { id:'Heading1', name:'Heading 1', basedOn:'Normal', next:'Normal', quickFormat:true, run:{ font:HFONT, size:40, bold:true, color:NAVY }, paragraph:{ spacing:{ before:0, after:360 }, keepNext:true, outlineLevel:0 } },
      { id:'Heading2', name:'Heading 2', basedOn:'Normal', next:'Normal', quickFormat:true, run:{ font:HFONT, size:28, bold:true, color:NAVY }, paragraph:{ spacing:{ before:480, after:200 }, keepNext:true, outlineLevel:1 } },
    ] },
  numbering: { config: [ numCfg('warm', GREEN), numCfg('cool', BLUE) ] },
  sections: [
    { properties: { page: { margin: { top:1134, bottom:1134, left:1134, right:1134 } }, titlePage: true },
      footers: {
        first: new Footer({ children:[ P(T('')) ] }),
        default: new Footer({ children:[ new Paragraph({ alignment: AlignmentType.CENTER, children:[ T('RKR207 Eğitsel Oyunlar  ·  ', { size:18, color:MUTED }), new TextRun({ children:[PageNumber.CURRENT], size:18, color:MUTED, font:FONT }) ] }) ] }) },
      children: [...cover, ...warm, ...cool] },
  ],
});
Packer.toBuffer(doc).then(b => fs.writeFileSync('RKR207_Egitsel_Oyunlar.docx', b));
