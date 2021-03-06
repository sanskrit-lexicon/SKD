#-*- coding:utf-8 -*-
"""skd_transcode.py
 
 
"""
from __future__ import print_function
import sys, re,codecs
import transcoder
transcoder.transcoder_set_dir('transcoder')

def convert(line,tranin,tranout):
 # convert text  in '<s>X</s>'
 # for skd, there are believed to be two cases:
 # for lines within an entry.
 # [Page...]
 # other
 if line.startswith('[Page'):
  return line
 # for other lines, insert <s>X</s> around the line
 line = '<s>%s</s>'%line
 tagname = 's'
 def f(m):
  x = m.group(1)
  parts = re.split(r'(<.*?>)',x)
  newparts = []
  for part in parts:
   if part == None:
    newpart = ''
   elif part.startswith('<'):
    newpart = part
   else:
    #newpart = transcoder.transcoder_processString(part,tranin,tranout)
    newpart = transcode(part,tranin,tranout)
   newparts.append(newpart)
  y = ''.join(newparts)
  #z = '<s>%s</s>' % y
  z = y  # don't want '<s>' or '</s> for skd
  return z

 regex = '<s>(.*?)</s>'
 #lineout = transcoder.transcoder_processElements(line,tranin,tranout,tagname)
 lineout = re.sub(regex,f,line)
 return lineout

def print_unicode(x,u):
 """ Sample output:
x= a/MSa—BU/
0905 | अ | DEVANAGARI LETTER A
0951 | ॑ | DEVANAGARI STRESS SIGN UDATTA
0902 | ं | DEVANAGARI SIGN ANUSVARA
0936 | श | DEVANAGARI LETTER SHA
2014 | — | EM DASH
092D | भ | DEVANAGARI LETTER BHA
0942 | ू | DEVANAGARI VOWEL SIGN UU
0951 | ॑ | DEVANAGARI STRESS SIGN UDATTA
 """
 import unicodedata
 outarr = []
 for c in u:
  name = unicodedata.name(c)
  icode = ord(c)
  a = f"{icode:04X} | {c} | {name}"
  outarr.append(a)
 print('x=',x)
 for out in outarr:
  print(out)
 print()

def transcode(x,tranin,tranout):
 y = transcoder.transcoder_processString(x,tranin,tranout)
 #if True and (('|' in x) or ('Q' in x)):
 if False and ('~' in x):  # for debugging.
  print_unicode(x,y)
 return y

def convert_metaline(line,tranin,tranout):
 # '<k1>X<k2>Y'
 m = re.search('<k1>([^<]+)<k2>([^<]+)',line)
 x = m.group(0)  # entire match
 k1 = m.group(1)
 k2 = m.group(2)
 #k1a =transcoder.transcoder_processString(k1,tranin,tranout)
 #k2a =transcoder.transcoder_processString(k2,tranin,tranout)
 k1a = transcode(k1,tranin,tranout)
 k2a = transcode(k2,tranin,tranout)
 y = '<k1>%s<k2>%s' %(k1a,k2a)
 lineout = line.replace(x,y)
 if False and (tranin == 'slp1') and (tranout == 'deva'):
  if '/' in k2:
   print_unicode(k2,k2a)
 return lineout

if __name__=="__main__": 
 tranin = sys.argv[1]
 tranout = sys.argv[2]
 filein = sys.argv[3] #  xxx.txt (path to digitization of xxx
 fileout = sys.argv[4] # 
 
 with codecs.open(filein,"r","utf-8") as f:
  with codecs.open(fileout,"w","utf-8") as fout:
   inentry = False
   for iline,line in enumerate(f):
    line = line.rstrip('\r\n')
    if inentry:
     # inentry = True
     if line.startswith('<LEND>'):
      lineout = line
      inentry = False
     elif line.startswith('<L>'):  # error
      print('Error 1. Not expecting <L>')
      print("line # ",iline+1)
      print(line)
      exit(1)
     else:
      # keep looking for <LEND
      lineout = convert(line,tranin,tranout)
    else:
     # inentry = False
     if line.startswith('<L>'):
      lineout = convert_metaline(line,tranin,tranout)
      inentry = True
     elif line.startswith('<LEND>'): # error
      print('Error 2. Not expecting <LEND>')
      print("line # ",iline+1)
      print(line)
      exit(1)
     else:
      # line outside of <L>...<LEND>
      lineout = line
    fout.write(lineout+'\n')
    if False: # True:
     if iline > 10000:
      print('quit at iline=',iline)
      break
