LUC=lucene-core-4.5.0.jar:lucene-analyzers-common-4.5.0.jar:lucene-analyzers-stempel-4.5.0.jar:lucene-analyzers-morfologik-4.5.0.jar:morfologik-fsa-1.7.1.jar:morfologik-polish-1.7.1.jar:morfologik-stemming-1.7.1.jar

javac -cp $LUC LuceneStemmerTester.java
#java -cp .:$LUC LuceneStemmerTester en_kstem input.txt
java -cp .:$LUC LuceneStemmerTester en_porter input.txt lower
java -cp .:$LUC LuceneStemmerTester en_minimal input.txt lower

#java -cp .:$LUC LuceneStemmerTester hu_light input.txt
#java -cp .:$LUC LuceneStemmerTester pl_stempel input.txt
#java -cp .:$LUC LuceneStemmerTester pl_morfologik input.txt




