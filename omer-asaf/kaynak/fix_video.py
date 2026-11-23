import sys, zipfile, shutil
src=sys.argv[1]; tmp=src+'.tmp'
TIMING='<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst><p:video><p:cMediaNode vol="80000"><p:cTn id="2" fill="hold" display="0"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst></p:cTn><p:tgtEl><p:spTgt spid="%s"/></p:tgtEl></p:cMediaNode></p:video></p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>'
import re
with zipfile.ZipFile(src) as zi, zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED) as zo:
    for it in zi.infolist():
        d=zi.read(it.filename)
        if re.match(r'ppt/slides/slide\d+\.xml$', it.filename):
            s=d.decode('utf8')
            v=s.find('<a:videoFile')
            m=re.match(r'<p:cNvPr id="(\d+)"', s[s.rfind('<p:cNvPr id="',0,v):]) if v>0 else None
            if m and '<p:timing>' not in s:
                s=s.replace('</p:clrMapOvr>','</p:clrMapOvr>'+TIMING%m.group(1),1)
                print('timing added', it.filename, 'spid', m.group(1))
                d=s.encode('utf8')
        ct = zipfile.ZIP_STORED if it.filename.endswith('.mp4') else zipfile.ZIP_DEFLATED
        zo.writestr(it, d, compress_type=ct)
shutil.move(tmp,src)
