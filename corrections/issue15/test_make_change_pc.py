#-*- coding:utf-8 -*-
"""test_make_change_pc.py
"""
from __future__ import print_function
import sys, re,codecs
import digentry

class Pcerror(object):
  def __init__(self,line):
   # sample line: tab-delimited 3 fields
   # <L>1	<pc>1-001	[1-001-a]
   # dummy property values
   self.line = line
   self.col1,self.col2,self.col3 = line.split('\t') # array with three parts
   # Retrieve L-value from col1
   m = re.search(r'^<L>([^ ]*)$',self.col1)
   if m == None:
     print('Pcerror. Error parsing col 1')
     exit(1)
   self.L = m.group(1) # eg. the '1' from '<L>1'
   # retrieve old <pc> value from col2
   m = re.search(r'^<pc>([^ ]*)$',self.col2)
   if m == None:
     print('Pcerror. Error parsing col 2')
     exit(1)
   self.oldpc = m.group(1)  # eg. '1-001'
   # retrieve newe <pc> value from col3
   m = re.search(r'^\[([^ ]*)\]$',self.col3)
   if m == None:
     print('Pcerror. Error parsing col 3')
     exit(1)
   self.newpc = m.group(1)  # eg. '1-001-a'
   
def init_pcrecs(filein):
 recs=[]  # list of Pcerror objects, to be returned
 dbg = False
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  for line in f:
   line = line.rstrip('\r\n') # remove line-ending character(s)
   rec = Pcerror(line) # parse line and get object
   recs.append(rec)  # add this record
 print(len(recs),"records read from",filein)
 if dbg:  # print out first 3 records 
  for i in range(0,3):
   rec = recs[i]
   print('record',i+1)  # why +1 ?
   print(' L = "%s"' % rec.L)
   print(' oldpc       = "%s"' % rec.oldpc)
   print(' newpc       = "%s"' % rec.newpc)
 
 return recs
           
class Change(object):
 def __init__(self,entry,pcrec):
  self.entry = entry
  self.pcrec = pcrec
  
def get_pcrec_for_entry(entry,pcrecs):
 """ Match on L
  Entry object has a dictionary entry.metad, by which L may be found
  
 """
 L = entry.metad['L']
 for pcrec in pcrecs:
  if pcrec.L == L:
   return pcrec
 # find which pcrec matches entry, and return that pcrec.
 # If no match is found, return None
 return None

def generate_changes(entries,pcrecs):
 """
  For each entry, we look at metaline.
    Example: <L>99<pc>1-004<k1>aklikA<k2>aklikA
  1. Find the Pcerror record with the same 'L'.
    example: <L>96	<pc>1-004	[1-004-b]
  2. Check that the pc value from metaline agrees with oldpc
  3. Replace oldpc with newpc in metaline:
    example: <L>99<pc>1-004-b<k1>aklikA<k2>aklikA
  4. generate a Change object
  Return the array of Change objects

  How to do step 1?  One way is a 'linear search':
  In our example, metaline L = 99
  for pcrec in pcrecs:
   if pcrec.L == L:
    return pcrec
  return None  # no match

  This works, but is slow.
   there are 42000+ records in pcrecs
  And this search must be done for each of the 42000 entries of skd.
  So roughly we have 42000*42000  
   (* 42000 42000) 1,764,000,000  almost 2 billion
 """
 changes = [] # computed by this function
 for entry in entries:
  pcrec = get_pcrec_for_entry(entry,pcrecs)
  if pcrec != None:
   # check that pc from entry is same as oldpc from pcrec
   metapc = entry.metad['pc']
   if metapc != pcrec.oldpc:
    print('generate_changes: Mismatch between metpc and oldpc')
    print('  metapc = ',metapc)
    print('   oldpc = ',oldpc)
    continue # don't make a change object
   # generate a change object 
   change = Change(entry,pcrec)
   changes.append(change)
  else:
   print('Could not find pcrec for entry',entry.metaline)
 print(len(changes),'lines that may need changes')
 return changes

def get_title(pcrecs):
 outarr = []
 outarr.append('; ===================================================')
 outarr.append('; PC (page-column) changes')
 outarr.append('; ===================================================')
 return outarr
               
def write_changes(fileout,changes,title):
 outrecs = [] # list of lines for each change
 outrecs.append(title)
 for change in changes:
  outarr = [] # lines for this change
  entry = change.entry
  pcrec = change.pcrec
  outarr.append('; -------------------------------------')
  oldmetaline = entry.metaline
  # replace <pc>X< in metaline with Y = newpc
  newpc = pcrec.newpc
  newmetaline = re.sub(r'<pc>(.*?)<','<pc>%s<' %newpc,oldmetaline)
  lnum = entry.linenum1  # line number of metaline in skd.txt
  outarr.append('%s old %s' %(lnum,oldmetaline))
  outarr.append(';')
  outarr.append('%s new %s' %(lnum,newmetaline))
  outrecs.append(outarr)
 with codecs.open(fileout,"w","utf-8") as f:
  for outarr in outrecs:
   for out in outarr:
    f.write(out+'\n')
 print(len(outrecs),"records written to",fileout)

if __name__=="__main__":
 filein = sys.argv[1] # skd.txt
 filein1 = sys.argv[2]  # skd.pc.values ... f
 fileout = sys.argv[3] # changes
 entries = digentry.init(filein)
 # entries = entries[:100]  # first 100 for testing
 pcrecs = init_pcrecs(filein1)
 changes = generate_changes(entries,pcrecs)
 title = get_title(pcrecs)
 write_changes(fileout,changes,title)
