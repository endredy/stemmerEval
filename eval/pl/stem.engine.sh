
JLIB=../../java/stemmertester
#JLIB=../../java/lib
LUC=$JLIB/lucene-core-4.5.0.jar:$JLIB/lucene-analyzers-common-4.5.0.jar:$JLIB/lucene-analyzers-stempel-4.5.0.jar:$JLIB/lucene-analyzers-morfologik-4.5.0.jar:$JLIB/morfologik-fsa-1.7.1.jar:$JLIB/morfologik-polish-1.7.1.jar:$JLIB/morfologik-stemming-1.7.1.jar
OUTD=../../eval/pl

echo "pl stempel..."
time java -cp $JLIB:$LUC LuceneStemmerTester pl_stempel $1 > $OUTD/stempfel/$2
echo "pl morfologik"
time java -cp $JLIB:$LUC LuceneStemmerTester pl_morfologik $1 > $OUTD/morfologik/$2
#cd $OUTD
#exit

#HUMOR
#time ~/humor/bin/stem2005Console ~/humor/bin/pl6mor.lex ~/humor/bin/plastem.lex 1045 65001 -filter_stem -output_stem -file $1 > humor/$2

#hunspell
HUNSPELLPATH=~/projects/stemmers/hunspell
time java -cp $HUNSPELLPATH:$HUNSPELLPATH/hunspell.jar:$HUNSPELLPATH/jna.jar MyStemFilter $HUNSPELLPATH/dicts/pl_PL $1 > ./hunspell/$2
