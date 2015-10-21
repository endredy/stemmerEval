
LIBPATH=lib
LIBS=$LIBPATH/hunspell.jar:$LIBPATH/jna.jar:$LIBPATH/lucene-analyzers-common-5.3.1.jar:$LIBPATH/lucene-analyzers-morfologik-5.3.1.jar:$LIBPATH/lucene-analyzers-stempel-5.3.1.jar:$LIBPATH/lucene-core-5.3.1.jar:$LIBPATH/lucene-queryparser-5.3.1.jar:$LIBPATH/humor2java.jar

DIR=/usr/lib/jvm/java-7-openjdk-amd64/bin

$DIR/javac -cp $LIBS stemEvalLucene/MyStemFilter.java stemEvalLucene/evalLucene.java
$DIR/jar cfe stemEvalLucene.jar stemEvalLucene.evalLucene stemEvalLucene/*.class




