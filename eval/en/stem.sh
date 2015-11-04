mkdir -p kstem hunspell

function stem(){
    ./stem.engine.sh ../../corpus/goldLemma/en/bnc/$1.bnc.txt.words.txt $1.txt
}

#stem FICTION
#stem ACPROSE
#stem CONVRSN
#stem NEWS
stem NONAC
#stem OTHERPUB
#stem OTHERSP
#stem UNPUB
exit
./eval.sh

