#!/usr/bin/env python
import sys
import re
import math
import os
import argparse
from nltk.metrics import paice

import word2sentence
import stemFileReaders

# visszaadja a toveket, elso eleme a nyertes to
def getGoldStems(s):
    t=s.split('\t')
    v=t[1].split('(')
    if len(v) == 1:
        x = v[0].strip()
        return (x, x) # nincs () benne, csak egy tove (angol)
    return (v[0], v[1].split(','))

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
inputFormat = p.format
if (inputFormat == 'base'):
    f = stemFileReaders.StemReader(p.stemfile, nostem)
elif (inputFormat == 'ocamorph'):
    f = stemFileReaders.StemReaderOcamorf(p.stemfile)
elif (inputFormat == 'ocastem'):
    f = stemFileReaders.StemReaderOcastem(p.stemfile)
elif (inputFormat == 'foma'):
    f = stemFileReaders.StemReaderFoma(p.stemfile)
else:
    print('unknown stem file format: ' + inputFormat)
    sys.exit(0)

fGold = open(p.gold,'r')
debug = 0
fullSents = p.fullSents
fullSentPath= p.fullSentsPath#'sentences'
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
currHits = word2sentence.word2sentence()
inputWord = ''
stems=[]#set()
stem=''
first=1

goldLemmas={}
onlyPunct = re.compile('^\W+$') # it contains only punctuation

while True:
    (word, stems) = f.getNextWordAndStems()
    if word == None:
        break

    goldLine = fGold.readline()
    while (goldLine.strip() == ''):
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
        goldLine = fGold.readline()
    if debug:
        currSent.append(word.strip())
    if inputFormat == 'foma':
        word = f.getWord(goldLine)
    (gStem, gStemList) = getGoldStems(goldLine)
    if onlyPunct.match(word) != None:
        continue # words are ignored which contain only punctuation

    word = word.lower()
    gStem = gStem.lower()
    if gStem in stopwords:
        continue # stopword: SKIP
    goldHits.addHit(word, gStem, sentID)  # TODO: a kis/nagybetut az inputrol at kene masolni
    for s in stems:
        currHits.addHit(word, s, sentID)

if debug:
    fDebug.close()

fGold.close()

if fullSents:
    goldSentFile = open(goldSentFilename, 'w')

for w in goldHits.getWords():
    sIdsGold = goldHits.getSentIDs(w)

    if fullSents:
        goldSentFile.write(w + '\t' + ",".join(str(e) for e in sIdsGold) + '\n')
        continue

if fullSents:
    goldSentFile.close()
