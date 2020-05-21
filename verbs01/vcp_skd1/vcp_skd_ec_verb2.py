#-*- coding:utf-8 -*-
"""vcp_skd_ec_verb2.py
  
"""
from __future__ import print_function
import sys, re,codecs
from verb_ec import ECverb
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
 d = {}
 for line in lines:
  if line.startswith(';;'):
   rec = Dhatu(line,dictlo)
   recs.append(rec)
   d[rec.L] = rec
  else:
   rec.lines.append(line)
 print(len(recs),'records from',filein)
 return recs,d
 #recs1 = merge_dups(recs)
 #print(len(recs1),'records after merging duplicate headwords')
 #check_unique(dictlo,recs1)
 #return recs1

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

def maprecs(vcp_recs,skd_recs,vcpskdr):
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

from string import Template
def html_head(dict1,dict2):
 template = Template( """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">

  <title>${d1}-${d2} verbs</title>

  <link rel="stylesheet" href="https://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
  <script>
  $( function() {
    $( "#accordion" ).accordion({
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
   width: 45%;
    vertical-align: top;
  }
 td.section1 { padding-right:10px; padding-left:5px;}
 td.section2 { padding-left:10px;}

#accordion .ui-accordion-content {
    max-height: 200px;
}
 
</style>
</head>
 """)
 s = template.safe_substitute(d1 = dict1.upper(), d2 = dict2.upper())
 return s

def html_title(dict1,dict2):
 import datetime
 x = datetime.datetime.now()
 today = x.strftime("%B %d %Y")
 template = Template("""
<body>

<h1> Comparison of verbs from ${d1} and ${d2} dictionaries. </h1>
<p> ${today}
    
</p>
<div id="accordion">
 
 """)
 s = template.safe_substitute(d1 = dict1.upper(), d2 = dict2.upper(),
    today=today)
 return s

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

def html_section_one(dictlo,ec,dL,tranout):
 tranin='slp1'
 outarr = []
 outarr.append('<h3> %s </h3>'%dictlo)
 
 for rec in ec.entries:
  k1 = rec.k1
  L = rec.L
  k1a = transcode_line(k1,tranin,tranout)
  outarr.append('<b> k1=%s, L=%s</b><br/>' %(k1a,L))
  rec = dL[L]  # dhatu object
  lines = [l for l in rec.lines if not l.startswith('[Page')]
  for iline,line in enumerate(lines):
   if iline > 2:
    line1 = '<i>... etc.  etc. etc. ...</i>'
    outarr.append(line1 + '<br/>')
    break
   else:
    line1 = line_adjust(line,tranout)
    outarr.append(line1 + '<br/>')
 out = '\n'.join(outarr)
 return out

def ec_keystr(ec):
 if ec.entries == []:
  return '?'
 keys = []
 for entry in ec.entries:
  k = entry.k1
  if k not in keys:
   keys.append(k)
 return ','.join(keys)

def html_section(imatch,ec1,ec2,flag,d1,d2,dict1,dict2,tranout):
 tranin='slp1'
 ec1keystr = ec_keystr(ec1)
 ec2keystr = ec_keystr(ec2)
 key1 = transcode_line(ec1keystr,tranin,tranout)
 key2 = transcode_line(ec2keystr,tranin,tranout)

 outarr = []
 outarr.append('<h2>%s=%s, %s=%s%s</h2>' %(dict1,key1,dict2,key2,flag))
 ec1txt = html_section_one(dict1,ec1,d1,tranout)
 ec2txt = html_section_one(dict2,ec2,d2,tranout)
 table = """
 <table class="oneverb">
  <tr>
   <td class="section1">%s</td>
   <td class="section2">%s</td>
  </tr>
 </table>
 """%(ec1txt,ec2txt)
 outarr.append(table)
 return '\n'.join(outarr)

def write(fileout,ecrecs,d1,d2,dict1,dict2,tranout):
 tranin = 'slp1'
 n = 0
 nflag = 0
 neq = 0
 htmlarr = [] # array of html strings
 htmlarr.append(html_head(dict1,dict2))
 htmlarr.append(html_title(dict1,dict2))
 
 if True:  # just for indenting
  imatch = 0
  for iecrec,ecrec in enumerate(ecrecs):
   ec1,ec2,flag = ecrec
   imatch = imatch + 1
   #if imatch == 50: #dbg
   # break
   htmlarr.append(html_section(imatch,ec1,ec2,flag,d1,d2,dict1,dict2,tranout))
   n = n + 1
 htmlarr.append('</div></body></html>') 
 with codecs.open(fileout,"w","utf-8") as f:
  out = '\n'.join(htmlarr)
  f.write(out + '\n')
 print(n,"records written to",fileout)
 #print(nflag,"matches are approximate")

def unused_write_match(fileout,vcp_mergerecs,tranout):
 tranin = 'slp1'
 n = 0
 nflag = 0
 neq = 0
 htmlarr = [] # array of html strings
 htmlarr.append(html_head())
 htmlarr.append(html_title())

 if True:  # just for indenting
  imatch = 0
  for vcp_mergerec in vcp_mergerecs:
   skd_mergerec = vcp_mergerec.matchrecs
   if skd_mergerec == None:
    continue # not a match
   imatch = imatch + 1
   #if imatch == 50:
   # break
   htmlarr.append(html_section(imatch,vcp_mergerec,skd_mergerec,tranout))
   n = n + 1
 htmlarr.append('</div></body></html>') 
 with codecs.open(fileout,"w","utf-8") as f:
  out = '\n'.join(htmlarr)
  f.write(out + '\n')
 print(n,"records written to",fileout)
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

def init_ec_map_helper1(x,dictname):
 #  vcp=ama,3749;ama,3750
 dname,ecstring = x.split('=')
 assert dname == dictname
 # we don't need these class dictionaries
 ECverb.dk = {}
 ECverb.dL = {}
 if ecstring == '?':
  ec = ECverb('') # empty
 else:
  ec = ECverb(ecstring)
 return ec

def init_ec_map_helper(line,dict1,dict2):
 """
 vcp=ama,3749;ama,3750 skd=ama,1827;ama,1828
 vcp=arca,4372;arca,4373 skd=arcca,2184;arcca,2185 (*)
 """
 line = line.rstrip('\r\n')
 parts = line.split(' ')
 ec1 = init_ec_map_helper1(parts[0],dict1)
 ec2 = init_ec_map_helper1(parts[1],dict2)
 if len(parts) == 2:
  flag = ''
 else:
  flag = parts[2]
 return (ec1,ec2,flag)

def init_ec_map(filein,dict1,dict2):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  recs = []
  for line in f:
   rec = init_ec_map_helper(line,dict1,dict2) # a 3-tuple: ec1, ec2, flag
   recs.append(rec)
 print("init_ec_map",len(recs),"read from",filein)
 return recs
if __name__=="__main__": 
 tranout = sys.argv[1] # deva or slp1
 filein = sys.argv[2] #  vcp_verb1
 filein1 = sys.argv[3] # skd_verb1
 filein2 = sys.argv[4]  # vcp_skd_ec_map.txt
 fileout = sys.argv[5] # 
 dict1 = 'vcp'
 dict2 = 'skd'
 vcp_recs,vcp_d = init_verbs(filein,dict1)
 skd_recs,skd_d = init_verbs(filein1,dict2)
 ecrecs = init_ec_map(filein2,dict1,dict2) # array of 3-tuples
 write(fileout,ecrecs,vcp_d,skd_d,dict1,dict2,tranout)
