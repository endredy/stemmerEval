import re


def getStem(s):
    if (s == '+?' or s == 'unknown word'):
        return None # unknown
    i=s.find('+')
    if (i == -1):
        return s
    return s[0:i]


class StemReaderOcastem:

    def __init__(self, filename):
        self.f = open(filename, 'r')

    def reset(self):
        self.f.seek(0)

    def getNextWordAndStems(self):

        stems = []
        line = self.f.readline()
        if not line:
            return (None, [])
        p = line.strip().split('\t')
        return (p[0], p[1:])

class StemReaderFoma:

    def __init__(self, filename):
        self.f = open(filename, 'r')

    def reset(self):
        self.f.seek(0)

    def getNextWordAndStems(self):

        stems = []
        line = self.f.readline()
#        print(line)
        while line and len(line.strip()) != 0:
            s=getStem(line)
            if s is None or len(s) > 0:
                stems.append(s)
            line = self.f.readline()

        if len(line) == 0:
            return(None, stems) # end of file
        return ('', stems)

    def getWord(self, s):
        t=s.split('\t')
        return t[0]

class StemReaderOcamorf:

    def __init__(self, filename):
        self.f = open(filename, 'r')
        self.nextWord = ''

    def reset(self):
        self.f.seek(0)
        self.nextWord = ''

    # el/PREV+megy/VERB<PAST><PERS<1>><PLUR>
    # m.lik/VERB[PERF_PART]/ADJ
    def getStem(self, s):
        r=''
        skip=0
        if (s == 'UNKNOWN'):
            return None # unknown
        for ch in s:
            if (ch == '/'):
                skip=1
            if (skip == 0):
                r += ch
            if (ch == '+'):
                skip=0

        return r

    def getNextWordAndStems(self):

        stems = []
        word = ''
        if self.nextWord != '':
            word = self.nextWord
        line = self.f.readline()
        while line and len(line) != 0:
            if (line.startswith('> ')):
                #new word
                if self.nextWord == '':
                    word = line.strip(' >\n')
                    self.nextWord = line # avoid this condition next time
                    line = self.f.readline()
                    continue
                else:
                    self.nextWord = line.strip(' >\n')
                    return (word, stems)

            s=self.getStem(line.strip())
            if s is None or len(s) > 0:
                stems.append(s)
            line = self.f.readline()

        return (None, stems)


class StemReader:

    def __init__(self, filename, nostem):
        self.currWord = ''
        self.currStems = []
        self.nextWord = ''
        self.f = open(filename, 'r')
        self.debug = 0
        self.first = 1
        self.currSent = []
        self.nostem = nostem

    def reset(self):
        self.f.seek(0)
        self.currWord = ''
        self.nextWord = ''
        self.first = 1

    def getNextLine(self, t):

        line = self.f.readline()
        reg = '^\S' # line start with letters (new word)
        if t == 'not empty':
            reg = '\S'
        if t == 'stemline':
            reg = '^\s'
        while (line and re.search(reg, line) == None):
            line = self.f.readline()
        return line

    def getNextWordAndStems(self):
        # vagy a fajl elejere mutat, vagy egy input szo utanra
        self.currStems = []
        if (self.first == 1):
            # elso szo
            self.currWord = self.getNextLine('')
            self.first = 0
#            self.currWord = line#.strip()
        else:
            self.currWord = self.nextWord # folytatjuk
        self.currWord = self.currWord.strip()
        line = self.currWord

        while(line):
#            print(line + self.currWord)

            # no stem:.
            if self.nostem:
                # no stem: we dont need stem, so skip them, and then return
                self.nextWord = self.getNextLine('')
                return (self.currWord, [self.currWord])

            line = self.getNextLine('not empty')
            if (re.match('\S', line) != None):
                # new word:
                self.nextWord = line.strip().lower()
                return (self.currWord, self.currStems)

            # beljebb van: stem

            s = getStem(line.strip())

            if s is None:
                self.currStems.append(s)
            if (s is None or s == ''):
                continue
            s = s.lower() # legyen kisbetus
            if len(s) > 0:
                self.currStems.append(s)

        return (None, [])




