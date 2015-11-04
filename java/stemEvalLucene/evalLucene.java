package stemEvalLucene;

// 5.3 http://lucene.apache.org/core/5_3_1/demo/overview-summary.html#overview_description
// http://blog.swwomm.com/2013/07/tuning-lucene-to-get-most-relevant.html

//package org.apache.lucene.demo;

/*
* Licensed to the Apache Software Foundation (ASF) under one or more
* contributor license agreements.  See the NOTICE file distributed with
* this work for additional information regarding copyright ownership.
* The ASF licenses this file to You under the Apache License, Version 2.0
* (the "License"); you may not use this file except in compliance with
* the License.  You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/


import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.Tokenizer;
import org.apache.lucene.analysis.core.StopFilter;
import org.apache.lucene.analysis.core.WhitespaceTokenizer;
import org.apache.lucene.analysis.en.EnglishMinimalStemFilter;
import org.apache.lucene.analysis.en.EnglishPossessiveFilter;
import org.apache.lucene.analysis.en.KStemFilter;
import org.apache.lucene.analysis.en.PorterStemFilter;
import org.apache.lucene.analysis.hu.HungarianLightStemFilter;
import org.apache.lucene.analysis.miscellaneous.KeywordRepeatFilter;
import org.apache.lucene.analysis.miscellaneous.RemoveDuplicatesTokenFilter;
import org.tartarus.snowball.ext.EnglishStemmer;
import org.tartarus.snowball.ext.HungarianStemmer;

import stemEvalLucene.MyStemFilter.StemmerType;

import org.apache.lucene.analysis.snowball.SnowballFilter;
import org.apache.lucene.analysis.standard.StandardFilter;
import org.apache.lucene.analysis.stempel.StempelFilter;
import org.apache.lucene.analysis.stempel.StempelStemmer;
import org.apache.lucene.analysis.util.CharArraySet;
import org.apache.lucene.analysis.pl.PolishAnalyzer;
import org.apache.lucene.analysis.morfologik.MorfologikFilter;

import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.document.LongField;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig.OpenMode;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.Term;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.FileVisitResult;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.SimpleFileVisitor;
import java.nio.file.attribute.BasicFileAttributes;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.Set;

import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.queryparser.classic.ParseException;

//import org.apache.pdfbox.lucene.LucenePDFDocument;
//import org.apache.pdfbox.pdmodel.PDDocument;
//
//import org.apache.pdfbox.util.PDFTextStripper;
//import org.apache.pdfbox.util.TextNormalize;
//import org.apache.poi.hslf.extractor.PowerPointExtractor;
//import org.apache.poi.hssf.extractor.ExcelExtractor;
//import org.apache.poi.hwpf.extractor.WordExtractor;
//import org.apache.poi.poifs.filesystem.POIFSFileSystem;
//import org.json.JSONArray;
//import org.json.JSONException;
//import org.json.JSONObject;

import java.io.FileNotFoundException;


/** Corpus based evaluation of stemmers, by the help of Lucene
* <p>
* This is a command-line application evaluating stemmers of Lucene.
* Run it with the config file, which describes the tested stemmers, path of indexing documents and IR gold standard.
* 
* 
* "The main idea of this article is that every corpus with lemmas can be used 
* as an IR evaluation data set. In the tool presented here, every sentence in the corpus 
* will be the result item of an IR (hit), and its words (in their original forms) are the queries. 
* These word-sentence connections will be used as a gold standard, and each stemmer will be tested
* against this: calculation of precision and recall is based on the sets of sentences determined 
* by stemmers and by the gold standard.
* 
* On the one hand, the tool contains a Lucene evaluation java code as well: sentences of the corpora 
* (as separate documents) are indexed by stemmers, and each word (as a query) gets a result set which 
* is compared to the gold standard. This is a classical collection set based evaluation, but the 
* collection is big (millions of doc) and it is made automatically from the corpus. This java code 
* evaluates in two ways: evaluates all result items, and evaluates only the first n results. 
* This latter option reflects the mode when a human verifies the results: only the first n items matter."
* 
*/
//https://www.elastic.co/guide/en/elasticsearch/guide/current/choosing-a-stemmer.html
public class evalLucene {

	private MyAnalyzer analyzer;
	
	/**
	 * a corpus usually has more domains (newspaper, literature, etc)
	 * They are evaluated separately, to give comparable overview a stemmer between domains.
	 * This class contains the parameters of a domain:
	 *  path of documents
	 *  path of indexes
	 *  path of gold standard (all input words and their doc ids)
	 * */
    private class catalog{
    	
    	/**
    	 * constructor, 
    	 * @param docPath input, path of documents
    	 * @param indexPath path of indexes (where they will be)
    	 * @param goldPath path of gold standard
    	 * */
    	public catalog(String docPath, String indexPath, String goldPath) {
			this.docPath = docPath;
			this.indexPath = indexPath;
			this.goldPath = goldPath;
		}
		protected String docPath;
    	protected String indexPath;
    	protected String goldPath;
    }
    
    /**
     * This class contains the intermediate results of a stemmer in each domain.
     * Finally, it counts a total as well.
     * */
    private class stemmerResults{
    	private Map<String, Map<String, String>> evals = new HashMap<String, Map<String, String>>();
    	private Map<String, Long> totals = new HashMap<String, Long>();
    	
    	private void addResult(String stemmer, String domain, float F,
    			long tp, long fp, long fn){
    		Map<String, String> curr = evals.get(domain);
    		if (curr == null){
    			curr = new HashMap<String, String>();
    			evals.put(domain, curr);
    		}
   			curr.put(stemmer, String.valueOf(F));
   			
   			addTotal(stemmer, "tp", tp);
   			addTotal(stemmer, "fp", fp);
   			addTotal(stemmer, "fn", fn);
   			
    	}
    	private void addTotal(String stemmer, String name, long value){
    		Long t = totals.get(stemmer + name);
   			if (t != null)
   				value += t.longValue();
   			totals.put(stemmer + name, new Long(value));
    	}

    	private void printSummaMetric(){
    		//print 1st row: every stemmer
    		for(Map.Entry<String, Map<String, String>> entry : evals.entrySet()){
    			
    			for(Map.Entry<String, String> stemmer : entry.getValue().entrySet()){
    				System.out.print("\t" + stemmer.getKey() + "\t");
    			}
    			break;
    		}
    		log("");
    		System.out.println();
    		// print each row: one domain with each stemmer
    		for(Map.Entry<String, Map<String, String>> entry : evals.entrySet()){
    			
    			System.out.print("\n" + entry.getKey());
    			for(Map.Entry<String, String> stemmer : entry.getValue().entrySet()){
    				System.out.print("\t" + stemmer.getValue());
    			}
    		}
    		
    		//total line
    		System.out.print("\ntotal"); 
    		for(Map.Entry<String, Map<String, String>> entry : evals.entrySet()){
    			
    			
    			for(Map.Entry<String, String> stemmer : entry.getValue().entrySet()){
    				long tp=0, fp=0, fn=0;
    				//System.out.print(totals);
    				Long t = totals.get(stemmer.getKey() + "tp");
    				if (t != null) tp = t.longValue();
    				t = totals.get(stemmer.getKey() + "fp");
    				if (t != null) fp = t.longValue();
    				t = totals.get(stemmer.getKey() + "fn");
    				if (t != null) fn = t.longValue();
    				
    				float F = countFscore(tp, fp, fn, false);

    				System.out.print("\t" + 100*F);
    			}
    			break;
    		}
    		System.out.println();
    	}
    	
    }
	private Map<String, catalog> catalogs = new HashMap<String, catalog>();

	/** evaluation of all hit results */
	private stemmerResults fullEvals = new stemmerResults();
	/** evaluation of all the first n hit results */
	private stemmerResults limitedEvals = new stemmerResults();
	private int debugLevel = 0;
 
	// https://lucene.apache.org/core/5_2_1/core/org/apache/lucene/analysis/package-summary.html
	class MyAnalyzer extends Analyzer {

        private String type;
        private Properties dictProperties;
        /** index original word as well */
        private boolean includingOriginalTerm = false;
        /** stopwords, they are ignored by stemmers */
        private Set<String> stopwords = null;
        
        /**
         * set the type of the stemmer
         * */
        public boolean setType(String s, Properties prop){
            type = s;
            if (prop != null){
            	dictProperties = prop;
            	String tmp = prop.getProperty("includeOriginalTerm");
            	if (tmp != null && tmp.equals("1"))
            		includingOriginalTerm = true;
            	tmp = prop.getProperty("stopWordFile");
            	if (tmp != null && !tmp.isEmpty())
            		stopwords = loadStopWords(tmp);
            }
            return true; 
        }

		@Override
		/**
		 * it makes the stemming in Lucene (set as filters)
		 * */
		protected TokenStreamComponents createComponents(String fieldName) {

			Tokenizer source = new WhitespaceTokenizer(); //new LetterTokenizer();//
			
			// chain filters: http://stackoverflow.com/questions/19259314/how-to-use-multiple-filter-on-lucene-analyzer-lucene-4-4
			TokenStream filter = null; 
			if (includingOriginalTerm)
				filter = new KeywordRepeatFilter(source);
			else
				filter = source; // ha nem akarjuk
			
			if (stopwords != null && !stopwords.isEmpty()){
				CharArraySet cas = new CharArraySet(stopwords, true);
				filter = new StopFilter(filter, cas);
			}
			
			// === EN ===
			if (type.equals("en_kstem"))
		        filter = new KStemFilter(filter);
			else if (type.equals("en_porter"))
		        filter = new PorterStemFilter(filter);
			else if (type.equals("en_possessive"))
			    filter = new EnglishPossessiveFilter(filter);
			else if (type.equals("en_minimal"))
		        filter = new EnglishMinimalStemFilter(filter);
			else if (type.equals("en_snowball"))
			    filter = new SnowballFilter(filter, new EnglishStemmer());
			// === HU ===
			else if (type.equals("hu_light"))
			    filter = new HungarianLightStemFilter(filter);
			else if (type.equals("hunspell"))
			    filter = new MyStemFilter(filter, StemmerType.HUNSPELL, dictProperties);
			else if (type.equals("humor"))
			    filter = new MyStemFilter(filter, StemmerType.HUMOR, dictProperties);
			else if (type.equals("ocastem"))
			    filter = new MyStemFilter(filter, StemmerType.OCASTEM, dictProperties);
			else if (type.equals("hu_snowball"))
			    filter = new SnowballFilter(filter, new HungarianStemmer());
			// === PL ===
			// 3 options (http://solr.pl/en/2012/04/02/solr-4-0-and-polish-language-analysis/)
		    else if (type.equals("pl_stempel"))
		    	filter = new StempelFilter(filter, new StempelStemmer(PolishAnalyzer.getDefaultTable()));
		    else if (type.equals("pl_morfologik"))
		    	filter = new MorfologikFilter(filter /*morfologik.stemming.PolishStemmer.DICTIONARY.COMBINED, */);
		    else if (type.equals("nostem"))
		    	filter = new StandardFilter(filter);
		    else{
		    	log("ERROR: unknown stemmer type: " + type);
		    	filter = new StandardFilter(filter);
		    }
			
			filter = new RemoveDuplicatesTokenFilter(filter);
            return new TokenStreamComponents(source, filter);			
		}
	}
	
	public evalLucene() {
	}
 
	public void setDebugLevel(int debugLevel) {
		this.debugLevel = debugLevel;
	}

	public void addCatalog(String name, String docPath, String indexPath, String goldPath){
		if (docPath == null || indexPath == null || goldPath == null)
			log("missing docPath/indexPath/goldPath for: " + name);
		catalogs.put(name, new catalog(docPath.trim(), indexPath.trim(), goldPath.trim()));
	}

	public void setStemmer(String name, Properties prop){
		 analyzer = new MyAnalyzer();
		 analyzer.setType(name, prop); 
	}
 
	public Set<String> loadStopWords(String stopwordFile){
	    InputStream fis;
	    Set<String> stopwords = new HashSet<String>();
		try {
			fis = new FileInputStream(stopwordFile);
			BufferedReader br = new BufferedReader(new InputStreamReader(fis, Charset.forName("UTF-8")));
			String line;
			while ((line = br.readLine()) != null){
				if (line.isEmpty() || line.startsWith("#")) {
					continue; // commented out
			    }
				stopwords.add(line.trim());
			}
			br.close();
		} catch (FileNotFoundException e) {
			// stopword file not found
			log("stopword file not found (" + stopwordFile + "): " + e.getMessage());
		} catch (IOException e) {
			// error reading stopword file
			log("error at loading stopword file '" + stopwordFile + "': " + e.getMessage());
		} 
		return stopwords;
	}

	/**
	 * index the given catalog (a domain of the corpus: newspaper, literature, stc)
	 * 
	 * @param catalogName name of the catalog (domain)
	 * @param create create index (removing any previous index) or just update
	 * */
	public boolean index(String catalogName, boolean create){

		try {
		
			catalog c = catalogs.get(catalogName);
			if (c == null){
				log("unknown catalog: " + catalogName);
				return false;
			}
			String docsPath = c.docPath;
			String indexPath = c.indexPath;
	
			final Path docDir = Paths.get(docsPath);
			if (!Files.isReadable(docDir)) {
				log("Document directory '" +docDir.toAbsolutePath()+ "' does not exist or is not readable, please check the path");
				return false;
			}
			Date start = new Date();
	
			log("Indexing to directory '" + indexPath + "'...");
			
			Directory dir = FSDirectory.open(Paths.get(indexPath));
			IndexWriterConfig iwc = new IndexWriterConfig(analyzer);
			
			if (create) {
				// Create a new index in the directory, removing any
				// previously indexed documents:
				iwc.setOpenMode(OpenMode.CREATE);
			} else {
				// Add new documents to an existing index:
				iwc.setOpenMode(OpenMode.CREATE_OR_APPEND);
			}
			
			// Optional: for better indexing performance, if you
			// are indexing many documents, increase the RAM
			// buffer.  But if you do this, increase the max heap
			// size to the JVM (eg add -Xmx512m or -Xmx1g):
			//
			// iwc.setRAMBufferSizeMB(256.0);
			
			IndexWriter writer = new IndexWriter(dir, iwc);
	
			indexDocs(writer, docDir);
			
			writer.close();
			Date end = new Date();
			log(new String(" " + (end.getTime() - start.getTime()) + " total milliseconds"));
		
		} catch (IOException e) {
			log(e.getMessage());
			return false;
		}
		return true;
	}
	
	private static void log(String str) {
		SimpleDateFormat dformat = new SimpleDateFormat("yyyy.MM.dd. HH:mm:ss");
		System.out.println( dformat.format(new Date()) + " " + str );
		
	}

	/**
	 * it counts the harmonic mean of the recall and the average precision
	 * 
	 * @param tp number of true positive items
	 * @param fp number of false positive items
	 * @param fn number of false negative items
	 * @param print precision and recall should be printed or not
	 * 
	 * @return F-score
	 * 
	 * */
	private float countFscore(long tp, long fp, long fn, boolean print){
		float prec = tp+fp==0 ? 0 : (float)tp / (tp + fp);
		float rec = tp+fn==0 ? 0 : (float)tp / (tp + fn);
		float F = 2*prec*rec / (prec + rec);
		if (print) log("  F = " + F + " (prec = "+prec+", rec = "+rec+")");
		return F;
	}
	
	private void printMetric(String metric, String stemmer, String domain, long tp, long fp, long fn){
	
		log("  tp = "+tp+", fp = "+fp+", fn = "+fn);
		float F = countFscore(tp, fp, fn, true);

		
		if (metric.equals("full")){
			fullEvals.addResult(stemmer, domain, 100*F, tp, fp, fn);
		}else{
			limitedEvals.addResult(stemmer, domain, 100*F, tp, fp, fn);
		}
	}
	
	private void printSumma(){
		
		System.out.println("full");
		fullEvals.printSummaMetric();
		
		System.out.println("limited");
		limitedEvals.printSummaMetric();
	}
	

	/**
	 * evaluate the given catalog (domain):
	 * each word is queried, and the result set is compared to the gold standard.
	 * True positive, false positive and false negative results are counted, and finally F-score as well
	 * 
	 * There are two evaluations: all result items are evaluated and the first n items.
	 * Latter is able to evaluate the ranking algorithm of the IR itself.
	 * 
	 *  format of gold standard file (from catalog.xxx.goldPath in config file): <br/>
	 *   <original word form> <sentence id list, where this word is occured> <br/>
	 *   marries 473 <br/>
	 *   epidemic        24,241 <br/>
	 *   simple  736,656,677,88,601,701,655 <br/>
	 *   varied  597 <br/><br/>
	 *   
	 *  @param catalogName name of the catalog (newspaper, literature, etc)
	 *  @param limit limit of the limited evaluation: the first &lt;limit&gt; results are evaluated separately  
	 * */
	public void evaluate(String catalogName, int limit){
		
		Date start = new Date();
		catalog c = catalogs.get(catalogName);
		long tp=0, fp=0, fn=0;
		long fullTP=0, fullFP=0, fullFN=0;
		FileInputStream fis;
		BufferedReader reader;
		try {
			fis = new FileInputStream(new File(c.goldPath));
			reader = new BufferedReader(new InputStreamReader(fis, "UTF-8"));
			String         line = null;
	
			while( ( line = reader.readLine() ) != null ) {
				String[] part = line.split("\t");
				if (part.length != 2) continue; // invalid line
				List<String> r = query(part[0], catalogName, 0); // it gives all the hits
				String[] goldList = part[1].split(",");
				Set<String> curr = new HashSet<String>(r);
				Set<String> gold = new HashSet<String>(Arrays.asList(goldList));
				Set<String> intersection = new HashSet<String>(gold);
				intersection.retainAll(curr); // transforms s1 into the intersection of s1 and s2. (The intersection of two sets is the set containing only the elements common to both sets.)
//				int positive = intersection.size();
				fullTP += intersection.size();
				
				if (debugLevel > 1){
					log("in:" + part[0]);
					log(" tp:" + intersection);
				}
				Set<String> num = new HashSet<String>(gold);
				num.removeAll(curr); // transforms s1 into the (asymmetric) set difference of s1 and s2. (For example, the set difference of s1 minus s2 is the set containing all of the elements found in s1 but not in s2.
				fullFN += num.size();
//				long egyik = num.size();
				if (debugLevel > 1){
					log(" fn:" + num);
				}
				
				num = new HashSet<String>(curr);
				num.removeAll(gold); 
				fullFP += num.size();
				if (debugLevel > 1){
					log(" fp:" + num);
				}
				
				//calculate only the 1st n hits
				// 	we use only the first n (=limit) hits
				int subsize = r.size() < limit ? r.size() : limit;
				
				Set<String> firstNRes = new HashSet<String>(r.subList(0, subsize));
				intersection = new HashSet<String>(gold);
				intersection.retainAll(firstNRes); // transforms s1 into the intersection of s1 and s2. (The intersection of two sets is the set containing only the elements common to both sets.)
				tp += intersection.size();
				
				num = new HashSet<String>(gold);
				num.removeAll(firstNRes); // transforms s1 into the (asymmetric) set difference of s1 and s2. (For example, the set difference of s1 minus s2 is the set containing all of the elements found in s1 but not in s2.
				fn += num.size();
				
				Set<String> numfp = new HashSet<String>(firstNRes);
				numfp.removeAll(gold); 
				fp += numfp.size();
				
				// a limit felettieket csak log() mertekben veszi figyelembe
				/*if (r.size() < limit) continue;
				firstNRes = new HashSet<String>(r.subList(subsize, r.size()));
				intersection.retainAll(firstNRes); // transforms s1 into the intersection of s1 and s2. (The intersection of two sets is the set containing only the elements common to both sets.)
				if (intersection.size() > 0)
					tp += Math.log10(intersection.size());
				
				int missingFromGold = num.size();
				num.removeAll(firstNRes); //ami az goldbol hianyzik, es ebben a tartomanyban van, az nem gaz, de ezt hozzaadjuk 
				if (missingFromGold - num.size() > 0)
					fn -= Math.log10(missingFromGold - num.size()); // ezeket mar korabban levontuk, de itt (kesobb) megtalalhatoak voltak
				
				numfp = new HashSet<String>(firstNRes);
				numfp.removeAll(gold); 
				if (numfp.size() > 0)
					fp += Math.log10(numfp.size());*/

			}
			reader.close();
			Date end = new Date();
			log(new String(" " + (end.getTime() - start.getTime()) + " total milliseconds"));

			
			log(" evaluating '" + analyzer.type + "' in " + catalogName+" with the 1st "+limit+" hits");
			printMetric("limited", analyzer.type, catalogName, tp, fp, fn);

			log(" evaluating '" + analyzer.type + "' in " + catalogName+" with all hits");
			printMetric("full", analyzer.type, catalogName, fullTP, fullFP, fullFN);
			
		} catch (FileNotFoundException e) {
			log(e.getMessage());
		} catch (UnsupportedEncodingException e) {
			log(e.getMessage());
		} catch (IOException e) {
			log(e.getMessage());
		} 
	}
	
	/**
	 * give the id list of sentences, from Lucene index
	 * 
	 * @param input input word
	 * @param catalogName catalog (domain) name which we'd like to search in
	 * @param limit how many hits are needed (0 means all)
	 * */
	public List<String> query(String input, String catalogName, int limit){

		List<String> res = new ArrayList<String>();
		try {  		
			
			catalog c = catalogs.get(catalogName);
			IndexReader reader = DirectoryReader.open(FSDirectory.open(Paths.get(c.indexPath)));
			IndexSearcher searcher = new IndexSearcher(reader);
			
			QueryParser parser = new QueryParser("contents", analyzer);
			Query query = parser.parse(QueryParser.escape(input));
			
			int n = limit > 0 ? limit : searcher.count(query);
			if (n == 0)
				n = 1;
			TopDocs results = searcher.search(query, n);
	
			int endPos = limit;
			if (limit != 0)
				endPos = Math.min(results.totalHits, limit); // 1st n hits
			else
				endPos = results.totalHits; //all hits 
			
			for (int i = 0; i < endPos; i++) {
				int id = results.scoreDocs[i].doc;
				Document doc = searcher.doc(id);
				res.add(doc.get("filename"));
			}
			reader.close();
	      return res;
	      
	  	} catch (ParseException e) {
	  		log(e.getMessage());
	  	} catch (IOException e) {	
	  		log(e.getMessage());
	  	}
		return res;
	}

	  
/**
* Indexes the given file using the given writer, or if a directory is given,
* recurses over files and directories found under the given directory.
* 
* NOTE: This method indexes one document per input file.  This is slow.  For good
* throughput, put multiple documents into your input file(s).  An example of this is
* in the benchmark module, which can create "line doc" files, one document per line,
* using the
* <a href="../../../../../contrib-benchmark/org/apache/lucene/benchmark/byTask/tasks/WriteLineDocTask.html"
* >WriteLineDocTask</a>.
*  
* @param writer Writer to the index where the given file/dir info will be stored
* @param file The file to index, or the directory to recurse into to find files to index
* @throws IOException If there is a low-level I/O error
*/
private void indexDocs(final IndexWriter writer, Path path)
 throws IOException {
 if (Files.isDirectory(path)) {
      Files.walkFileTree(path, new SimpleFileVisitor<Path>() {
        @Override
        public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException {
          try {
            indexDoc(writer, file, attrs.lastModifiedTime().toMillis());
          } catch (IOException ignore) {
            // don't index files that can't be read.
          }
          return FileVisitResult.CONTINUE;
        }
      });
    } else {
      indexDoc(writer, path, Files.getLastModifiedTime(path).toMillis());
    }
 }
 
  /** Indexes a single document */
  static void indexDoc(IndexWriter writer, Path file, long lastModified) throws IOException {
    try (InputStream stream = Files.newInputStream(file)) {
      // make a new, empty document
      Document doc = new Document();
      
      // Add the path of the file as a field named "path".  Use a
      // field that is indexed (i.e. searchable), but don't tokenize 
      // the field into separate words and don't index term frequency
      // or positional information:
      Field pathField = new StringField("path", file.toString(), Field.Store.YES);
      doc.add(pathField);
      
      String f = file.getFileName().toString();
      f = f.replaceFirst("\\.txt", "");
      doc.add(new StringField("filename", f, Field.Store.YES));
      
      // Add the last modified date of the file a field named "modified".
      // Use a LongField that is indexed (i.e. efficiently filterable with
      // NumericRangeFilter).  This indexes to milli-second resolution, which
      // is often too fine.  You could instead create a number based on
      // year/month/day/hour/minutes/seconds, down the resolution you require.
      // For example the long value 2011021714 would mean
      // February 17, 2011, 2-3 PM.
      doc.add(new LongField("modified", lastModified, Field.Store.NO));
      
      // Add the contents of the file to a field named "contents".  Specify a Reader,
      // so that the text of the file is tokenized and indexed, but not stored.
      // Note that FileReader expects the file to be in UTF-8 encoding.
      // If that's not the case searching for special characters will fail.
      doc.add(new TextField("contents", new BufferedReader(new InputStreamReader(stream, StandardCharsets.UTF_8))));
      if (writer.getConfig().getOpenMode() == OpenMode.CREATE) {
        // New index, so we just add the document (no old document can be there):
        //log("adding " + file);
        writer.addDocument(doc);
      } else {
        // Existing index (an old copy of this document may have been indexed) so 
        // we use updateDocument instead to replace the old one matching the exact 
        // path, if present:
        //log("updating " + file);
        writer.updateDocument(new Term("path", file.toString()), doc);
      }
    }
  }

	 
	/** Evaluate some stemmers with the help of gold standard, generated from a corpus */
	public static void main(String[] args) {
		
		String configFile = "stemEval.config";
		
		// custom config file:
		for ( int i=0; i<args.length; ++i ){
			if(args[i].equalsIgnoreCase("-c"))
				configFile = args[i+1];
		}
		
		try {
			InputStream is = new FileInputStream(configFile);
			Properties prop = new Properties();
			prop.load(is);
			
			evalLucene c = new evalLucene();
			
			c.setDebugLevel(Integer.parseInt(prop.getProperty("debugLevel", "0")));
			String[] stemmersToTests = ((String)prop.get("stemmerName")).split(",");
			String[] catalogs = ((String)prop.get("catalog.names")).split(",");
			for (String cat : catalogs) {
				c.addCatalog(cat, 
						(String)prop.get("catalog."+cat+".docPath"), 
						(String)prop.get("catalog."+cat+".indexPath"),
						(String)prop.get("catalog."+cat+".goldPath"));
			}
			
			boolean skipIndexing = prop.get("index").equals("0");
			int limit = 200;
			if (prop.getProperty("limit").isEmpty() == false)
				limit = Integer.parseInt(prop.getProperty("limit"));
			
			for (String stemmer : stemmersToTests){
			
				c.setStemmer(stemmer, prop);//"C:/data/projects/workspace/stemEvalLucene/dicts/hu_HU");
				for (String cat : catalogs) {
					if (skipIndexing)
						log("indexing " + cat + " is skipped");
					else{
						log("indexing " + cat + " with '" + stemmer + "'...");
						c.index(cat, true);
					}	
					log("query " + cat + "...");
					c.evaluate(cat, limit);
				}
			}
			c.printSumma();
			log("test is done");
	
		} catch (IOException e) {
			log(e.getMessage());
			e.printStackTrace(); //perhaps we have even no config and/or log file, so print it
		}
	}
}