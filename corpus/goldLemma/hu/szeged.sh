
# this script converts sentences of Szeged Tree Bank 2.0 into stemmer evaluation form: words and their lemmas
#  Szeged Tree Bank 2.5: many suffixes are removed from lemma (hat/het, gat/get), so many stemmers makes errors. I cannot fine tune each stemmer (only few of them), therefore SZTB 2.0 is used instead.

GOLDDATAPATH=data
#SZEGEDTREEBANK_PATH=/common/resources/corpora/szeged_treebank_2
SZEGEDTREEBANK_PATH=sample


function prepareInput(){
 python extractWords.py $1 > $GOLDDATAPATH/$2.txt
 iconv -f "ISO-8859-2" -t "UTF-8" $GOLDDATAPATH/$2.txt > $GOLDDATAPATH/$2.utf.txt
 perl -pe "s/^\n//" $GOLDDATAPATH/$2.utf.txt > tmp
 perl -pe "s/\t[^\n]+\n/\n/" tmp > $GOLDDATAPATH/$2.utf.words
 rm tmp
}

prepareInput $SZEGEDTREEBANK_PATH/newspapers/np.xml  np
#exit
prepareInput $SZEGEDTREEBANK_PATH/newspapers/nv.xml  nv
prepareInput $SZEGEDTREEBANK_PATH/newspapers/hvg.xml  hvg
prepareInput $SZEGEDTREEBANK_PATH/newspapers/mh.xml  mh
prepareInput $SZEGEDTREEBANK_PATH/law/gazdtar.xml   gazdtar
prepareInput $SZEGEDTREEBANK_PATH/law/szerzj.xml  szerzj

prepareInput $SZEGEDTREEBANK_PATH/compositions/10elb.xml  10elb
prepareInput $SZEGEDTREEBANK_PATH/compositions/10erv.xml  10erv
prepareInput $SZEGEDTREEBANK_PATH/compositions/8oelb.xml  8oelb
prepareInput $SZEGEDTREEBANK_PATH/business-news/newsml.xml  newsml
prepareInput $SZEGEDTREEBANK_PATH/fiction/1984.xml 1984

prepareInput $SZEGEDTREEBANK_PATH/fiction/pfred.xml pfred
prepareInput $SZEGEDTREEBANK_PATH/fiction/utas.xml utas
prepareInput $SZEGEDTREEBANK_PATH/computer/cwszt.xml cwszt
prepareInput $SZEGEDTREEBANK_PATH/computer/win2000.xml win2000

# newsp humor "np nv .."
function createDomain(){
rm -f $GOLDDATAPATH/domain.$1.utf.txt
for f in $2
    do
	echo "Processing $f"
        cat $GOLDDATAPATH/$f.utf.txt >> $GOLDDATAPATH/domain.$1.utf.txt
        cat $GOLDDATAPATH/$f.utf.words >> $GOLDDATAPATH/domain.$1.utf.words
    done
}

createDomain newsp "np nv hvg mh"
createDomain law "gazdtar szerzj"
createDomain comp "10elb 10erv 8oelb"
createDomain busin "newsml"
createDomain fict "1984 pfred utas"
createDomain it "cwszt win2000"
