#-*- coding:utf-8 -*-
"""vcp_skd_verb2n.py
  
"""
from __future__ import print_function
import sys, re,codecs
#from parseheadline import parseheadline
import transcoder
transcoder.transcoder_set_dir('transcoder')

def transcode_line(x,tranin,tranout):
 """ For VCP. Take into account xml-like markup
 """
 if re.search(r'^\[Page.*?\]$',x):
  return x
 parts = re.split(r'(<[^>]*>)',x)
 newparts = []
 for part in parts:
  if part.startswith('<'):
   newparts.append(part)
  else:
   newpart = transcoder.transcoder_processString(part,tranin,tranout)
   newparts.append(newpart)
 y = ''.join(newparts)
 return y


class Dhatu(object):
 def __init__(self,line,dictlo):
  self.dictlo = dictlo
  m = re.search(r'^;; Case ([0-9]+): L=(.*?), k1=(.*?), .*, mw=([^ ]*)',line)
  self.case,self.L,self.k1,self.mw = [m.group(i) for i in range(1,5)]
  self.lines = []

def check_unique(dictlo,recs1):
 d = {}
 for irec1,rec1 in enumerate(recs1):
  k = rec1.k
  if k not in d:
   d[k] = []
  d[k].append(rec1)

 keys = d.keys()
 keysdup = [k for k in keys if len(d[k]) != 1]
 print('check_unique',dictlo,len(keysdup),"repeated keys")
 for k in keysdup:
  a = d[k]
  print('  non-unique:',k,len(a))

def init_verbs(filein,dictlo):
 # slurp lines
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [line.rstrip('\r\n') for line in f]
 recs = []
 kprev = None
 for line in lines:
  if line.startswith(';;'):
   rec = Dhatu(line,dictlo)
   recs.append(rec)
  else:
   rec.lines.append(line)
 print(len(recs),'records from',filein)
 recs1 = merge_dups(recs)
 print(len(recs1),'records after merging duplicate headwords')
 check_unique(dictlo,recs1)
 return recs1

class MergeDups(object):
 def __init__(self,k,rec):
  self.k = k
  self.matchrecs = None
  self.recs = [rec]

def merge_dups(recs):
 ans = []
 k = None
 for rec in recs:
  if k != rec.k1:
   k = rec.k1
   m = MergeDups(k,rec)
   ans.append(m)
  else:
   m.recs.append(rec)
 if True:
  # check by count
  n = 0
  for a in ans:
   n = n + len(a.recs)
  if n == len(recs):
   print('merge_dups check ok')
  else:
   print('merge_dups problem:',n,len(recs))
 return ans

slp_from = "aAiIuUfFxXeEoOMHkKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzsh"
slp_to =   "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvw"
slp_from_to = str.maketrans(slp_from,slp_to)


def init_dict(dictlo,recs):
 d = {}
 for r in recs:
  k = r.k
  if k in d:
   print('init_dict duplicate',dictlo,k)
  d[k] = r
 return d

def mapcount1(dictlo,recs):
 neq = 0
 n = len(recs)
 for rec in recs:
  if rec.matchrecs != None:
   neq = neq + 1
 print('%s: %s records matched, %s records unmatched'%(dictlo,neq,n-neq))

def mapcount(vcp_recs,skd_recs):
 mapcount1('vcp',vcp_recs)
 mapcount1('skd',skd_recs)

def maprecs(vcp_recs,skd_recs,vcpskd):
 # dictionary for skd
 skddict = init_dict('skd',skd_recs)
 for vcp_rec in vcp_recs:
  vcp = vcp_rec.k
  if vcp in skddict:
   skd_rec = skddict[vcp]
   vcp_rec.matchrecs = skd_rec
   if skd_rec.matchrecs != None:
    print('maprecs warning 1',vcp)
   skd_rec.matchrecs = vcp_rec
  elif vcp in vcpskd:
   skd = vcpskd[vcp]
   if skd not in skddict:
    print('maprecs. Error',vcp,skd)
    exit(1)
   skd_rec = skddict[skd]
   vcp_rec.matchrecs = skd_rec
   if skd_rec.matchrecs != None:
    print('maprecs warning 2',vcp,skd)
   skd_rec.matchrecs = vcp_rec
 mapcount(vcp_recs,skd_recs)

def html_head():
 return """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>VCP-SKD unmatched verbs</title>

  <link rel="stylesheet" href="https://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
  <script>
  $( function() {
    $( "#accordion1" ).accordion({
      active : 'none', //false,  // All sections collapsed
      collapsible: true,
      autoHeight: false,
      navigation:true
     });
    $( "#accordion2" ).accordion({
      active : 'none', //false,  // All sections collapsed
      collapsible: true,
      autoHeight: false,
      navigation:true
     });

  } );
  </script>
<style>
 .upasarga {color: green;}
 table {}
 tr {}
 td  {border-style: groove;
   /*width: 45%;*/
    vertical-align: top;
  }
 td.vcp { padding-right:10px; padding-left:5px;}
 td.skd { padding-left:10px;}

#accordion1 .ui-accordion-content {
    max-height: 200px;
    /*width:95%;*/
    padding-left:0px;
    padding-right:0px;
}
#accordion2 .ui-accordion-content {
    max-height: 200px;
    /*width:95%;*/
    padding-left:0px;
    padding-right:0px;
}
#accordion1,#accordion2 {
    /*background-color: green; */
}
.panel {
    width:450px;
}
</style>
</head>
 """

def html_title():
 import datetime
 x = datetime.datetime.now()
 today = x.strftime("%B %d %Y")
 template = """
<body>

<h1> Unmatched verbs from VCP and SKD dictionaries. </h1>
<p>These are verb records from VCP dictionary which, thus far, are not matched
    with a verb record from SKD;  and vice-versa.
</p>
<p> %s
    
</p>
 
 """ % today
 return template

def line_adjust(line,tranout):
 tranin='slp1'
 if line.startswith('<>'):
  line1 = line.replace('<>','')
  return transcode_line(line1,tranin,tranout)
 if line.startswith('*<HI>'):
  line1 = line.replace('*<HI>','')
  line2 = transcode_line(line1,tranin,tranout)
  return '<span class="upasarga">%s</span>' %line2
 if line.startswith(';'):
  return ''
 return transcode_line(line,tranin,tranout)

def html_section_one(dictlo,recs,tranout):
 tranin='slp1'
 outarr = []
 outarr.append('<h3> %s </h3>'%dictlo)

 for rec in recs:
  k1 = rec.k1
  L = rec.L
  k1a = transcode_line(k1,tranin,tranout)
  outarr.append('<b> k1=%s, L=%s</b><br/>' %(k1a,L))
  lines = rec.lines
  for line in lines:
   line1 = line_adjust(line,tranout)
   outarr.append(line1 + '<br/>')
 out = '\n'.join(outarr)
 return out

def unused_html_section(imatch,vcp_mergerec,skd_mergerec,tranout):
 tranin='slp1'
 vcp = vcp_mergerec.k
 skd = skd_mergerec.k
 if vcp == skd:
  flag = ''
 else:
  flag = ' *'
 vcp1 = transcode_line(vcp,tranin,tranout)
 skd1 = transcode_line(skd,tranin,tranout)

 outarr = []
 outarr.append('<h2> Match %04d: vcp=%s, skd=%s%s</h2>' %(imatch,vcp1,skd1,flag))
 vcptxt = html_section_one('vcp',vcp_mergerec.recs,tranout)
 skdtxt = html_section_one('skd',skd_mergerec.recs,tranout)
 table = """
 <table class="oneverb">
  <tr>
   <td class="vcp">%s</td>
   <td class="skd">%s</td>
  </tr>
 </table>
 """%(vcptxt,skdtxt)
 outarr.append(table)
 return '\n'.join(outarr)

def html_section_onen(dictlo,recs,tranout):
 tranin='slp1'
 outarr = []

 for rec in recs:
  k1 = rec.k1
  L = rec.L
  k1a = transcode_line(k1,tranin,tranout)
  outarr.append('<b> k1=%s, L=%s</b><br/>' %(k1a,L))
  lines = rec.lines
  for line in lines:
   line1 = line_adjust(line,tranout)
   outarr.append(line1 + '<br/>')
 out = '\n'.join(outarr)
 return out

def html_panels(dictlo,mergerecs,tranout):
 tranin = 'slp1'
 outarr = []
 for imergerec,mergerec in enumerate(mergerecs):
  icase = imergerec+1
  k = mergerec.k
  k1 = transcode_line(k,tranin,tranout)
  outarr.append('<h2> Case %04d: %s=%s</h2>' %(icase,dictlo,k1))
  txt = html_section_onen(dictlo,mergerec.recs,tranout)
  outarr.append('<div class="panel">%s</div>' % txt)
 out = '\n'.join(outarr)
 return out

def write_nomatch(fileout,vcp_mergerecs,skd_mergerecs,tranout):
 tranin = 'slp1'
 n = 0
 htmlarr = [] # array of html strings
 htmlarr.append(html_head())
 htmlarr.append(html_title())
 varr = [r for r in vcp_mergerecs if r.matchrecs == None] # ~170+
 sarr = [r for r in skd_mergerecs if r.matchrecs == None] # ~100
 if False:  # debug
  varr = varr[0:20]
  sarr = sarr[0:20]
 htmlvcp = html_panels('vcp',varr,tranout)
 htmlskd = html_panels('skd',sarr,tranout)
 html0 = """
 <table>
  <tr><th>VCP</th><th>SKD</th></tr>
  <tr>
  <td class="panel"><div id="accordion1">%s</div></td>
  <td class="panel"><div id="accordion2">%s</div></td>
 </tr></table>
 """ %(htmlvcp,htmlskd)
 htmlarr.append(html0)
 htmlarr.append('</body></html>') 
 with codecs.open(fileout,"w","utf-8") as f:
  out = '\n'.join(htmlarr)
  f.write(out + '\n')
 print("html  written to",fileout)
 #print(nflag,"matches are approximate")

def init_vcp_skd_map(filein):
 # slurp lines
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [line.rstrip('\r\n') for line in f if not line.startswith(';')]
 d = {} # map from vcp to skd
 for line in lines:
  vcp,skd = line.split(':')
  if vcp in d:
   print('init_vcp_skd_map: duplicate found:',line)
  d[vcp] = skd
 return d

def test(tranout):
 x = 'rAma'
 tranin = 'slp1'
 y = transcode_line(x,tranin,tranout)
 y = transcoder.transcoder_processString(x,tranin,tranout)
 print('test: %s -> %s' %(x,y))
 exit(1)
def test1(vcp_recs,skd_recs):
 varr = [r for r in vcp_recs if r.matchrecs == None]
 sarr = [r for r in skd_recs if r.matchrecs == None]
 nvarr = len(varr)
 nsarr = len(sarr)
 print(nvarr,nsarr)
 fileout = 'temp_verb2n_test1.txt'
 f = codecs.open(fileout,"w","utf-8")
 for mr in sarr:
  k1 = mr.k
  Lcodes = [r.L for r in mr.recs]
  L_str = '/'.join(Lcodes)
  mwset = list(set([r.mw for r in mr.recs]))
  assert len(mwset) == 1
  mw = mwset[0]
  out = 'dict=%s, k1=%s, L=%s, mw=%s' %('skd',k1,L_str,mw)
  f.write(out+'\n')
 f.close()
 print('test1: %s unmatched skd verbs written to'%nsarr,fileout)
 exit(1)
if __name__=="__main__": 
 tranout = sys.argv[1] # deva or slp1
 filein = sys.argv[2] #  vcp_verb1
 filein1 = sys.argv[3] # skd_verb1
 filein2 = sys.argv[4] # vcp_skd_map
 fileout = sys.argv[5] # matches
 vcp_recs = init_verbs(filein,'vcp')
 skd_recs = init_verbs(filein1,'skd')
 vcpskd = init_vcp_skd_map(filein2)
 maprecs(vcp_recs,skd_recs,vcpskd)
 #test1(vcp_recs,skd_recs)
 
 write_nomatch(fileout,vcp_recs,skd_recs,tranout)
