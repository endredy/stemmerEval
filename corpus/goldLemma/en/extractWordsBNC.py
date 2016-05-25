#!/usr/bin/env python
import sys
import re
import ntpath
import os

# BNC xml: <s n="1"><w c5="NN1" hw="factsheet" pos="SUBST">FACTSHEET </w><w c5="DTQ" hw="what" pos="PRON">WHAT </w>

# create gold standard with (1) or without Part-of-Speech (0)
POSinfo=1

sentRegEx = re.compile(r'<s\b.*?>(.*?)</s>', re.DOTALL)
# <w c5="VDD" hw="do" pos="VERB">Did </w> 
#wRegEx = re.compile(r'<w.*?hw="(.*?)".*? pos="(.*?)"[^/]*>(.*?)</w>', re.DOTALL) # hw/pos order can be different :)
wRegEx = re.compile(r'(<w[^/<>]*hw="([^\"]*)"[^/<>]*>)(.*?)</w>', re.DOTALL)
posRegEx = re.compile(r'<w[^/<>]*pos="([^\"]*)"[^/<>]*>', re.DOTALL)
typeRegEx = re.compile(r'<[ws]text type="(.*?)"', re.DOTALL)
# type of text
#  <wtext type="FICTION">
#  <stext type="OTHERSP">

if os.path.isfile(sys.argv[1]) is False:
#    print('file ' + sys.argv[1] + ' does not exist')
    sys.exit(0)
f = open(sys.argv[1],'r')
fullData = f.read()
f.close()

filename = ntpath.basename(sys.argv[1])

type='unknown'
tt = typeRegEx.findall(fullData)
for t in tt:
    if t is not None or len(m) != 0:
        type=t

directory = './bnc/' + type
if not os.path.exists(directory):
    os.makedirs(directory)
outFile = open(directory + '/' + filename + '.txt', 'w')

sents = sentRegEx.findall(fullData)
for s in sents:
    c = 0
    matches = wRegEx.findall(s)
    for m in matches:
        if m is None or len(m) == 0:
	    continue
#        outFile.write('full' + str(m))
        p = posRegEx.findall(m[0])
        pos = ''
        if len(p) > 0:
            pos = p[0]
        word = m[2].strip()
        stem = m[1].strip()
        if word == '&amp;':
            continue
        outFile.write(word + '\t' + stem)
        if POSinfo:
            outFile.write('[' + pos + ']')
        outFile.write('\n')
        c = c + 1
    if c > 0:
        outFile.write('\n') # end of a sentence
