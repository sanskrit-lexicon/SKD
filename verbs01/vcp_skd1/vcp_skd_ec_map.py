#-*- coding:utf-8 -*-
"""vcp_skd_ec_map.py
  
"""
from __future__ import print_function
import sys, re,codecs
from verb_ec import init_manual_ecs,ECverb
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

def unused_check_unique(dictlo,recs1):
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

class unused_MergeDups(object):
 def __init__(self,k,rec):
  self.k = k
  self.matchrecs = None
  self.recs = [rec]

def unused_merge_dups(recs):
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

def unused_init_dict(dictlo,recs):
 d = {}
 for r in recs:
  k = r.k
  if k in d:
   print('init_dict duplicate',dictlo,k)
  d[k] = r
 return d

def unused_mapcount1(dictlo,recs):
 neq = 0
 n = len(recs)
 for rec in recs:
  if rec.matchrecs != None:
   neq = neq + 1
 print('%s: %s records matched, %s records unmatched'%(dictlo,neq,n-neq))

def mapcount(vcp_recs,skd_recs):
 mapcount1('vcp',vcp_recs)
 mapcount1('skd',skd_recs)

def unused_maprecs(vcp_recs,skd_recs,vcpskdr):
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

  <title>VCP-SKD verbs</title>

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
 td.vcp { padding-right:10px; padding-left:5px;}
 td.skd { padding-left:10px;}

#accordion .ui-accordion-content {
    max-height: 200px;
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

<h1> Comparison of verbs from VCP and SKD dictionaries. </h1>
<p> %s
    
</p>
<div id="accordion">
 
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

def html_section(imatch,vcp_mergerec,skd_mergerec,tranout):
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

def write_match(fileout,vcp_mergerecs,tranout):
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
 d1 = {} # map from vcp to skd
 d2 = {} # map from skd to vcp
 for line in lines:
  vcp,skd = line.split(':')
  if vcp in d1:
   print('init_vcp_skd_map: duplicate 1 found:',line,vcp)
  d1[vcp] = skd
  if skd in d2:
   print('init_vcp_skd_map: duplicate 2 found:',line,skd)
  d2[skd] = vcp
 return d1,d2

def test(tranout):
 x = 'rAma'
 tranin = 'slp1'
 y = transcode_line(x,tranin,tranout)
 y = transcoder.transcoder_processString(x,tranin,tranout)
 print('test: %s -> %s' %(x,y))
 exit(1)

def init_ecs(filein):
 ECverb.dk = {}
 ECverb.dL = {}
 ecs = init_manual_ecs(filein)
 return ecs,ECverb.dk,ECverb.dL

def mapclassa(ecs1,ecs2_dk,d12,which):
 for ec1 in ecs1:
  ec1.matches = []
  for entry in ec1.entries:
   k1 = entry.k1
   if (k1 in ecs2_dk) and (k1 in d12):
    print('mapclassa %s WARNING 1: %s'%(which,k1))
   if k1 in ecs2_dk:
    ec2 = ecs2_dk[k1]  # equivalence classes containing k1
    ec1.matches.append(ec2)
   if k1 in d12:
    k2 = d12[k1]
    if k2 in ecs2_dk:
     ec2 = ecs2_dk[k2]
     ec1.matches.append(ec2)
    else:
     print('mapclassa %s WARNING 2: %s class not found'%(which,k2))

def mapclass(ecs1,ecs1_dk,ecs2,ecs2_dk,d12,d21,dict1,dict2):
 mapclassa(ecs1,ecs2_dk,d12,'%s-%s'%(dict1,dict2))
 mapclassa(ecs2,ecs1_dk,d21,'%s-%s'%(dict2,dict1))

def get_ec_rep(ecs,dictid):
 # sort the k1 values of the entries, and pick the alphabetically smallest
 for ec in ecs:
  keys = [entry.k1 for entry in ec.entries]
  keys.sort(key = lambda k : k.translate(slp_from_to))
  ec.rep = keys[0]

def get_all_reps(ecs1,ecs2):
 #reps1 = [ec.rep for ec in ecs1]
 d = {}
 for ec1 in ecs1:
  if ec1.matches != []:
   ec2 = ec1.matches[0]  # take first one
   #d[ec2.rep] = [ec1,ec2]
   d[ec1.rep] = [ec1,ec2]
  else:
   ec2 = None
   d[ec1.rep] = [ec1,ec2]
  if ec1.rep == 'arca':print(ec1.toString('slp1','slp1')," <-> ",ec2.toString('slp1','slp1'))
 #reps1.sort(key = lambda k : k.translate(slp_from_to))
 for ec2 in ecs2:
  if ec2.matches != []:
   continue
  k = ec2.rep
  if k in d:
   ec1 = d[k][0]
   if d[k][1] == None:
    d[k][1] = ec2
  elif ec2.matches != []:
   ec1 = ec2.matches[0] # take first one
   d[k] = [ec1,ec2]
  else:
   d[k] = [None,ec2]
  #if k == '
 keys = sorted(d.keys(),key = lambda k : k.translate(slp_from_to))
 return d,keys

def write_all_helper(ec,tranin,tranout):
 if ec == None:
  return '?'
 else:
  return ec.toString(tranin,tranout)
def write_all_flag(ec1,ec2):
 if (ec1 == None) or (ec2 == None):
  return ''
 k1unique = list(set([entry.k1 for entry in ec1.entries]))
 k2unique = list(set([entry.k1 for entry in ec2.entries]))
 if k1unique == k2unique:
  flag = ''
 else:
  flag = ' (*)'
 return flag

def write_all(fileout,all_reps,dall,tranout,dict1,dict2):
 tranin = 'slp1'
 no_out1 = 0
 no_out2 = 0
 nflag = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for rep in all_reps:
   ec1,ec2 = dall[rep]
   out1 = write_all_helper(ec1,tranin,tranout)
   out2 = write_all_helper(ec2,tranin,tranout)
   flag = write_all_flag(ec1,ec2)
   out = '%s=%s %s=%s%s'%(dict1,out1,dict2,out2,flag)
   f.write(out+'\n')
   if out1 == '?': no_out1 = no_out1 + 1
   if out2 == '?': no_out2 = no_out2 + 1
   if flag != '': nflag = nflag + 1
 n = len(all_reps)
 print(n,"records written to",fileout)
 print('%s cases where %s is unmatched' % (no_out1,dict2))
 print('%s cases where %s is unmatched' % (no_out2,dict1))
 nmatch = n - no_out1 - no_out2
 print('%s cases where match is found' % nmatch)
 print('%s cases where the match has spelling variations' %nflag)

if __name__=="__main__": 
 tranout = sys.argv[1] # deva or slp1
 fileinec1 = sys.argv[2]  # vcp_ecs.txt
 fileinec2 = sys.argv[3]  # skd_ecs.txt
 filein2 = sys.argv[4] # vcp_skd_map
 fileout = sys.argv[5] # vcp_skd_ec_map.txt
 dict1 = 'vcp'
 dict2 = 'skd'
 print("reading",fileinec1)
 vcp_ecs,vcp_dk,vcp_dL = init_ecs(fileinec1)
 print("reading",fileinec2)
 skd_ecs,skd_dk,skd_dL = init_ecs(fileinec2)

 vcpskd,skdvcp = init_vcp_skd_map(filein2)
 # update vcp_ecs, skd_ecs by adding 'matches' attribute to each 
 # equivalence class.
 mapclass(vcp_ecs,vcp_dk,skd_ecs,skd_dk,vcpskd,skdvcp,dict1,dict2)
 # get a representative of each equivalence class
 get_ec_rep(vcp_ecs,dict1)
 get_ec_rep(skd_ecs,dict2)
 dall,all_reps = get_all_reps(vcp_ecs,skd_ecs)

 write_all(fileout,all_reps,dall,tranout,dict1,dict2)
 exit(0)
 #maprecs(vcp_ecs,skd_ecs,vcpskd)
 #maprecs(vcp_recs,skd_recs,vcpskd)
 #write_match(fileout,vcp_recs,tranout)
