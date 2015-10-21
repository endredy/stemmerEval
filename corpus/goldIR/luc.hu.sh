


STOPWORD=../../stopwords/Hungarian.txt
EVALSCRIPT=../../script/evalStemmerLuc.py
GOLDDATAPATH=../goldLemma/hu/data
LUCEVALOUTPUT=hu
SENTSOUT=hu/sents

mkdir -p $LUCEVALOUTPUT $SENTSOUT

#for f in newsp busin
for f in newsp busin it law comp fict
    do
	echo "Processing $f"
	python3 $EVALSCRIPT --stopword $STOPWORD --stemfile $GOLDDATAPATH/domain.$f.utf.words --gold $GOLDDATAPATH/domain.$f.utf.txt --format base --fullSents 1 --fullSentsPath $SENTSOUT --domain $f > $LUCEVALOUTPUT/domain.$f
#	python3 $EVALSCRIPT --stopword $STOPWORD --stemfile ../hunspell/domain.$f.txt --gold $GOLDDATAPATH/domain.$f.utf.txt --format base --fullSents 1 --fullSentsPath $SENTSOUT --domain $f > $LUCEVALOUTPUT/domain.$f
    done