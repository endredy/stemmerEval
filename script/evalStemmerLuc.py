#!/usr/bin/env python
import sys
import re
import math
import os
import argparse
from nltk.metrics import paice

def getStem(s):
    if (s == '+?' or s == 'unknown word'):
        return None # unknown
    i=s.find('+')
    if (i == -1):
        return s
    return s[0:i]

# visszaadja a toveket, elso eleme a nyertes to
def getGoldStems(s):
    #fel     fel(fel)
    #tegnap  tegnap(tegnap)
    #print(s)
    t=s.split('\t')
#    print(t)
#    t[1] = t[1].replace('+', '')
    v=t[1].split('(')
    if len(v) == 1:
        x = v[0].strip()
        return (x, x) # nincs () benne, csak egy tove (angol)
    return (v[0], v[1].split(','))

# a to alternativakbol valaszt
def getBestStem(stems):
    longest=''
    for s in stems:
        if s is None:
            return ''
        if (len(longest) < len(s)):
            longest=s
    return longest

# az adott szohoz hozzaadja az adott mondat azonositojat
class word2sentence:

    def __init__(self):
        self.words = {}
        self.ids = {}
        self.stem2words = {} # for debug

    def addHit(self, word, stem, sID):
#        print('addHit: ' + word + ' ' + stem)
        if stem == '':
            stem = word
        i = self.words.get(word, '')
        if i == '':
            self.words[word] = [stem]
        elif stem not in i:
            i.append(stem)

#        self.ids.add(iID)
        o = self.ids.get(stem, None)
        if o == None:
            self.ids[stem]=set([sID]) # [sID]
        elif sID not in o:
            o.add(sID) # append(sID)

        # debug
        s = self.stem2words.get(stem, '')
        if s == '':
            self.stem2words[ stem ] = [word]
        elif word not in s:
            s.append(word)

    def getWords(self):
        return self.words

    def getWordsByStem(self, word):
        stems = self.words.get(word, [])
        r = ''
        for s in stems:
            r += ' ' + s + ' -> ' + str(self.stem2words.get(s, []))
        return r

    def getSentIDs(self, word):
        st = self.words.get(word, '')
        if (st == ''):
            return set()#[]
        r = set() #[]
        for i in st:
            #r = r + self.ids.get(i, [])
            r = r.union(self.ids.get(i, set())) # itt [] volt!
        return r

    def print(self):
        print('\nwords: ' + str(self.words))
        print('\nids: ' + str(self.ids))

    def getPaiceStems(self):
        return self.stem2words

class StemReaderOcastem:

    def __init__(self, filename):
        self.f = open(filename, 'r')

    def reset(self):
        self.f.seek(0)

    def getNextWordAndStems(self):

        stems = []
        line = self.f.readline()
        if not line:
            return (None, [])
        p = line.strip().split('\t')
        return (p[0], p[1:])

class StemReaderFoma:

    def __init__(self, filename):
        self.f = open(filename, 'r')

    def reset(self):
        self.f.seek(0)

    def getNextWordAndStems(self):

        stems = []
        line = self.f.readline()
#        print(line)
        while line and len(line.strip()) != 0:
            s=getStem(line)
            if s is None or len(s) > 0:
                stems.append(s)
            line = self.f.readline()

        if len(line) == 0:
            return(None, stems) # end of file
        return ('', stems)

    def getWord(self, s):
        t=s.split('\t')
        return t[0]

class StemReaderOcamorf:

    def __init__(self, filename):
        self.f = open(filename, 'r')
        self.nextWord = ''

    def reset(self):
        self.f.seek(0)
        self.nextWord = ''

    # el/PREV+megy/VERB<PAST><PERS<1>><PLUR>
    # m.lik/VERB[PERF_PART]/ADJ
    def getStem(self, s):
        r=''
        skip=0
        if (s == 'UNKNOWN'):
            return None # unknown
        for ch in s:
            if (ch == '/'):
                skip=1
            if (skip == 0):
                r += ch
            if (ch == '+'):
                skip=0

        return r

    def getNextWordAndStems(self):

        stems = []
        word = ''
        if self.nextWord != '':
            word = self.nextWord
        line = self.f.readline()
        while line and len(line) != 0:
            if (line.startswith('> ')):
                #new word
                if self.nextWord == '':
                    word = line.strip(' >\n')
                    self.nextWord = line # avoid this condition next time
                    line = self.f.readline()
                    continue
                else:
                    self.nextWord = line.strip(' >\n')
                    return (word, stems)

            s=self.getStem(line.strip())
            if s is None or len(s) > 0:
                stems.append(s)
            line = self.f.readline()

        return (None, stems)


class StemReader:

    def __init__(self, filename):
        self.currWord = ''
        self.currStems = []
        self.nextWord = ''
        self.f = open(filename, 'r')
        self.debug = 0
        self.first = 1
        self.currSent = []

    def reset(self):
        self.f.seek(0)
        self.currWord = ''
        self.nextWord = ''
        self.first = 1

    def getNextLine(self, t):

        line = self.f.readline()
        reg = '^\S' # line start with letters (new word)
        if t == 'not empty':
            reg = '\S'
        if t == 'stemline':
            reg = '^\s'
        while (line and re.search(reg, line) == None):
            line = self.f.readline()
        return line

    def getNextWordAndStems(self):
        # vagy a fajl elejere mutat, vagy egy input szo utanra
        self.currStems = []
        if (self.first == 1):
            # elso szo
            self.currWord = self.getNextLine('')
            self.first = 0
#            self.currWord = line#.strip()
        else:
            self.currWord = self.nextWord # folytatjuk
        self.currWord = self.currWord.strip()
        line = self.currWord

        while(line):
#            print(line + self.currWord)

            # no stem:.
            if nostem:
                # no stem: we dont need stem, so skip them, and then return
                self.nextWord = self.getNextLine('')
                return (self.currWord, [self.currWord])

            line = self.getNextLine('not empty')
            if (re.match('\S', line) != None):
                # new word:
                self.nextWord = line.strip().lower()
                return (self.currWord, self.currStems)

            # beljebb van: stem

            s = getStem(line.strip())

            if s is None:
                self.currStems.append(s)
            if (s is None or s == ''):
                continue
            s = s.lower() # legyen kisbetus
            if len(s) > 0:
                self.currStems.append(s)

        return (None, [])


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
f = open(p.stopword)#sys.argv[1],'r')
for line in f:
    stopwords.append( line.strip())
f.close()

nostem=0
if p.nostem == 'nostem':
    nostem = 1

print(p.gold)#sys.argv[2])
inputFormat = p.format#sys.argv[4]
if (inputFormat == 'base'):
    f = StemReader(p.stemfile)
elif (inputFormat == 'ocamorph'):
    f = StemReaderOcamorf(p.stemfile)
elif (inputFormat == 'ocastem'):
    f = StemReaderOcastem(p.stemfile)
elif (inputFormat == 'foma'):
    f = StemReaderFoma(p.stemfile)
else:
    print('unknown stem file format: ' + inputFormat)
    sys.exit(0)
#f = open(sys.argv[1],'r')
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
goldHits = word2sentence()
currHits = word2sentence()
inputWord = ''
stems=[]#set()
stem=''
first=1
oov=0
tp=0
fn=0
fp=0
tp1=0
fp1=0
fn1=0
besttp2=0
bestfp2=0
tp2=0
fp2=0
stp = 0
sfp = 0
sfn = 0

goldLemmas={}
onlyPunct = re.compile('^\W+$') # csak irasjelbol all az input

while True:
    (word, stems) = f.getNextWordAndStems()
    if word == None:
        break

#    print(str(tp+fp+fn) + ' ' + str(word) + str(stems))
        #new word
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
#    print(str(tp+fp+fn) + ' ' + str(word) + str(stems))
    (gStem, gStemList) = getGoldStems(goldLine)
#    stem = getBestStem(stems)
#    stem = stems[0]
    if onlyPunct.match(word) != None:
#    if word.find('-') != -1 or word.find('/') != -1 or word == "'":
        continue # kotojeles perjeles szavakat kidobjuk, mert megszivatja a lucene stemmereket (+ ' % etc)
#        print(gStem + ' == ' + stem)


    # meg kisbetusites elott irjuk ki, ha kell
#    if (len(stems) == 0 and word != ''):
    if None in stems or (len(stems) == 0 and word != ''):
#        print('oov: ' + word)
        oov += 1

    word = word.lower()
    gStem = gStem.lower()
    if gStem in stopwords:
        continue # stopword: NEM SZAMOLJUK
        # not stopword: count it
    goldHits.addHit(word, gStem, sentID)  # TODO: a kis/nagybetut az inputrol at kene masolni
#        if gStem in stems:
#                currHits.addHit(inputWord, gStem, sentID)
#            else:
#                currHits.addHit(inputWord, stem, sentID)

# VAGY
#            currHits.addHit(inputWord, stem.lower(), sentID)
    for s in stems:
        currHits.addHit(word, s, sentID)
#        if (sentID == 418):
#            print(goldLine)
#            print(inputWord + ' Gold:' + gStem + ' stem:' + stem)

#beletesszuk az eredeti alakot is
#            goldHits.addHit(inputWord, inputWord, sentID)
#            currHits.addHit(inputWord, inputWord, sentID)
#            goldHits.print()
#            currHits.print()
#    inputTest = re.sub(r'\W', '', inputWord)
#        if inputTest == '':
#            print(inputWord + ' skipped')
#            stems=set()
#            stem=''
#            inputWord = line.strip()
#            continue

#            print(inputWord + ' ' + gStem)
# legjobb to valasztasa eseten elerheto eredmeny:
#        if (gStem in stems):
#            tp += 1
#        else:
#            fn += 1

#    gStem = gStem.lower()
    # egyes metrika : minden egyes teves alternativa +1 fp
    bestStem = getBestStem(stems)
    if len(stems)>0:
        if bestStem == gStem or stems[0] == gStem:
            tp1 += 1
        else:
            fn1 += 1 # vagy az legyen az fn, ha teljesen bena tovet ad?
        fp1 += len(stems) - 1 

    # kettes metrika: accuracy: az 1. ill leghosszabb hanyszor volt jo
    if bestStem == gStem:  # leghosszabb
#    if (len(stems) > 0 and stems[0] == gStem): # elso
        tp2 += 1
    else:
        fp2 += 1

    # ugyanezen metrika, de legjobb eset szamolasa
    if gStem in stems:
        besttp2 += 1
    else:
        bestfp2 += 1


    # harmas metrika: minden gold lemma
    c = goldLemmas.get(word, 0)
    if c == 0:
        goldLemmas[ word ] = set([gStem])
    else:
        c.add(gStem)

    rankCounter = -1
    for i in range(0, len(stems)):
        if stems[i] == gStem:
            rankCounter = i
            break
    if rankCounter != -1:
        # volt jo talalat
        tp += 1
        fp += rankCounter # az n. helyen volt a jo to
    else:
        fn += 1 # nem volt sehol a jo to
#        print('fn: ' + word + ' ' + stem + ' ' + gStem)

#    if (gStem == stem):
#        tp += 1 # eltalalta
#    elif (gStem in stems):
#        print('fp: ' + gStem + '?' + stem)
#        fp += 1 # a to alternativak kozott ott volt a jo
#    else:
#        print('fn: ' + gStem + '?' + stem)
#        fn += 1 # rossz to
    if (False and gStem.lower() != stem.lower()):
        print(gStem + '  ' + stem + '(' + ','.join(stems) + ')')

#f.close()
#fGold.close()
if debug:
    fDebug.close()

# 3-as metrics
f.reset()
if inputFormat == 'foma':
    fGold.seek(0)
while False: #True:
    (word, stems) = f.getNextWordAndStems()
#    print(word)
    if word == None:
        break

    if inputFormat == 'foma':

        goldLine = fGold.readline()
        while (goldLine.strip() == ''):
            goldLine = fGold.readline()
        word = f.getWord(goldLine)


    currStems = set(stems)
#    print('word: ' + word)
    goldStems = goldLemmas.get(word, set())

#    print(str(goldStems) + ' ' + str(currStems))
    a = goldStems.intersection(currStems)
    stp += len(a) # benne van a goldban ez a talalat
    a = goldStems.difference(currStems) # new set with elements in g but not in h
    sfn += len(a) # a gold ezen talata nincs benne az eredmenyben (false negative)
    b = currStems.difference(goldStems)
    sfp += len(b)

fGold.close()

# print summary
sys.stdout.write('ranking metrics\n')
#sys.stdout.write('tp = {}\nfp = {}\nfn = {}\noov = {}\n'.format(tp, fp, fn, oov))
sys.stdout.write('tp = {}\nfp = {}\nfn = {}\noov={} ({})\nsum={}\n'.format(tp, fp, fn, oov, oov/(tp+fp+fn), tp+fp+fn))
prec = 0 if tp+fp==0 else tp / (tp + fp)
rec  = 0 if tp+fn==0 else tp / (tp + fn)
F = 0
if prec + rec != 0:
    F = 2*prec*rec / (prec + rec)
sys.stdout.write('P = {}\nR = {}\nF = {}\n'.format(prec, rec, F))


sys.stdout.write('\nstrict\n')
#sys.stdout.write('tp = {}\nfp = {}\nfn = {}\noov = {}\n'.format(tp, fp, fn, oov))
sys.stdout.write('tp = {}\nfp = {}\nfn = {}\n'.format(tp1, fp1, fn1, oov))
prec = 0 if tp1+fp1==0 else tp1 / (tp1 + fp1)
rec  = 0 if tp1+fn1==0 else tp1 / (tp1 + fn1)
F = 0
if prec + rec != 0:
    F = 2*prec*rec / (prec + rec)
sys.stdout.write('P = {}\nR = {}\nF = {}\n'.format(prec, rec, F))


sys.stdout.write('\naccuracy\n')
#sys.stdout.write('tp = {}\nfp = {}\nfn = {}\noov = {}\n'.format(tp, fp, fn, oov))
sys.stdout.write('tp = {}\nfp = {}\nacc={}\n'.format(tp2, fp2, tp2/(tp2+fp2)))
sys.stdout.write('BEST acc.\ntp = {}\nfp = {}\nacc={}\n'.format(besttp2, bestfp2, besttp2/(besttp2+bestfp2)))

sys.stdout.write('\nsets\n')
#sys.stdout.write('tp = {}\nfp = {}\nfn = {}\noov = {}\n'.format(tp, fp, fn, oov))
#sys.stdout.write('tp = {}\nfp = {}\nfn = {}\noov={} ({})\nsum={}\n'.format(stp, sfp, sfn, oov, oov/(stp+sfp+sfn), stp+sfp+sfn))
#prec = 0 if stp+sfp==0 else stp / (stp + sfp)
#rec  = 0 if stp+sfn==0 else stp / (stp + sfn)
#F = 0
#if prec + rec != 0:
#    F = 2*prec*rec / (prec + rec)
#sys.stdout.write('P = {}\nR = {}\nF = {}\n'.format(prec, rec, F))


#sys.exit(0) # most csak a lemmapontossag kell

if fullSents:
    goldSentFile = open(goldSentFilename, 'w')


# print search quality
stp = 0
sfp = 0
sfn = 0
#for key, value in my_dict.iteritems():
for w in goldHits.getWords():
    sIdsGold = goldHits.getSentIDs(w)
    sIdsCurr = currHits.getSentIDs(w)

    if fullSents:
        goldSentFile.write(w + '\t' + ",".join(str(e) for e in sIdsGold) + '\n')
        continue

    printDebugInfos = 0
#    g = set(sIdsGold)
#    h = set(sIdsCurr)
    a = sIdsGold.intersection(sIdsCurr)
    stp += len(a) # benne van a goldban ez a talalat
    a = sIdsGold.difference(sIdsCurr) # new set with elements in g but not in h
    sfn += len(a) # a gold ezen talata nincs benne az eredmenyben (false negative)
    if (len(a) > 0):
        printDebugInfos = 1
    b = sIdsCurr.difference(sIdsGold)
    if len(b) > 0:
        base = len(b) % 10
        n = 0
        if len(b) > 10:
            n = math.log(len(b) - base) + 10
            #if len(b) % 100 >= 50:
            #    n += 50 # 50 felettiek min. azt kapjak, mint a 50 alattiak
        sfp += base + n # 10 alatti erteket siman hozzadom + logaritmikusan: ranking szimulacioja
#        if len(b) < 10:
#            sfp += 1 # van olyan talalata, ami nincs a goldban, tudom durva, de csak +1
#        else:
#            sfp += len(b)/10  # nagyobb, mint 10 ilyenje van: tobb minusz pont
   
#    if len(a) > 10:
#        sfp += len(a)/10 # nincs benne a goldban ez a talalat (false positive), a ranking ezeket jo esetben hatratolja
#    else:
#        sfp += len(a) # 10 alatt siman hozzadjuk
#    if (len(a) > 0):
#        printDebugInfos = 1

#    for g in sIdsGold:
#        if g in sIdsCurr:
#            stp += 1 # benne van a goldban ez a talalat
#        else:
#            sfn += 1 # a gold ezen talata nincs benne az eredmenyben (false negative)
#    for c in sIdsCurr:
#        if c not in sIdsGold:
#            # debug
#            printDebugInfos = 1
#            sfp += 1 # nincs benne a goldban ez a talalat (false positive)
    if False and printDebugInfos:
        print('input word: ' + w)

        print(' gold stems: ' + str(goldHits.getWords().get(w)))
        print('  =>' + str(goldHits.getWordsByStem(w)))
        print(' curr stems: ' + str(currHits.getWords().get(w)))
        print('  =>' + str(currHits.getWordsByStem(w)))
        print(' gold hits:' + str(len(sIdsGold)))
        print(' curr hits:' + str(len(sIdsCurr)))
#        print(' gold hits:' + str(sIdsGold))
#        print(' curr hits:' + str(sIdsCurr))
        print(' fn hits:' + str(a))


if fullSents:
    goldSentFile.close()
    sys.exit(0)
#debug
#goldHits.print()
#currHits.print()

sys.stdout.write('\n\nsearch eval\n')
sys.stdout.write('tp = {}\nfp = {}\nfn = {}\n'.format(stp, sfp, sfn))
prec = 0 if stp+sfp==0 else stp / (stp + sfp)
rec  = 0 if stp+sfn==0 else stp / (stp + sfn)
F = 2*prec*rec / (prec + rec)
sys.stdout.write('P = {}\nR = {}\nF = {}\n'.format(prec, rec, F))

# Paice test
lemmas = goldHits.getPaiceStems()
stems = currHits.getPaiceStems()
p = paice.Paice(lemmas, stems)
print('\nPaice metrics:')
print(p)
