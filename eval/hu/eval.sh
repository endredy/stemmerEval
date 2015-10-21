
STOPWORD=../../stopwords/Hungarian.txt
EVALSCRIPT=../../script/evalStemmer.py
GOLDPATH=../../corpus/goldLemma/hu/data

mkdir -p eval

# az itteni goldot kell hasznalni, mert ebben vannak jelolve a  mondatok
function eval(){

    python3 $EVALSCRIPT $STOPWORD ocamorph/$1.txt $GOLDPATH/$1.utf.txt ocamorph > eval/ocamorph.$1
    python3 $EVALSCRIPT $STOPWORD ocastem/$1.txt $GOLDPATH/$1.utf.txt ocastem > eval/ocastem.$1
    python3 $EVALSCRIPT $STOPWORD hunspell/$1.txt $GOLDPATH/$1.utf.txt base > eval/hunspell.$1
    python3 $EVALSCRIPT $STOPWORD humor/$1.txt $GOLDPATH/$1.utf.txt base > eval/humor.$1
    python3 $EVALSCRIPT $STOPWORD snowball/$1.txt $GOLDPATH/$1.utf.txt base > eval/snowball.$1
#    python3 $EVALSCRIPT $STOPWORD foma/$1.txt $GOLDPATH/$1.utf.txt foma > eval/foma.$1
# no stem
    python3 $EVALSCRIPT $STOPWORD snowball/$1.txt $GOLDPATH/$1.utf.txt base nostem > eval/nostem.$1
}

for f in newsp busin it law comp fict
    do
        echo "Processing $f"
        eval domain.$f
    done
