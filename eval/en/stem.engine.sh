
WORDSPATH=../../corpus/goldLemma/en/bnc
#HUMOR
#~/humor/bin/stem2005Console ~/humor/bin/huau.lex ~/humor/bin/huastem.lex 1038 65001 -filter_stem -output_stem -file $WORDSPATH/domain.$1.utf.words > humor/domain.$1.txt
#-build_cache
#exit
#foma
#cd ../hunmorph-foma-hunmorph-foma
#cat ../szeged/data/$1.utf.words | ../linux64/flookup -x hun0530.foma > ../szeged/foma/$1.txt
# javitott foma:
#cd ../hunmorph-foma-hunmorph-fomaIK
#cat ../szeged/data/$1.utf.words | ../linux64/flookup -x hun0923.foma > ../szeged/foma/$1.txt
#cd ../szeged

#hunspell
HUNSPELLPATH=~/projects/stemmers/hunspell
time java -cp $HUNSPELLPATH:$HUNSPELLPATH/hunspell.jar:$HUNSPELLPATH/jna.jar MyStemFilter $HUNSPELLPATH/dicts/en_US $1 > ./hunspell/$2


#kstem
cd ../../java/stemmertester
#java -cp .:hunspell.jar:jna.jar MyStemFilter dicts/hu_HU ../szeged/data/$1.utf.words > ../szeged/hunspell/$1.txt
#cd ../szeged
LUC=lucene-core-4.5.0.jar:lucene-analyzers-common-4.5.0.jar:lucene-analyzers-stempel-4.5.0.jar:lucene-analyzers-morfologik-4.5.0.jar:morfologik-fsa-1.7.1.jar:morfologik-polish-1.7.1.jar:morfologik-stemming-1.7.1.jar
OUTD=../../eval/en

#time java -cp .:$LUC LuceneStemmerTester en_porter $1 > $OUTD/porter/$2 lower
#exit
time java -cp .:$LUC LuceneStemmerTester en_kstem $1 > $OUTD/kstem/$2
#time java -cp .:$LUC LuceneStemmerTester en_minimal $1 > $OUTD/enminimal/$2
cd $OUTD


#snowball
#python3 snowballTest.py hungarian data/$1.utf.words > snowball/$1.txt

# ocamorph
#../hunmorph/ocamorph --compounds --bin ../hunmorph/morphdb_hu.bin --in data/$1.iso.words > ocamorph/$1.txt

# ocastem
#default:
#cat data/$1.iso.words | ../ocastem/ocamorph-1.1-linux/ocastem --bin ../ocastem/morphdb_hu.20070606.bin > ocastem/$1.txt
# sok kapcsolo
#cat data/$1.iso.words | ../ocastem/ocamorph-1.1-linux/ocastem --bin ../ocastem/morphdb_hu.20070606.bin --lowercase no --decompounding no --stem-known all > ocastem/$1.txt
#kevesebb
#cat data/$1.iso.words | ../ocastem/ocamorph-1.1-linux/ocastem --bin ../ocastem/morphdb_hu.20070606.bin --lowercase no --decompounding no > ocastem/$1.txt
#meg kevesebb
#cat data/$1.iso.words | ../ocastem/ocamorph-1.1-linux/ocastem --bin ../ocastem/morphdb_hu.20070606.bin --decompounding no  > ocastem.decomp/$1.txt

# ujabb Attila keres
#cat data/$1.iso.words | ../ocastem/ocamorph-1.1-linux/ocastem --bin ../ocastem/morphdb_hu.20070606.bin --decompounding no --stem-known all > ocastem/$1.txt