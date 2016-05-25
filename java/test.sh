
LIBPATH=lib
LIBS=$LIBPATH/hunspell.jar:$LIBPATH/jna.jar:$LIBPATH/lucene-analyzers-common-5.3.1.jar:$LIBPATH/lucene-analyzers-morfologik-5.3.1.jar:$LIBPATH/lucene-analyzers-stempel-5.3.1.jar:$LIBPATH/lucene-core-5.3.1.jar:$LIBPATH/lucene-queryparser-5.3.1.jar:$LIBPATH/humor2java.jar:$LIBPATH/morfologik-fsa-1.7.1.jar:$LIBPATH/morfologik-polish-1.7.1.jar:$LIBPATH/morfologik-stemming-1.7.1.jar


# EN
#java -cp .:stemEvalLucene.jar:$LIBS  stemEvalLucene.evalLucene -c stemEval.en.config

# PL
#java -cp .:stemEvalLucene.jar:$LIBS  stemEvalLucene.evalLucene -c stemEval.pl.config

# HU
#java -cp .:stemEvalLucene.jar:$LIBS  stemEvalLucene.evalLucene -c stemEval.hu.config


