


STOPWORD=../../stopwords/Polish.txt
EVALSCRIPT=../../script/evalStemmerLuc.py
GOLDDATAPATH=../goldLemma/pl/pnc
LUCEVALOUTPUT=pl
SENTSOUT=pl/sents

mkdir -p $LUCEVALOUTPUT $SENTSOUT
for f in typ_fakt typ_nd typ_inf-por typ_net_interakt typ_konwers typ_net_nieinterakt typ_listy typ_nklas typ_lit typ_publ typ_lit_poezja typ_qmow typ_media typ_urzed
    do
	echo "Processing $f"
	python3 $EVALSCRIPT --stopword $STOPWORD --stemfile $GOLDDATAPATH/$f.ann_morphosyntax.xml.txt.words --gold $GOLDDATAPATH/$f.ann_morphosyntax.xml.txt --format base --fullSents 1 --fullSentsPath $SENTSOUT --domain $f > $LUCEVALOUTPUT/domain.$f
    done