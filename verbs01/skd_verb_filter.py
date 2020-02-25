#-*- coding:utf-8 -*-
"""skd_verb_filter.py
 
 
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
  self.markcode = None
  self.markline = None
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

def mark_entries_verb(entries):
 """ skd verbs: iti kavikalpadrumaH """

 for entry in entries:
  # first exclude known non-verbs
  k1 = entry.metad['k1']
  L  = entry.metad['L']
  code = None
  linenum1 = entry.linenum1  # integer line number of metaline
  datalines = entry.datalines
  # various forms of iti kavikalpadrumaH in first line
  if re.search(' iti kavikalpadrumaH',datalines[0]):
   code = 1
  elif re.search(' iti kavikalpa-',datalines[0]):
   code = 2
  elif re.search(' iti kavi-',datalines[0]):
   code = 3
  if code != None:
   entry.markcode = code
   entry.markline = datalines[0]
   entry.marklinenum=linenum1 + 1
   continue
  # patterns of first line that indicate non-verb
  
  if re.search(r' klI,',datalines[0]): # neuter
   continue
  if re.search(r' puM,',datalines[0]): # masculine 
   continue
  if re.search(r' strI,',datalines[0]): # feminine
   continue
  if re.search(r' tri,',datalines[0]): # 3-genders ?
   continue
  
  # patterns in additional lines
  for iline,line in enumerate(datalines):
   if iline == 0:  #handled above
    continue
   if re.search(' iti kavikalpadrumaH',line):
    code = 10
   elif re.search('<>iti kavikalpadrumaH',line):
    code = 11
   elif re.search(' iti kavikalpa-',line): 
    code = 12
   elif re.search(' iti kavi-',line):
    code = 13
   elif re.search('kavikalpalat',line):
    continue  # kavakalpalatA NOT a verb indicator
   elif L in ['8480','31310','37770','42132']:
    code = 14  # kUpa, varRa, sapa, hrapa
   elif re.search('[< ]kavi',line):
    # 13 cases.  These are alphabet letters
    pass
   if code != None:
    entry.markcode = code
    entry.markline = line
    entry.marklinenum=entry.linenum1 + (iline+1)
    break # for iline,line

def write(fileout,entries,tranout):
 tranin = 'slp1'
 n = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for irec,rec in enumerate(recs):
   entry = rec.entry
   if rec.line1.strip() != entry.datalines[0].strip():
    print(' rec.line1=',rec.line1)
    print('entry line=',entry.datalines[0])
    print('Error at record',irec+1)
    exit(1)
   upasargas=find_upasarga_lines(entry)
   k1 = entry.metad['k1']  
   L =  entry.metad['L']
   k2 = entry.metad['k2']
   if rec.mwverb == None:
    mw = '?'
   elif rec.mwverb == k1:
    mw = rec.mwverb + ' (same)'
   else:
    mw = rec.mwverb + ' (diff)'
   outarr = []
   outarr.append(';; Case %04d: L=%s, k1=%s, k2=%s, #upasargas=%s, mw=%s' %(irec+1,L,k1,k2,len(upasargas),mw))
   #outarr.append(rec.line1)
   for x in entry.datalines:
   #for x in upasargas:
    y = transcode_line(x,tranin,tranout)
    outarr.append(y)
   outarr.append(';' + ('-'*70))
   outarr.append(';')
   n = n + 1
   for out in outarr:
    f.write(out + '\n')
 print(n,"records written to",fileout)

def write1(fileout,recs):
 n = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for irec,rec in enumerate(recs):
   entry = rec.entry
   if rec.line1.strip() != entry.datalines[0].strip():
    print(' rec.line1=',rec.line1)
    print('entry line=',entry.datalines[0])
    print('Error at record',irec+1)
    exit(1)
   upasargas=find_upasarga_lines(entry)
   k1 = entry.metad['k1']  
   L =  entry.metad['L']
   k2 = entry.metad['k2']
   outarr = []
   outarr.append('; Case %04d: L=%s, k1=%s, k2=%s, #upasargas=%s' %(irec+1,L,k1,k2,len(upasargas)))
   outarr.append(rec.line1)
   for x in upasargas:
    outarr.append(x)
   outarr.append(';')
   n = n + 1
   for out in outarr:
    f.write(out + '\n')
 print(n,"records written to",fileout)

def find_entries(recs,entries):
 # dictionary for entries
 d = {}
 for entry in entries:
  d[entry.linenum1]= entry
 # 
 for irec,rec in enumerate(recs):
  try:
   linenum = int(rec.linenum)
  except:
   print('find_entries. bad linenum=',rec.linenum)
   print('record # ',irec+1)
   print('  line = ',rec.line)
   exit(1)
  rec.entry = d[linenum-1]

def write_verbs(fileout,entries):
 n = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for ientry,entry in enumerate(entries):
   code = entry.markcode
   if not code:
    continue
   n = n + 1
   outarr = []
   k1 = entry.metad['k1']  
   L =  entry.metad['L']
   k2 = entry.metad['k2']
   outarr.append(';; Case %04d: L=%s, k1=%s, k2=%s, code=%s' %(n,L,k1,k2,code))
   linenum = entry.marklinenum
   line = entry.markline
   outarr.append('%6s: %s'%(linenum,line))
   outarr.append(';')
   for out in outarr:
    f.write(out+'\n')
 print(n,"verbs written to",fileout)

if __name__=="__main__": 
 filein = sys.argv[1] #  xxx.txt (path to digitization of xxx
 fileout = sys.argv[2] # 
 entries = init_entries(filein)
 mark_entries_verb(entries)
 write_verbs(fileout,entries)
 exit(1)
 dhatus = init_verbs(filein1)
 mark_entries_verb(entries)
 find_entries(dhatus,entries)
 mwverbs,mwverbsd = init_mwverbs(filein2)
 mwverbmap(mwverbsd,dhatus)
 write(fileout,dhatus,tranout)
