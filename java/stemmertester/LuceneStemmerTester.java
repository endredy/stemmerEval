import java.io.Reader;
import java.io.StringReader;
import java.io.IOException;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;

import java.util.*;
import java.io.*;


import java.util.List;
import java.util.ArrayList;

import org.apache.lucene.analysis.Tokenizer; //ei
import org.apache.lucene.analysis.core.*;

import org.apache.lucene.analysis.Analyzer.TokenStreamComponents;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.en.*;//KStemFilter;
import org.tartarus.snowball.ext.EnglishStemmer;
import org.apache.lucene.analysis.snowball.SnowballFilter;
import org.apache.lucene.analysis.hu.*;
import org.apache.lucene.analysis.pl.*;
import org.apache.lucene.analysis.stempel.*;
import org.apache.lucene.analysis.morfologik.*;
import org.apache.lucene.analysis.standard.StandardTokenizer;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;
import org.apache.lucene.util.Version;

public class LuceneStemmerTester {

    public static void mainBackup(String[] args) throws Exception {

        MyAnalyzer analyzer = new MyAnalyzer();

		analyzer.setType("en_porter");
        String str = "alma logs balls boxes children men feet as was going japanese baba-jaga ";

//        Reader reader = new StringReader(str);
        TokenStream stream = analyzer.tokenStream("", str);//new StringReader(str));
		System.out.println(stem(stream) + "|");

		str = new String("apple pie");
		stream = analyzer.tokenStream("", str);
		System.out.println(stem(stream) + "|");
		
		stream = analyzer.tokenStream("", "spies on the tables");
		System.out.println(stem(stream) + "|");
    }
	
	public static void main(String[] args) {

		if (args.length < 2){
		    System.out.println("<dict path> <input file> <lower, optional>");
		    return;
		}
		boolean lower = false; //def
		if (args.length > 2 && args[2].equals("lower"))
		    lower = true;			
        MyAnalyzer analyzer = new MyAnalyzer();
		//set stemmer type
		if (analyzer.setType(args[0]) == false){
		    System.out.println("invalid stemmer type: " + args[0]);
		    return;			
		}
		TokenStream stream = null;
	    

		try {

                BufferedReader in = new BufferedReader(new InputStreamReader(new FileInputStream(args[1]), "UTF-8"));
                while(in.ready()) {
					String line = in.readLine();
					if (lower) line = line.toLowerCase();
					stream = analyzer.tokenStream("", line);
					List<String> stems = stem(stream); //tokenizeString(analyzer, line); //
					System.out.println(line);
					for(String s : stems){
						System.out.println("\t" + s);
					}
                }
                

            } catch (UnsupportedEncodingException e) {
				System.out.println("UnsupportedEncodingException ");                    
            } catch (IOException e) {
				System.out.println("io error " + e.getMessage());                    
			} catch (Exception e) {
				System.out.println("exception " + e.getMessage());                    
			}
		
	}	


	//=====================
	public static List<String> tokenizeString(Analyzer analyzer, String string) {
		List<String> result = new ArrayList<String>();
		//System.out.println("tokenizeString: " + string);
		try {
	//	TokenStreamComponents t = analyzer.createComponents("", new StringReader(string));
	//	TokenStream stream  = t.getTokenStream();
		  TokenStream stream = analyzer.tokenStream("", new StringReader(string));
		  stream.reset();
		  while (stream.incrementToken()) {
			result.add(stream.getAttribute(CharTermAttribute.class).toString());
		  }
	//    stream.end();
	//stream.end(); stream.close();
		} catch (IOException e) {
		  // not thrown b/c we're using a string reader...
		  throw new RuntimeException(e);
		}
		return result;
	}
	
    public static List<String> stem(TokenStream stream) throws Exception{
        List<String> result = new ArrayList<String>();
		stream.reset();
        while (stream.incrementToken()) {
            CharTermAttribute term = stream.getAttribute(CharTermAttribute.class);
			result.add(term.toString());
        }
		stream.end();
		return result;
    }

    static class MyAnalyzer extends Analyzer {
		private String type;
		public boolean setType(String s){
			type = s;
			//System.out.println("setType");
			return true; //TODO: check

		}
/*        public final TokenStream tokenStream(String fieldName, Reader reader) {
            TokenStream result = new StandardTokenizer(Version.LUCENE_41, reader);
            result = new KStemFilter(result);
            return result;
        }
*/

	   @Override
	   protected TokenStreamComponents createComponents(String fieldName, Reader reader) {
		 //Tokenizer source = new FooTokenizer(reader);

		//System.out.println("createComp");
	//    final 
		Tokenizer source = new WhitespaceTokenizer(Version.LUCENE_45, reader);
		TokenStream result = new StandardTokenizer(Version.LUCENE_45, reader);

	// EN
		if (type.equals("en_kstem"))
			result = new KStemFilter(result);
		else if (type.equals("en_porter"))
			result = new PorterStemFilter(result);
		else if (type.equals("en_minimal"))    
			result = new EnglishMinimalStemFilter(result);
		else if (type.equals("en_snowball"))
			result = new SnowballFilter(result, new EnglishStemmer());
	// HU
		else if (type.equals("hu_light"))
			result = new HungarianLightStemFilter(result);
		
	// PL
	 // 3 opcio: hunspell + ez a ketto  (http://solr.pl/en/2012/04/02/solr-4-0-and-polish-language-analysis/)
		else if (type.equals("pl_stempel"))
			result = new StempelFilter(result, new StempelStemmer(PolishAnalyzer.getDefaultTable()));
		else if (type.equals("pl_morfologik"))
			result = new MorfologikFilter(result, /*morfologik.stemming.PolishStemmer.DICTIONARY.COMBINED, */Version.LUCENE_45);

	//    MORFOLOGIK
	//    MORFEUSZ
	//    COMBINED


		return new TokenStreamComponents(source, result);
	   }
    }
}