"""convert.py
  Python example of transcoding
"""
from __future__ import print_function
import sys,codecs,re
sys.path.append('../')
import transcoder
transcoder.transcoder_set_dir('transcoder')

def convert(filein,fileout,tranin,tranout):
 fp = codecs.open(filein,"r",'utf-8')
 fpout = codecs.open(fileout,"w",'utf-8')
 n=0
 for ix,x in enumerate(fp):
  x = x.rstrip('\r\n')
  n=n+1
  if x.startswith(';'): 
   # a comment
   fpout.write("%s\n" % x)
   continue
  m = re.search(r'^(.*?):(.+)$',x)
  if not m:
   out = "line %s is unknown: %s" %(ix+1,x)
   print(out)
   exit(1)
  head = m.group(1)
  body = m.group(2)
  head1 = transcoder.transcoder_processString(head,tranin,tranout)
  body1 = transcoder.transcoder_processString(body,tranin,tranout)
  y = "%s:%s" % (head1,body1)
  fpout.write("%s\n" % y)
 fp.close()
 fpout.close()
 print(n,"lines converted\n")
#-----------------------------------------------------
if __name__=="__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2]
 tranin = sys.argv[3]
 tranout = sys.argv[4]
 convert(filein,fileout,tranin,tranout)


