STOPWORD=../../stopwords/Polish.txt
EVALSCRIPT=../../script/evalStemmer.py
GOLDPATH=../../corpus/goldLemma/pl/pnc

mkdir -p eval

function eval(){

    python3 $EVALSCRIPT $STOPWORD hunspell/$1.txt $GOLDPATH/$1.ann_morphosyntax.xml.txt base > eval/hunspell.$1
#    python3 $EVALSCRIPT $STOPWORD humor/$1.txt $GOLDPATH/$1.ann_morphosyntax.xml.txt base > eval/humor.$1
    python3 $EVALSCRIPT $STOPWORD stempfel/$1.txt $GOLDPATH/$1.ann_morphosyntax.xml.txt base > eval/stempfel.$1
    python3 $EVALSCRIPT $STOPWORD morfologik/$1.txt $GOLDPATH/$1.ann_morphosyntax.xml.txt base > eval/morfologik.$1
# no stem
    python3 $EVALSCRIPT $STOPWORD stempfel/$1.txt $GOLDPATH/$1.ann_morphosyntax.xml.txt base nostem > eval/nostem.$1
}

eval typ_lit
exit
eval typ_fakt
eval typ_nd
eval typ_inf-por
eval typ_net_interakt
eval typ_konwers
eval typ_net_nieinterakt
eval typ_listy
eval typ_nklas
eval typ_publ
eval typ_lit_poezja
eval typ_qmow
eval typ_media
eval typ_urzed

