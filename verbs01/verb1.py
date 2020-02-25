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

def write(fileout,recs,tranout):
 tranin = 'slp1'
 n = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for irec,rec in enumerate(recs):
   entry = rec.entry
   assert rec.L == entry.metad['L']
   assert rec.k1 == entry.metad['k1']
   """
   if rec.mw == None:
    mw = '?'
   elif rec.mw == k1:
    mw = rec.mw + ' (same)'
   else:
    mw = rec.mw + ' (diff)'
   """
   outarr = []
   outarr.append(rec.line)
   for x in entry.datalines:
    y = transcode_line(x,tranin,tranout)
    outarr.append(y)
   outarr.append(';' + ('-'*70))
   outarr.append(';')
   n = n + 1
   for out in outarr:
    f.write(out + '\n')
 print(n,"records written to",fileout)

class Dhatu(object):
 def __init__(self,line):
  line = line.rstrip('\r\n')
  self.line = line
  m = re.search(r'^;; Case ([0-9]+): L=(.*?), k1=(.*?), k2=(.*?), vcp=(.*?), mw=(.*?)$',line)
  self.case,self.L,self.k1,self.k2,self.vcp,self.mw = [m.group(i) for i in range(1,7)]
  self.entry = None

def init_verbs(filein):
 # slurp lines
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  recs = [Dhatu(line) for line in f if line.startswith(';;')]
 print(len(recs),'records from',filein)
 return recs

def find_entries(recs,entries):
 # dictionary for entries
 d = {}
 for entry in entries:
  L = entry.metad['L']
  d[L]= entry
 # 
 for irec,rec in enumerate(recs):
  L = rec.L
  rec.entry = d[L]

if __name__=="__main__": 
 tranout = sys.argv[1] # deva or slp1
 filein = sys.argv[2] #  xxx.txt (path to digitization of xxx
 filein1 = sys.argv[3] # skd_verb_filter_map.txt
 fileout = sys.argv[4] # 
 entries = init_entries(filein)
 dhatus = init_verbs(filein1)
 find_entries(dhatus,entries)
 write(fileout,dhatus,tranout)
