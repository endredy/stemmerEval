#!/usr/bin/env python
import sys
import re
import math
import os
import argparse
from nltk.metrics import paice

import word2sentence

# it gives the stems, 1st one is the winner stem
def getGoldStems(s):
    t=s.split('\t')
    v=t[1].split('(')
    if len(v) == 1:
        x = v[0].strip()
        return (t[0], x, x) # there is no ()  it has only 1 stem (en)
    return (t[0], v[0], v[1].split(','))


# there can be POS info with the stem
def isStopword(stem, stopwords):
    s = stem.split('[')
    if len(s) > 1:
        s1 = '['.join(s[0:-1]) # without last item
        return s1 in stopwords
    return s in stopwords

# parameters:
#  <stopword file> <stem file> <gold std file> <format> <no stem, optionally>

parser = argparse.ArgumentParser(description='eval stemmers with corpus')
parser.add_argument('--stopword', default='')
parser.add_argument('--stemfile', default='')
parser.add_argument('--gold', default='')
parser.add_argument('--format', default='base')
parser.add_argument('nostem', nargs='?', default=0) #, required=False)
parser.add_argument('--domain', default='')
parser.add_argument('--fullSents', default=0)
parser.add_argument('--fullSentsPath', default='')
p = parser.parse_args()

# load stopwords
stopwords = []
f = open(p.stopword)
for line in f:
    stopwords.append( line.strip())
f.close()

nostem=0
if p.nostem == 'nostem':
    nostem = 1

print(p.gold)
fGold = open(p.gold,'r')
debug = 0
fullSents = p.fullSents
fullSentPath= p.fullSentsPath
goldSentFilename = ''

if fullSents:
    debug=1
    if p.domain != '':
        fullSentPath = p.fullSentsPath + '/' + p.domain
        if not os.path.exists(fullSentPath):
            os.makedirs(fullSentPath)
    goldSentFilename = p.fullSentsPath + '/' + p.domain + 'GoldSents.txt'

print(fullSentPath + ' ' + str(fullSents) + ' nostem:' + str(nostem) + ' ' + str(debug))
if debug:
    fDebug = open('sentLists.txt', 'w')

sentID = 0
currSent = []
goldHits = word2sentence.word2sentence()
inputWord = ''
stems=[]
stem=''
first=1

goldLemmas={}
onlyPunct = re.compile('^\W+$') # it contains only punctuation

for goldLine in fGold:

    if (goldLine.strip() == ''):
        # new sentence
        if fullSents:
            prefix = str(int(sentID / 1000))
            if not os.path.exists(fullSentPath + '/' + prefix):
                os.makedirs(fullSentPath + '/' + prefix)
            currSentFile = open(fullSentPath + '/' + prefix + '/' + str(sentID) + '.txt', 'w')
            currSentFile.write(' '.join(currSent))
            currSentFile.close()

        if debug:
            fDebug.write('\n\nsentID:' + str(sentID) + '\n')
            fDebug.write('\n'.join(currSent))

        currSent = []

        sentID += 1 # new sentence 
        continue

    (word, gStem, gStemList) = getGoldStems(goldLine)
    currSent.append(word.strip())
    if onlyPunct.match(word) != None:
        continue # words are ignored which contain only punctuation

#    word = word.lower()
#    gStem = gStem.lower()
    if isStopword(gStem.lower(), stopwords):
        continue # stopword: SKIP
#    print(word + ' ' + gStem + ' ' + str(sentID))
    goldHits.addHit(word, gStem, sentID)  # TODO: a kis/nagybetut az inputrol at kene masolni

if debug:
    fDebug.close()

fGold.close()

if fullSents:
    goldSentFile = open(goldSentFilename, 'w')

for w in goldHits.getWords():
    sIdsGold = goldHits.getSentIDs(w)

    #debug info:
    #print(goldHits.getWordsByStem(w))
    if fullSents:
        goldSentFile.write(w + '\t' + ",".join(str(e) for e in sIdsGold) + '\n')
        continue

if fullSents:
    goldSentFile.close()
