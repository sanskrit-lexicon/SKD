#-*- coding:utf-8 -*-
"""verb1.py
 
 
"""
from __future__ import print_function
import sys, re,codecs
from parseheadline import parseheadline
import transcoder
transcoder.transcoder_set_dir('transcoder')

class Entry(object):
 Ldict = {}
 def __init__(self,lines,linenum1,linenum2):
  # linenum1,2 are int
  self.metaline = lines[0]
  self.lend = lines[-1]  # the <LEND> line
  self.datalines = lines[1:-1]  # the non-meta lines
  # parse the meta line into a dictionary
  #self.meta = Hwmeta(self.metaline)
  self.metad = parseheadline(self.metaline)
  self.linenum1 = linenum1
  self.linenum2 = linenum2
  #L = self.meta.L
  L = self.metad['L']
  if L in self.Ldict:
   print("Entry init error: duplicate L",L,linenum1)
   exit(1)
  self.Ldict[L] = self
  #  extra attributes
  self.marked = False # from a filter of markup associated with verbs
  self.marks = []  # verb markup markers, in order found, if any

def init_entries(filein):
 # slurp lines
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [line.rstrip('\r\n') for line in f]
 recs=[]  # list of Entry objects
 inentry = False  
 idx1 = None
 idx2 = None
 for idx,line in enumerate(lines):
  if inentry:
   if line.startswith('<LEND>'):
    idx2 = idx
    entrylines = lines[idx1:idx2+1]
    linenum1 = idx1 + 1
    linenum2 = idx2 + 1
    entry = Entry(entrylines,linenum1,linenum2)
    recs.append(entry)
    # prepare for next entry
    idx1 = None
    idx2 = None
    inentry = False
   elif line.startswith('<L>'):  # error
    print('init_entries Error 1. Not expecting <L>')
    print("line # ",idx+1)
    print(line.encode('utf-8'))
    exit(1)
   else: 
    # keep looking for <LEND>
    continue
  else:
   # inentry = False. Looking for '<L>'
   if line.startswith('<L>'):
    idx1 = idx
    inentry = True
   elif line.startswith('<LEND>'): # error
    print('init_entries Error 2. Not expecting <LEND>')
    print("line # ",idx+1)
    print(line.encode('utf-8'))
    exit(1)
   else: 
    # keep looking for <L>
    continue
 # when all lines are read, we should have inentry = False
 if inentry:
  print('init_entries Error 3. Last entry not closed')
  print('Open entry starts at line',idx1+1)
  exit(1)

 print(len(lines),"lines read from",filein)
 print(len(recs),"entries found")
 return recs


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

merge_manualcases = [
 # vcp, skd
 ('uCa','ucCa'),
 ('karRRa','karR'),
 ('glunca','gluYca'),
 ('GiRRa','GiRa'),
 ('Jf','JF'),
 ('zarba','zarvva'),
 ('zimBa','zinBa'),
 ('sarba','sarvva'),
 ('stanBa','staBa'), # or stamBa skd
 ('srimBa','srinBa'),
 ('svurcCa','svUrcCa'),
 ('',''),

]
def merge_approx_match(r1,r2):
 if re.sub(r'r(.)\1',r'r\1',r1.k) == re.sub(r'r(.)\1',r'r\1',r2.k): 
  return True
 if re.sub(r'a$',r'',r1.k) == re.sub(r'a$',r'',r2.k): 
  return True
 if (r1.k,r2.k) in merge_manualcases:
  return True
 return False
def merge(recs1,recs2):
 #check_unique('vcp',recs1)
 #check_unique('skd',recs1)
 ans = []
 n1 = len(recs1)
 n2 = len(recs2)
 i1 = 0
 i2 = 0
 while (i1<n1) and (i2<n2):
  r1 = recs1[i1]
  r2 = recs2[i2]
  if r1.k == r2.k:
   ans.append([r1,r2])
   i1 = i1+1
   i2 = i2+1
   continue
  if merge_approx_match(r1,r2):
   ans.append([r1,r2])
   i1 = i1+1
   i2 = i2+1
   continue
  # no match or approximate match found. Proceed by alphabetical order
  if r1.k.translate(slp_from_to) < r2.k.translate(slp_from_to):
   ans.append([r1,None])
   i1 = i1 + 1
  else:
   ans.append([None,r2])
   i2 = i2 + 1
 return ans

def write(fileout,mergerecs,tranout):
 tranin = 'slp1'
 n = 0
 nflag = 0
 neq = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for imerge,mergerec in enumerate(mergerecs):
   vcprec,skdrec = mergerec
   if vcprec == None:
    out1 = '?'
   else:
    out1 = vcprec.k
   if skdrec == None:
    out2 = '?'
   else:
    out2 = skdrec.k
   outarr = []
   if (vcprec != None) and (skdrec != None) and (out1 != out2):
    flag = ' *'
    nflag = nflag + 1
   else:
    flag = ''
   outarr.append('vcp=%s, skd=%s%s'%(out1,out2,flag))
   if flag != '':
    print('%s:%s'%(vcprec.k,skdrec.k))
   n = n + 1
   for out in outarr:
    f.write(out + '\n')
 print(n,"records written to",fileout)
 print(nflag,"matches are approximate")

if __name__=="__main__": 
 tranout = sys.argv[1] # deva or slp1
 filein = sys.argv[2] #  vcp_verb1
 filein1 = sys.argv[3] # skd_verb1
 fileout = sys.argv[4] # 
 vcp_recs = init_verbs(filein,'vcp')
 skd_recs = init_verbs(filein1,'skd')
 mergerecs = merge(vcp_recs,skd_recs)
 write(fileout,mergerecs,tranout)
