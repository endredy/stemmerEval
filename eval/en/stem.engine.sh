
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
JLIB=../../java/stemmertester
#java -cp .:hunspell.jar:jna.jar MyStemFilter dicts/hu_HU ../szeged/data/$1.utf.words > ../szeged/hunspell/$1.txt
LUC=$JLIB/lucene-core-4.5.0.jar:$JLIB/lucene-analyzers-common-4.5.0.jar:$JLIB/lucene-analyzers-stempel-4.5.0.jar:$JLIB/lucene-analyzers-morfologik-4.5.0.jar:$JLIB/morfologik-fsa-1.7.1.jar:$JLIB/morfologik-polish-1.7.1.jar:$JLIB/morfologik-stemming-1.7.1.jar
OUTD=../../eval/en

#time java -cp .:$LUC LuceneStemmerTester en_porter $1 > $OUTD/porter/$2 lower
echo kstem
time java -cp $JLIB:$LUC LuceneStemmerTester en_kstem $1 > $OUTD/kstem/$2
#time java -cp .:$LUC LuceneStemmerTester en_minimal $1 > $OUTD/enminimal/$2

#snowball
#python3 snowballTest.py english data/$1.utf.words > snowball/$1.txt
