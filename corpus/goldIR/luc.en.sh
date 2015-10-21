


STOPWORD=../../stopwords/English.snow.txt
WORDPATH=../../en/hunspell
EVALSCRIPT=../../script/evalStemmerLuc.py
GOLDDATAPATH=../goldLemma/en/bnc
LUCEVALOUTPUT=en
SENTSOUT=en/sents

mkdir -p $LUCEVALOUTPUT $SENTSOUT

for f in ACPROSE CONVRSN FICTION NEWS NONAC OTHERPUB OTHERSP UNPUB
    do
	echo "Processing $f" 
	python3 $EVALSCRIPT --stopword $STOPWORD --stemfile $GOLDDATAPATH/$f.bnc.txt.words.txt --gold $GOLDDATAPATH/$f.bnc.txt --format base --fullSents 1 --fullSentsPath $SENTSOUT --domain $f > $LUCEVALOUTPUT/domain.$f
    done