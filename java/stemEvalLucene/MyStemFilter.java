package stemEvalLucene;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Properties;

import org.apache.lucene.analysis.TokenFilter;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;
import org.apache.lucene.analysis.tokenattributes.KeywordAttribute;
import org.apache.lucene.analysis.tokenattributes.PositionIncrementAttribute;
import org.apache.lucene.util.CharsRef;

import com.morphologic.lib.Humor;

import dk.dren.hunspell.Hunspell;
import java.util.Comparator;

/**
 * TokenFilter that uses hunspell affix rules and words to stem tokens.  Since hunspell supports a word having multiple
 * stems, this filter can emit multiple tokens for each consumed token
 */
public final class MyStemFilter extends TokenFilter {
  
	public enum StemmerType{
		HUNSPELL,
		HUMOR,
		OCASTEM
	}
  private final CharTermAttribute termAtt = addAttribute(CharTermAttribute.class);
  private final PositionIncrementAttribute posIncAtt = addAttribute(PositionIncrementAttribute.class);
  private final KeywordAttribute keywordAtt = addAttribute(KeywordAttribute.class);
  
  private StemmerType type;
  private Hunspell.Dictionary hunspell;
  //private OcaStem ocastem;
  private Humor humor;
  
  private List<CharsRef> buffer;
  private State savedState;
  
  private final boolean longestOnly;
  
  /**
   * Creates a new HunspellStemFilter that will stem tokens from the given TokenStream using affix rules in the provided
   * HunspellDictionary
   *
   * @param input TokenStream whose tokens will be stemmed
   * @param dictionary HunspellDictionary containing the affix rules and words that will be used to stem the tokens
   */
  public MyStemFilter(TokenStream input, StemmerType type, Properties props) {
    this(input, type, props, true);
  }
  
  /**
   * Creates a new HunspellStemFilter that will stem tokens from the given TokenStream using affix rules in the provided
   * HunspellDictionary
   *
   * @param input TokenStream whose tokens will be stemmed
   * @param dictionary HunspellDictionary containing the affix rules and words that will be used to stem the tokens
   * @param dedup true if only unique terms should be output.
   */
  public MyStemFilter(TokenStream input, StemmerType type, Properties dictProperties, boolean dedup) {
    super(input);
    this.longestOnly = false; //hatha akarjuk ezt...
    this.type = type;
    try {
    	if (type == StemmerType.HUNSPELL)
    		hunspell = Hunspell.getInstance().getDictionary(dictProperties.getProperty("hunspellPath"));
    	else if (type == StemmerType.HUMOR){
    		humor = new Humor("");
//    				new Humor(dictPath);
//			System.err.println("Humor library loaded");
			if (!humor.initialize(
					dictProperties.getProperty("humorPath"), 
					Integer.parseInt(dictProperties.getProperty("humorLanguageCode")), 
					Humor.SessionMode.STEM)){ //1038
//				System.err.println("Humor init failed");
		//		return;
				throw new FileNotFoundException("Humor init failed, " + dictProperties.getProperty("humorPath"));
			}
		
/*    	}else if (type == StemmerType.OCASTEM){
    		ocastem = new OcaStem();
//    		String path = "/home/pisti/projects/stemmers/ocastem/";
//    		String prog = "ocamorph-1.1-linux/ocastem";
    		//ocastem.init(path+prog, "--bin",  path+"morphdb_hu.20070606.bin", "--decompounding", "no", "--stem-known", "all");
    		ocastem.init(dictProperties.getProperty("ocastemProgPath"), 
    				"--bin",  dictProperties.getProperty("ocastemBinPath"),
    				"--decompounding", "no", 
    				"--stem-known", "all");
    		
*/    	}
	} catch (FileNotFoundException e) {
		// TODO Auto-generated catch block
		e.printStackTrace();
	} catch (UnsupportedEncodingException e) {
		// TODO Auto-generated catch block
		e.printStackTrace();
	} catch (UnsatisfiedLinkError e) {
		// TODO Auto-generated catch block
		e.printStackTrace();
	} catch (UnsupportedOperationException e) {
		// TODO Auto-generated catch block
		e.printStackTrace();
	}
  }

  /**
   * {@inheritDoc}
   */
  @Override
  public boolean incrementToken() throws IOException {
    if (buffer != null && !buffer.isEmpty()) {
      CharsRef nextStem = buffer.remove(0);
      restoreState(savedState);
      posIncAtt.setPositionIncrement(0);
      termAtt.setEmpty().append(nextStem);
      return true;
    }
    
    if (!input.incrementToken()) {
      return false;
    }
    
    if (keywordAtt.isKeyword()) {
      return true;
    }
    
    buffer = getStemList(termAtt.buffer(), termAtt.length());
    
    if (buffer.isEmpty()) { // we do not know this word, return it unchanged
      return true;
    }     

    CharsRef stem = buffer.remove(0);
    termAtt.setEmpty().append(stem);

    if (longestOnly) {
        buffer.clear();
      } else {
        if (!buffer.isEmpty()) {
          savedState = captureState();
        }
      }

    return true;
  }

  /**
   * {@inheritDoc}
   */
  @Override
  public void reset() throws IOException {
    super.reset();
    buffer = null;
  }
  
  static final Comparator<CharsRef> lengthComparator = new Comparator<CharsRef>() {
	    @Override
	    public int compare(CharsRef o1, CharsRef o2) {
	      int cmp = Integer.compare(o2.length, o1.length);
	      if (cmp == 0) {
	        // tie break on text
	        return o2.compareTo(o1);
	      } else {
	        return cmp;
	      }
	    }
	  };
  
  public List<CharsRef> getStemList(char word[], int length) {
	    List<CharsRef> stems = new ArrayList<CharsRef>();
	    //String w = new String(word, 0, length); 
		List<String> helper = null;
//		System.out.println("in: " + new String(word, 0, length));
		if (type == StemmerType.HUNSPELL)
			helper = hunspell.stem(new String(word, 0, length));
//		else if (type == StemmerType.OCASTEM)
//			helper = ocastem.stem(new String(word, 0, length));
		else if (type == StemmerType.HUMOR){
		
			int options = Humor._FILTER_STEM | Humor._CASE_SENSITIVE; //"alma"
			//int options = _FILTER_STEM | _SHOW_STEM_AND_POS; //"alma[FN]"
			//int options = _FILTER_STEM | _SHOW_STEM_FULL; //"alma[FN][NOM]"
			//int options = _FILTER_STEM_AND_POS | _SHOW_STEM_ONLY; //ment => megy, ment (bovebben a definicioknal)
			//int options = _FILTER_STEM | _SHOW_STEM_ONLY | _CASE_SENSITIVE; // case sensitive
//			System.out.println("in:" + new String(word, 0, length) + " obj:" + humor);
			String[] arr = humor.getStemEx(new String(word, 0, length), options);
			if (arr != null){
//				System.out.println("res:" + arr.length);
				helper = Arrays.asList(arr);
			}else
				helper = new ArrayList<String>();
//			System.out.flush();
			
		}

		//original word, as well!!! => KeywordRepeatFilter
		//helper.add(0, new String(word, 0, length));
	    //String[] helper = w.split("#");
//		System.out.println("out: " + helper);
		
		for (String h : helper)
	    	stems.add(new CharsRef(h));//h.toCharArray(), h.length()));
	    return stems;
  }

}
