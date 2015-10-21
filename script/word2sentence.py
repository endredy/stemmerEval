
# this class stores the sentence IDs of words
class word2sentence:

    def __init__(self):
        self.words = {}
        self.ids = {}
        self.stem2words = {} # for debug

    def addHit(self, word, stem, sID):
#        print('addHit: ' + word + ' ' + stem)
        if stem == '':
            stem = word
        i = self.words.get(word, '')
        if i == '':
            self.words[word] = [stem]
        elif stem not in i:
            i.append(stem)

#        self.ids.add(iID)
        o = self.ids.get(stem, None)
        if o == None:
            self.ids[stem]=set([sID]) # [sID]
        elif sID not in o:
            o.add(sID) # append(sID)

        # debug
        s = self.stem2words.get(stem, '')
        if s == '':
            self.stem2words[ stem ] = [word]
        elif word not in s:
            s.append(word)

    def getWords(self):
        return self.words

    def getWordsByStem(self, word):
        stems = self.words.get(word, [])
        r = ''
        for s in stems:
            r += ' ' + s + ' -> ' + str(self.stem2words.get(s, []))
        return r

    def getSentIDs(self, word):
        st = self.words.get(word, '')
        if (st == ''):
            return set()#[]
        r = set() #[]
        for i in st:
            #r = r + self.ids.get(i, [])
            r = r.union(self.ids.get(i, set())) # itt [] volt!
        return r

    def print(self):
        print('\nwords: ' + str(self.words))
        print('\nids: ' + str(self.ids))

    def getPaiceStems(self):
        return self.stem2words
