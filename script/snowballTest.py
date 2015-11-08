import sys
from nltk.stem import *
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer(sys.argv[1])
'''  "danish", "dutch", "english", "finnish", "french", "german",
     "hungarian", "italian", "norwegian", "porter", "portuguese",
     "romanian", "russian", "spanish", "swedish""hungarian"
'''

f = open(sys.argv[2],'r')

for line in f:
    line = line.strip()
    sys.stdout.write(line + "\n")
    sys.stdout.write("\t" + stemmer.stem(line) + "\n")

f.close()