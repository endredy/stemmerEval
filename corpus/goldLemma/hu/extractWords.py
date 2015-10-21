#!/usr/bin/env python
import sys
import re
#import gzip


# <humor><lemma>termel.s</lemma><mscat>[Nc-sn---p3]</mscat></humor>
# <msd><lemma>termel.s</lemma><mscat>[Nc-sn---p3]</mscat></msd>
def getLemma(s):
    lemmaRegEx = re.compile(r'<msd><lemma>(.*?)</lemma>', re.DOTALL)
    x = lemmaRegEx.findall(s)
    if (len(x) > 0):
        return getLastWord(x[0])
    return ""

def getLastWord(s):
    s1 = s.strip()
#    s1 = s1.replace('+', '') # sometimes lemma contains '+'
    i=s1.strip().rfind(' ')
    if (i == -1):
        return s1
    return s1[i+1:]

sentRegEx = re.compile(r'<s\b.*?>(.*?)</s>', re.DOTALL)
#npRegEx = re.compile(r'(.*?)(</?NP)', re.DOTALL)
anaRegEx = re.compile(r'<ana>(.*?)</ana>', re.DOTALL)
wRegEx = re.compile(r'<w>([^\n\r]+)[\n\r]+(.*?)</w>',  re.DOTALL)
anaVRegEx = re.compile(r'<anav>(.*?)</anav>', re.DOTALL)

#dataFile = gzip.open(fileName, "rb")
f = open(sys.argv[1],'r')
#read in the file to memory
#fullData = f.readlines()
fullData = f.read()
f.close()

sents = sentRegEx.findall(fullData)
for s in sents:
    c = 0
    matches = wRegEx.findall(s)
    for m in matches:
        if m is None or len(m) == 0:
	    continue
        word = getLastWord(m[0])
        stem = ''
# todo: tobb szavas input eseten az ucso szot kene csak megtartani/merni
#    continue
#    np = npRegEx.findall(m[1])
        stems = anaRegEx.findall(m[1])
#    if np is None or len(np) == 0:
#	continue
        if (len(stems) > 1):
            sys.stderr.write('warning: more selected stem' + word)
        elif (len(stems) == 1):
            stem = getLemma(stems[0])

#    for n in stem:
#        print getLemma(n.group(1))
        anav = anaVRegEx.findall(m[1])
        stemList = set()
        for v in anav:
            stemList.add(getLemma(v))
        stem += '(' + ','.join(stemList) + ')'
        print(word + '\t' + stem)
        c += 1
#	    sys.stdout.write(w.strip() + ' ')
    if c > 0:
        print # end of a sentence
