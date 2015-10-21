

# extract words and their lemmas from NBC (National British Corpus)

#DIR=/common/resources/corpora/BNC_XML_EDITION_cd/unzippedTexts
DIR=sample
mkdir bnc

function convertBNCdirectory(){
    for f in $1/*.xml
    do
      echo "converting file $f ..."
      python extractWordsBNC.py $f > ./bnc/$(basename $f).txt
    done
}

# one directory
#convertBNCdirectory /common/resources/corpora/BNC_XML_EDITION_cd/unzippedTexts/A/A0


for f in $DIR/*
    do
      echo "converting dir $f ..."
      find $f -type d | while read -r line; do convertBNCdirectory "$line"; done;
    done


# clean previous generated files
rm ./bnc/*.txt

# unify texts in each domain
for f in ./bnc/*
    do
      echo "concat dir $f ..."
      cat $f/*.txt >> ./bnc/$(basename $f).bnc.txt
    done


for f in ./bnc/*.txt
    do
      echo "generate input words $f ..."
      perl -pe "s/(.*?)\t.*?\n/\1\n/" $f > tmp
      perl -pe "s/^\n//" tmp > $f.words.txt
    done

