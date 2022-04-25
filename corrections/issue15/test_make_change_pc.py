#-*- coding:utf-8 -*-
"""test_make_change_pc.py
"""
from __future__ import print_function
import sys, re,codecs
import digentry

class Pcerror(object):
  def __init__(self,line):
   # dummy property values
   self.line = line
   self.oldmetaline = re.sub(r"(:<pc>.*$)|(\s)", "", line)
   self.newpc = re.sub(r"<L>.+:<pc>", "", line)
   self.newmetaline = re.sub(r"<pc>.+<k1>", "<pc>" + self.newpc + "<k1>", self.oldmetaline)

def init_pcrecs(filein):
 recs=[]  # list of Pcerror objects, to be returned
 dbg = True
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
   print(' oldmetaline = "%s"' % rec.oldmetaline)
   print(' newpc       = "%s"' % rec.newpc)
   print(' newmetaline = "%s"' % rec.newmetaline)
 return recs
           
class Change(object):
 def __init__(self,entry,pcrec):
  self.entry = entry
  self.pcrec = pcrec
  
def get_pcrec_for_entry(entry,pcrecs):
 for pcrec in pcrecs:
  if pcrec.oldmetaline == entry.metaline:
   return pcrec
 # find which pcrec matches entry, and return that pcrec.
 # If no match is found, return None
 return None

def generate_changes(entries,pcrecs):
 changes = [] # computed by this function
 for entry in entries:
  pcrec = get_pcrec_for_entry(entry,pcrecs)
  if pcrec != None:
   # generate a change object 
   change = Change(entry,pcrec)
   changes.append(change)
 print(len(changes),'lines that may need changes')
 return changes

def get_title(pcrecs):
 outarr = []
 outarr.append('; ===================================================')
 outarr.append('; PC (page-column) ERRORS correction')
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
  metaline = entry.metaline
  metaline1 = re.sub(r'<k2>.*$','',metaline)  # just show L,pc,k1
  oldmetaline = pcrec.oldmetaline
  newmetaline = pcrec.newmetaline
  lnum = entry.linenum1
  outarr.append('; %s' %metaline1)
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
 filein = sys.argv[1] #  xxx.txt
 filein1 = sys.argv[2]  # pcerrors.txt
 fileout = sys.argv[3] # changes
 entries = digentry.init(filein)
 pcrecs = init_pcrecs(filein1)
 changes = generate_changes(entries,pcrecs)
 title = get_title(pcrecs)
 write_changes(fileout,changes,title)
