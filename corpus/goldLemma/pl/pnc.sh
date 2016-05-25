

function convertBNCdirectory(){
    for f in $1/*/ann_morphosyntax.xml
    do
      echo "converting file $f ..."
      python extractWordsPOL.py "$f" >> "./pnc/$(basename $f).txt"
    done
}

mkdir -p ./pnc
rm -f ./pnc/*.txt
#convertBNCdirectory /common/resources/corpora/polish_1_million
convertBNCdirectory sample

for f in ./pnc/*.txt
    do
      echo "generate input words $f ..."
      perl -pe "s/(.*?)\t.*?\n/\1\n/" $f > tmp
      perl -pe "s/^\n//" tmp > $f.words
    done

