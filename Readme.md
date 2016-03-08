# Stemmer evaluation tool

This tool evaluates stemmers in 2 ways:
* Metrics on the direct output of the stemmers (python)
* Metrics on the IR quality of the stemmers (java, with the help of Lucene)

10 stemmers in 3 languages (English, Polish, Hungarian) were evaluated based on corpora:
* English stemmers on the British National Corpus: Snowball, Porter, Kstem, En-minimal, En-possessive, Hunspell, Humor (The corpus contains more than 2,000,000 sentences from the widest possible range of linguistic productions, from several domains. Evaluation was made with the 3rd XML edition of the BNC.)
* Polish stemmers on the National Corpus of Polish: Stemfel, Morfologik, Hunspell, Humor (64,000 sentences in a  a well balanced large corpus, with several domains)
* Hungarian stemmers on Szeged Treebank: Snowball, Hunspell, Humor, Hunmorph, Ocastem (the biggest Hungarian manually annotated corpus which contains about 80,000 sentences with 1,200,000 words annotated with lemmas)

The tool is published in an article 'Corpus based evalaution of stemmers'.

## 1. extraction of words and lemmas from corpus. 
A very little sample is included (1-2 sentences), just to test the code.
First, (word, lemma) tuples for lemma accuracy:
```
corpus/goldLemma/en/bnc.sh 
corpus/goldLemma/pl/pnc.sh 
corpus/goldLemma/hu/szeged.sh 
```

Second, words and related sentences are extracted for IR evaluation:
```
/corpus/goldIR/luc.en.sh
/corpus/goldIR/luc.hu.sh 
/corpus/goldIR/luc.pl.sh 
```

The main idea of this article is that every corpus with lemmas can be used as an IR evaluation data set. In the
tool presented here, every sentence in the corpus will be the result item of an IR (hit), and its words (in their original forms) are the queries. These word-sentence connections will be used as a gold standard, and each stemmer will be tested against this: calculation of precision and recall is based on the sets of sentences determined by stemmers and by the gold standard.

## 2. Metrics on the direct output of the stemmers

If (word, lemma) tuples are extracted (see  1. step), then stemming and 6 metrics are applied to the direct output of the stemmers:
```
eval/en/stem.sh 
eval/pl/stem.sh 
eval/hu/stem.sh 
```

## 3. Metrics on the IR quality of the stemmers

If IR gold standard is generated (see 1. step), then a Lucene based java evalution is applied:

```
java\test.sh 
```
it queries all words of the corpus, and evaluates the result set against the gold standard.
the java code: 
java/stemEvalLucene/evalLucene.java 

## references:

If you use the tool, please cite the following paper:

Istvan Endredy, 2015, Corpus based evaluation of stemmers, Poznan

```
@inproceedings{endstem,
  author = {Endr{\'e}dy, Istv{\'a}n},
  booktitle = {7th Language \& Technology Conference: Human Language Technologies as a Challenge for Computer Science and Linguistics},
  editor = {Zygmunt Vetulani; Joseph Mariani},
  isbn = {978-83-932640-8-7},
  publisher = {Pozna\'n: Uniwersytet im. Adama Mickiewicza w Poznaniu},
  title = {Corpus based evaluation of stemmers},
  page = {234--239},
  year = 2015
}
```


used corpora 
```
@incollection{Clear:1993:BNC:166403.166418,
 author = {Clear, Jeremy H.},
 chapter = {The British National Corpus},
 title = {The Digital Word},
 editor = {Landow, George P. and Delany, Paul},
 year = {1993},
 isbn = {0-262-12176-x},
 pages = {163--187},
 numpages = {25},
 url = {http://dl.acm.org/citation.cfm?id=166403.166418},
 acmid = {166418},
 publisher = {MIT Press},
 address = {Cambridge, MA, USA},
} 

@inbook{Degórski_Przepiórkowski_2012, 
  title={Recznie znakowany milionowy podkorpus NKJP}, 
  booktitle={Narodowy Korpus J\c{e}zyka Polskiego}, 
  publisher={Wydawnictwo Naukowe PWN}, 
  author={Deg\'orski, {\L}ukasz and Przepi\'orkowski, Adam}, 
  editor={Przepi\'orkowski, Adam and Ba\'nko, Miros{\l}aw Tomasz and G\'orski, Rafa{\l} L. and Lewandowska-Tomaszczyk, BarbaraEditors}, 
  year={2012}, 
  pages={51--58}
}

@inproceedings{Csendes:2005,
   author={D. Csendes and J., Csirik and T, Gyim{\'o}thy and A, Kocsor},
   title={The {S}zeged {T}reebank},
   booktitle={Text, Speech and Dialogue},
   year={2005},
   pages={123--131},
   publisher={Springer}
}
```