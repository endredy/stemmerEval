
STOPWORD=../../stopwords/English.snow.txt
EVALSCRIPT=../../script/evalStemmer.py
GOLDPATH=../../corpus/goldLemma/en/bnc

mkdir -p eval

function eval(){

    python3 $EVALSCRIPT $STOPWORD hunspell/$1.txt $GOLDPATH/$1.bnc.txt base > eval/hunspell.$1
#    python3 $EVALSCRIPT $STOPWORD humor/$1.txt $GOLDPATH/$1.bnc.txt base > eval/humor.$1
#    python3 $EVALSCRIPT $STOPWORD snowball/$1.txt $GOLDPATH/$1.bnc.txt base > eval/snowball.$1
    python3 $EVALSCRIPT $STOPWORD kstem/$1.txt $GOLDPATH/$1.bnc.txt base > eval/kstem.$1
    echo "processing $1 (porter)"

#    python3 $EVALSCRIPT $STOPWORD porter/$1.txt $GOLDPATH/$1.bnc.txt > eval/porter.$1
#    python3 $EVALSCRIPT $STOPWORD  enminimal/$1.txt $GOLDPATH/$1.bnc.txt > eval/enminimal.$1

# no stem
    python3 $EVALSCRIPT $STOPWORD kstem/$1.txt $GOLDPATH/$1.bnc.txt base nostem > eval/nostem.$1
}


#eval CONVRSN
#eval FICTION
#eval ACPROSE
#eval NEWS
eval NONAC
#eval OTHERPUB
#eval OTHERSP
#eval UNPUB


