These scripts create gold standard for IR evaluation: 
 -each sentence of the corpus is put in a separate file, its filename is its sentence ID (in more subdirectories, linux does not like more thousand files in a single dir)
 -gold standard sentence sets are counted for each word of the corpus. 
    Its format: <word form, as it is> <list of sentence IDs which has this word in any forms>
   