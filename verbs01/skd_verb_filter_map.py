#-*- coding:utf-8 -*-
"""skd_verb_filter_map.py
"""
from __future__ import print_function
import sys, re,codecs

class Skdverb(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  m = re.search(r'L=([^,]*), k1=([^,]*), k2=([^,]*)',line)
  self.L,self.k1,self.k2 = m.group(1),m.group(2),m.group(3)
  self.vcp=None
  self.mw = None
 
def init_skdverb(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Skdverb(x) for x in f if x.startswith(';; Case')]
 print(len(recs),"records read from",filein)
 return recs

class Vcpmw(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  self.vcp,self.mw = line.split(':')
 
def init_vcpmw(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Vcpmw(x) for x in f if not x.startswith(';')]
 print(len(recs),"records read from",filein)
 return recs

class MWVerb(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  self.k1,self.L,self.cat,self.cps,self.parse = line.split(':')
  self.used = False

def init_mwverbs(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [MWVerb(x) for x in f]
 print(len(recs),"mwverbs read from",filein)
 recs = [r for r in recs if r.cat == 'verb']
 #recs = [r for r in recs if r.cat in ['root','genuineroot']]
 #recs = [r for r in recs if r.cat == 'verb']
 print(len(recs),"verbs returned from mwverbs")
 d = {}
 for rec in recs:
  k1 = rec.k1
  if k1 in d:
   print('init_mwverbs: Unexpected duplicate',k1)
  d[k1] = rec
 return recs,d
map2mw_special = {
 'anca':'aYc',
 'aBa':'amB',
 'arcca':'arc',
 'ucCa':'uC',
 'udJa':'ujJ',  # sp? ujJa
 'urvva':'urv',
 'karjja':'karj',
 'karbba':'karb',
 'karvva':'karv',
 'kusma':'kusmaya',
 'krunca':'kruYc',
 'gardDa':'gfD',
 'GiRa':'GiRR',
 'canca':'caYc',
 'citra':'citraya',
 'cudqa':'cuqq',  # there is also cuqqa
 'jarcCa':'jarC',
 'jurvva':'jUrv', # ?
 'Rakza':'nakz',
 'Rarda':'nard',
 'RATa':'nAT',
 'RADa':'nAD',
 'DvAkza':'DvANkz',
 'baka':'vak',
 'Baqa':'BaRq',
 'Banja':'BaYj',
 'BfYa':'Bf',
 'munca':'muYc',
 'lata':'latAya',
 'raSa':'raSanAya',
 'vfca':'vfj',  # vfRakti
 'SUya':'SU',
 'Sraga':'SraNg',
 'zana':'san',
 'zarvva':'sarv',
 'zasta':'saMst',
 'zinBa':'simB',
 'sAma':'sAmaya',
 'suda':'sund',
 'sunBa':'sumB',
 'sranBa':'sramB',
 'srinBa':'srimB',
 'svUrcCa':'svUrC',
 'zila':'sil',
}
"""
 '':'',
 """
# MW: mark as verb
#+ 40722 olaj, 
#+ 44620 kark, 
#+ 220057 SU, 
# No need 217253.1 sil   (should there be Sil as a verb? 217253.1 sil)
#+ 241374 sAt,  
#+ 247218 sund, 
#+ 259867, svUrC
#
#+ MW correct: 11413.2 aBijYa  Change from H2B to H2
#+ new alternate spelling yOq  172935.1  alternate to yOw. 172935
# additions to vcp_mw_map
# 'kusma':'kusmaya', olaja:olaj, karka:kark

# skd corrections:
#+ 24660 Ba -> Baqa, 24661 Ba -> Baqa
#+ 25518 BnASa -> BrASa, 25520 BnAsa -> BrAsa
#+ 25519  BrAsa:  text changes Bn -> Br
#+ 34615 vuqa -> vruqa
#+ 36534 SraBa -> Srama  (print change?)
#+ 37043 za -> zU   (print change)
#+ 37112 zRuma -> zRusa   (print change).  Would match with mw 'snus' then
def map2mw(d,k1):
 if k1 in d:
  return k1
 if k1 in map2mw_special:
  return map2mw_special[k1]
 if not k1.endswith('a'):
  return None
 k = k1[0:-1] # remove final 'a'
 if k in d:
  return k
 k2 = re.sub(r'(.)\1',r'\1',k)
 if k2 in d:
  return k2
 return '?'

def skdmap(recs,vcpmw,mwd):
 vcpmwd = {}
 for r in vcpmw:
  vcp = r.vcp
  mw = r.mw
  if vcp in vcpmwd:
   print('duplicate vcp',vcp)
  vcpmwd[vcp] = mw

 for rec in recs:
  if rec.k1 in vcpmwd:
   rec.vcp = rec.k1
   rec.mw = vcpmwd[rec.k1]
   if rec.mw == '?':
    rec.mw = map2mw(mwd,rec.k1)
   continue
  rec.vcp='?'
  # try mw spelling directly
  rec.mw = map2mw(mwd,rec.k1)


def write(fileout,recs):
 n = 0

 with codecs.open(fileout,"w","utf-8") as f:
  for rec in recs:
   n = n + 1
   line = rec.line
   # add two fields
   mw = rec.mw
   if mw == None:
    mw = '?'
   out1 = "vcp=%s, mw=%s" %(rec.vcp,mw)
   # remove 'code' field
   line1 = re.sub(', code=.*$','',line)
   out = '%s, %s' %(line1,out1)
   f.write(out + '\n')
 print(n,"records written to",fileout)

if __name__=="__main__": 
 filein = sys.argv[1] #  skd_verb_filter.txt
 filein1 = sys.argv[2] # vcp_mw_map_init.txt
 filein2 = sys.argv[3] # mwverbs1
 fileout = sys.argv[4]

 recs = init_skdverb(filein)
 vcpmw = init_vcpmw(filein1)
 mwverbrecs,mwverbsd= init_mwverbs(filein2)
 skdmap(recs,vcpmw,mwverbsd)
 write(fileout,recs)
