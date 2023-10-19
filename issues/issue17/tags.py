#-*- coding:utf-8 -*-
"""tags.py
"""
import sys,re,codecs
## https:##stackoverflow.com/questions/27092833/unicodeencodeerror-charmap-codec-cant-encode-characters
## This required by git bash to avoid error
## UnicodeEncodeError: 'charmap' codec cannot encode characters 
## when run in a git bash script.

sys.stdout.reconfigure(encoding='utf-8') 

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines
  
def count_tags(lines):
 """
  return dictionary of counts of xml tags
 """
 tags = {} # returned
 metaline = None
 regexraw = '<.*?>'
 regex = re.compile(regexraw)
 for iline,line in enumerate(lines):
  if iline == 0: 
   continue 
  elif line == '':
   continue
  elif line.startswith('<L>'):
   metaline = line
   continue
  elif line == '<LEND>':
   metaline = None
   continue
  elif metaline == None:
   continue # not in an entry
  else: # one of the 'datalines' of entry
   linetags = re.findall(regex,line)
   for tag in linetags:
    if tag not in tags:
     tags[tag] = 0
    tags[tag] = tags[tag] + 1
 return tags

def write(fileout,tags):
 keys = sorted(tags.keys())
 with codecs.open(fileout,"w","utf-8") as f:
  for key in keys:
   count = tags[key]
   line = '%s %s' %(key,count)
   f.write(line + '\n')
 print(len(lines),"written to",fileout)
 
if __name__=="__main__":
 filein = sys.argv[1] #  xxx.txt (path to digitization of xxx)
 fileout = sys.argv[2] # revised xxx.txt
 lines = read_lines(filein)
 tags = count_tags(lines)

 write(fileout,tags)
  
