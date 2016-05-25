#!/usr/bin/env python
import sys
import re
import ntpath
import os

# pol xml:  
#  <s xml:id="words_1.57-s" corresp="ann_morphosyntax.xml#morph_1.57-s">
#           <seg xml:id="words_1.57-s_sa52">
#              <fs type="words">
#                <f name="orth">
#                  <string>drzwi</string>
#                </f>
#                <f name="base">
#                  <string>drzwi</string>
#                </f>
#		<f name="ctag">
#                  <symbol value="Verbfin"/>
#                </f>

# create gold standard with (1) or without Part-of-Speech (0)
POSinfo=1

sentRegEx = re.compile(r'<s\b.*?>(.*?)</s>', re.DOTALL)
itemRegEx = re.compile(r'<seg\b.*?>(.*?)</seg>', re.DOTALL)
wordRegEx = re.compile(r'<f name="orth">\s+<string>(.*?)</string>', re.DOTALL)
stemRegEx = re.compile(r'<f name="base">\s+<string>(.*?)</string>', re.DOTALL)
posRegEx = re.compile(r'<f name="ctag">\s+<symbol +value="(.*?)"/>', re.DOTALL)

# <catRef scheme="#taxonomy-NKJP-type" target="#typ_publ"/>
# <catRef scheme="#taxonomy-NKJP-channel" target="#kanal_prasa_dziennik"/>
p = os.path.dirname(sys.argv[1])
filename = ntpath.basename(sys.argv[1])

f = open(p + '/header.xml','r')
fullData = f.read()
f.close()
type = sentRegEx.findall(fullData)

type='unknown'
tt = re.compile(r'<catRef scheme="#taxonomy-NKJP-type" target="#(.*?)"', re.DOTALL).findall(fullData)
for t in tt:
    if t is not None or len(m) != 0:
        type=t

directory = './pnc/' + type
if not os.path.exists(directory):
    os.makedirs(directory)
outFile = open(directory + '.' + filename + '.txt', 'a')

f = open(sys.argv[1],'r')
fullData = f.read()
f.close()


sents = sentRegEx.findall(fullData)
for s in sents:
    c = 0
    matches = itemRegEx.findall(s)
    for m in matches:
        if m is None or len(m) == 0:
	    continue
        w = wordRegEx.findall(m)
        s = stemRegEx.findall(m)
        p = posRegEx.findall(m)
        word = ''
        if len(w) > 0:
           word = w[0].strip()
        stem = ''
        if len(s) > 0:
           stem = s[0].strip()
        pos = ''
        if len(p) > 0 and POSinfo:
           pos = '['+p[0].strip()+']'

        if re.match('[,.:;?!"\']', word) != None:
           continue

        outFile.write(word + '\t' + stem + pos + '\n')
        c = c + 1
    if c > 0:
        outFile.write('\n') # end of a sentence

outFile.close()