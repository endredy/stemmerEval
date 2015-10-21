#!/usr/bin/env python
import sys
import re

f = open(sys.argv[1],'r')
print(sys.argv[1])
tp=0
fn=0
fp=0
oov=0
summa=0
lasttp=0
lastfn=0
lastfp=0

searchRes = 0
stp=0
sfn=0
sfp=0
for line in f:
    l = re.match('search eval', line)
    if (l != None):
        searchRes = 1
#        if summa == 0:
        summa += lasttp+lastfp+lastfn

    l = re.match('(\S+) *= *(\d+)', line)
    if (l == None):
        continue
    if (l.group(1) == 'tp' or l.group(1) == 'stp'):
        if searchRes:
            stp += float(l.group(2))
        else:
            lasttp = float(l.group(2))
            tp += lasttp
    elif (l.group(1) == 'fp' or l.group(1) == 'sfp'):
        if searchRes:
            sfp += float(l.group(2))
        else:
            lastfp = float(l.group(2))
            fp += lastfp
    elif (l.group(1) == 'fn' or l.group(1) == 'sfn'):
        if searchRes:
            sfn += float(l.group(2))
            searchRes = 0 # last value, next item will be simple fp, tp, fn
        else:
            lastfn = float(l.group(2))
            fn += lastfn
    elif (l.group(1) == 'oov'):
        oov += float(l.group(2))

        #new word
#    print(line)

f.close()

#exit()

# print summary
sys.stdout.write('\n')
sys.stdout.write('tp = {}\nfp = {}\nfn = {}\noov={} ({})\nsum={}\n'.format(tp, fp, fn, oov, oov/summa, summa))
prec = 0 if tp+fp==0 else tp / (tp + fp)
rec  = 0 if tp+fn==0 else tp / (tp + fn)
F = 2*prec*rec / (prec + rec)
sys.stdout.write('P = {}\nR = {}\nF = {}\n'.format(prec, rec, F))


# print summary
sys.stdout.write('search eval:\n')
sys.stdout.write('stp = {}\nsfp = {}\nsfn = {}\n'.format(stp, sfp, sfn))
prec = 0 if stp+sfp==0 else stp / (stp + sfp)
rec  = 0 if stp+sfn==0 else stp / (stp + sfn)
F = 2*prec*rec / (prec + rec)
sys.stdout.write('P = {}\nR = {}\nF = {}\n'.format(prec, rec, F))

# legjobb eset:ha minden fp kijavulna:
#tp += fp
#fp = 0

#sys.stdout.write('best case would be:\n')
#sys.stdout.write(' tp = {}\n fp = {}\n fn = {}\n'.format(tp, fp, fn))
#prec = 0 if tp+fp==0 else tp / (tp + fp)
#rec  = 0 if tp+fn==0 else tp / (tp + fn)
#F = 2*prec*rec / (prec + rec)
#sys.stdout.write(' P = {}\n R = {}\n F = {}\n'.format(prec, rec, F))

