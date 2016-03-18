#!/bin/env/python3
# coding: utf-8

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
        self.obj list of object-Konj-object and object modifiers in the sentence 
        
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
        try:
            self.sentence = open(parsedSentence).read()
            self.sentence_parts = self.sentence.split("\n")
            self.word_parts = [part.split("\t") for part in self.sentence_parts]
            self.word_parts.pop()
        
        except IOError:
            raise IOError("file does not exist in specified folder")
    
    def check_SB_Verb(self):
        """checks if number of verbs is equal to number of subjects"""
        for word in self.word_parts:
            
            if word[4] == "VVFIN":
                self.verb.append(self.word_parts.index(word))
            
            elif word[7] == "SB":
                # checks modifiers
                self.sb.append(self.checkAttributes(self.word_parts.index(word)))
            
        return len(self.verb) <= len(self.sb)
    
    def checkOB(self):
        """checks if objects are directly connected"""
        for word in self.word_parts:
            
            if word[7] == "OA" or word[7] == "DA":
                obj = self.word_parts.index(word)
                
                if self.word_parts[obj+1][4] == "KON":
                    
                    self.obj.extend(self.checkfurtherObj(obj))
    

            
    
    def checkfurtherObj(self, obj):
        n = obj+2
        nextObj = [obj, obj+1]
        while self.word_parts[n][7] == "NK":
            modifierObj.append(n)
            n += 1
        
        if self.word_parts[n][7] == self.word_parts[obj][7]:
            nextObj.append(n)
        
        return nextObj
            
    
    
    def checkAttributes(self, index):
        """adds modifiers to subject list"""
        sb = []
        oIndex = index
        while True:
            if self.word_parts[index-1][7] == "NK" or self.word_parts[index-1][7] == "PNC":
                sb.append(index-1)
                index -= 1
            else:
                break
        sb.append(oIndex)
        return sb
            
            

    def getSentence(self):
        """returns normalized sentence"""
        self.checkOB()
        if self.check_SB_Verb():
        
            if self.obj != []:
                self.insertObject()
            
            self.checkPron()
            return self.orderSentence()
        
        self.checkPron()
        
        if len(self.sb) != 0:
            self.insertSubject()
       
        self.checkOB()
        
        if self.obj != []:
            self.insertObject()
            
        return self.orderSentence()

    
    def checkPron(self):
        """ replaces pronomina in the sentence"""
        subjects = list(self.sb)
        while subjects != []:
          
            if self.word_parts[subjects[-1][-1]][4] == "PPER":
                pron = subjects[-1][-1]
                sb = subjects[-2]
                sentence_new = self.sentence_parts[:pron]
                for s in sb:
                    sentence_new.append(self.sentence_parts[s])
                sentence_new.extend(self.sentence_parts[pron+1:])
                self.sentence_parts = sentence_new
          
            subjects.pop()
            
            
    def insertSubject(self):
        """ inserts subject before verb"""
        verbNumber = 1
        while self.sb != []:
          
            if self.word_parts[self.verb[-verbNumber]][7] != "SB":
                new_sentence_parts = self.sentence_parts[:self.verb[-1]]
                for s in self.sb[-1]:
                    new_sentence_parts.append(self.sentence_parts[s])
                new_sentence_parts.extend(self.sentence_parts[self.verb[-1]:])
                self.sentence_parts = new_sentence_parts
            verbNumber +=1
          
            if verbNumber > len(self.verb):
                break
          
            self.sb.pop()
            


    def insertObject(self):
        """insert first half of the sentence in front of second obj"""
        # TODO: more than just one object
        new_sentence_parts = self.sentence_parts[:self.obj[-1]]
        # first object at self.ob[0]
        new_sentence_parts.extend(self.sentence_parts[:self.obj[0]-1])
        new_sentence_parts.extend(self.sentence_parts[self.obj[-1]:])
        self.sentence_parts = new_sentence_parts
        
        
    def orderSentence(self):
        """ fixes line numbers"""
        import re
        number_of_lines = len(self.sentence_parts)
        sentence = ""
        for i in range(1,number_of_lines):
            line = re.sub("\S*\t", str(i) + "\t", self.sentence_parts[i-1], 1)
            sentence += line +"\n"
        return sentence
        
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
