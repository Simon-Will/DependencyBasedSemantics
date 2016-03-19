#!/usr/bin/env python3
# -*- coding: utf-8 -*-



class Normalizer:
    """Reads a parsed sentence out of a file and normalizes its structure
    A Normalizer object consists of a parsed sentence
    Each sentence is brought into a SB VB O (CONJ SB VB O form.
    
    Attributes:
        sentence: sentence read out of file
        sentence_parts  : list of lines of splitted sentence
        self.word_parts: list of attributes of one sentence_part
        self.verb : list of verbs in the sentence
        self.sb : list of subjects and subject modifiers in the sentence
        self.obj: list of object-Konj-object and object 
            modifiers in the sentence 
        self.pr : list of pron in sentence
    """
    
    def __init__(self, parsedSentence):
        """Initializes Normalzer with given values.
        parsedSentence has to be a file in wihich a sentence previously 
        parsed and in  conll format is written
        Args:
            parsedSentence: a list containing all words in the file
        Returns:
            the initialized Normalzer object
        Raises:
            IOError
        
        """
        self.obj = []
        self.verb = []
        self.sb = []
        self.pr = []
        
        try:
            self.sentence = open(parsedSentence).read()
            self.word_parts = [part.split("\t") for part in 
                                self.sentence.split("\n")][:-1]
            self.word_parts.pop()
         
        except IOError:
            raise IOError("Could not find file")
            
    def check_SB_Verb(self):
        """checks if number of verbs is equal to number of subjects"""
        for word in self.word_parts:
            
            if word[4] == "VVFIN":
                self.verb.append(self.word_parts.index(word))
            
            elif word[7] == "SB" and word[4] != "PPER":
                # checks modifiers
                self.sb.append(self.checkAttributes(
                                    self.word_parts.index(word))
                                    )
            
            elif word[4] == "PPER":
                self.pr.append(int(word[0]))
                
            
        return len(self.verb) <= len(self.sb)
        
        
    def checkAttributes(self, index):
        """adds modifiers to subject list"""
        sb = []
        oIndex = index
        while index > 0:
            if (self.word_parts[index-1][7] == "NK" or 
                self.word_parts[index-1][7] == "PNC"):
                sb.append(index-1)
                index -= 1
            else:
                break
        sb.append(oIndex)
        return sb
        

    def checkOB(self):
        """checks if objects are directly connected"""
        for word in self.word_parts:
            
            if word[7] == "OA" or word[7] == "DA" or word[7] == "OA2":
                obj = self.word_parts.index(word)
                
                try:
                    if self.word_parts[obj+1][4] == "KON":
                        self.obj.append(self.checkfurtherObj(obj))
                    
                except IndexError:
                    continue

    def checkfurtherObj(self, obj):
        """find coordinated object"""
        n = obj+2
        nextObj = []
        nextObj.extend(self.checkAttributes(obj))
        nextObj.extend([obj, obj+1])
        while self.word_parts[n][7] == "NK":
            nextObj.append(n)
            n += 1
        
        if (self.word_parts[n][7] == self.word_parts[obj][7] or
            self.word_parts[n][7] == "OA2"):
            nextObj.append(n)
        
        return nextObj
        
    
    
    def checkPron(self):
        """ replaces pronomina in the sentence"""
        pkonj = []
        for pron in self.pr:
            pkonj.append(pron-1)
            self.word_parts, words = self.word_parts[:pron-1], \
                                        self.word_parts[pron:]
            for i in range(pron,0,-1):
                subj = [sub for sub in self.sb if i in sub]
            self.word_parts.extend(self.addWords(subj))
            self.word_parts.extend(words)
            del subj[:]
        self.word_parts = self.mergenewSentence(self.word_parts)
        self.assignNodes(pkonj)
            
        
        
    def addWords(self, words):
        """ add words to be inserted"""
        appendedWords = []
        for word in words:
            for w in word:
                appendedWords.append(self.word_parts[w])
        return appendedWords
    
    def insertSubject(self):
        """inserts subject before verb"""
        vkonj = []
        for verb in self.verb:
            if self.word_parts[verb-1][7] != "SB":
                vkonj.append(verb)
                word_parts, words = self.word_parts[:verb], self.word_parts[verb:]
                subj = [su for su in self.sb for i in range(verb,0,-1) 
                            if i in su]
                word_parts.extend(self.addWords(subj))
                word_parts.extend(words)
                self.word_parts = word_parts
        self.word_parts = self.mergenewSentence(self.word_parts)
        self.assignNodes(vkonj)
        
    def insertObject(self):
        """insert first half of the sentence in front of second obj"""
        konj = []
        for obj in self.obj:
            konj.extend([kon for kon in obj 
                        if self.word_parts[kon][4] == "KON"])
            for konjunction in konj:
                word_parts, words = self.word_parts[:konjunction], \
                                    self.word_parts[konjunction+1:]
                word_parts.append(self.word_parts[konjunction])
                word_parts.extend(self.word_parts[:obj[0]])
                word_parts.extend(words)
        self.word_parts = self.mergenewSentence(word_parts)
        self.assignNodes(konj)
            
    def assignNodes(self, konj):
        """assign correct dependencies"""
        relations = {"SB" : [], "VVFIN" : [], "NN" : [], "OA" : [], 
                    "OA2" : [], "DA" : [], "MO": []}
        relations = self.assignRelations(self.word_parts, relations)
        for word in self.word_parts:
            if(self.checkNoun(word) or word[7] == "MO"):
                word = self.assignVerb(word, relations, konj)
            elif(word[7] == "NK"):
                word = self.assignNK(word, relations, konj)
            
        
    def checkNoun(self, word):
        return word[4] == "NN" and word[7] != "NK"
        
        
    def assignVerb(self, word, relations, konj):
        """assign verb dependency"""
        for n in relations["VVFIN"]:
            for konjunction in konj:
                if (int(word[0]) > konjunction and n > konjunction):
                    self.changeWord(word, n)
        return word
            
    
    def assignNK(self, word, relations, konj):
        """nomina and mo dependency"""
        for n in relations["NN"]:
            for konjunction in konj:
                if (int(word[0]) < konjunction and n < konjunction):
                    if(int(word[0]) > n and word[3] == "DET"):
                        continue
                    n =  self.checkMo(int(word[0]), n, relations["MO"])
                    self.changeWord(word, n)
                    return word
                    
                    
                elif (int(word[0]) > konjunction and n > konjunction):
                    if(int(word[0]) > n and word[3] == "DET"):
                        continue
                    n =  self.checkMo(int(word[0]), n, relations["MO"])
                    self.changeWord(word, n)
                    self.changeWord(word, n)
                    return word
        return word
            
            
    def checkMo(self, word, n, relations_mo):
        """checks for nomen-nk relation"""
        for mo in relations_mo:
            if (self.getDistance(mo, word) < self.getDistance(n, word)):
                #print(word[0], self.getDistance(n, int(word[0])), int(word[0])-mo)
                return mo
        return n
        
    def getDistance(self, n, m):
        if n > m:
            return n-m
        else:
            return m-n
        
    def assignRelations(self, words, relations):
        """selects correct dependency"""
        for key in relations.keys():
            values = []
            if key == "VVFIN" or key == "NN":
                values.extend([int(word[0]) for word in words 
                                if word[4] == key])
            else:
                values.extend([int(word[0]) for word in words 
                                if word[7] == key])
            relations[key] = values
        return relations         
    
    def changeWord(self, word, n):
        """cahnge dependency"""
        word[6] = str(n)
        return word
    
    def orderSentence(self):
        """ fixes line numbers"""
        sentence_p = []
        for word in self.word_parts:
            sentence_p.append(("\t").join(word))
        sentence = ""
        for line in sentence_p:
            sentence += line + "\n"
        return sentence
    
    def mergenewSentence(self, words):
        """combines sentence"""
        import re
        sentence_part = []
        sentence = ""
        for word in words:
            sentence_part.append(("\t").join(word))
        
        number_of_lines = len(sentence_part)
        for i in range(1,number_of_lines+1):
            line = re.sub("\S*\t",  str(i) + "\t", sentence_part[i-1], 1)
            sentence += line +"\n" 
        return [part.split("\t") for part in sentence.split("\n")][:-1]
    
        
        
        
            
    def getSentence(self):
        """returns normalized sentence"""
        self.checkOB()
        if self.check_SB_Verb():
        
            if self.obj != []:
                self.insertObject()
        
            self.checkPron()
            return self.orderSentence()
        
        
        if len(self.sb) != 0:
            self.insertSubject()
        
        
        self.checkPron()
        
        
        if self.obj != []:
            self.insertObject()
    
    #    self.assignNodes()
            
        return self.orderSentence()
     
     
     
     
     
     
     
     
def test():
    gurken = Normalizer("../test/conll/tanzende_gurken.conll")
    return gurken.getSentence() 

def testPronomina():
    gurken2 = Normalizer("../test/conll/tanzende_gurken2.conll")
    return gurken2.getSentence()
    
def testObj():
    hase = Normalizer("../test/conll/schenkender_hasen.conll")
    return hase.getSentence()
   
if __name__ == '__main__':
    print(test())
    print(testPronomina())
    print(testObj())

