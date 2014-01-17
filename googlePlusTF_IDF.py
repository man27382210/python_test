# Explore some of NLTK's functionality by exploring the data. 
# Here are some suggestions for an interactive interpreter session.

import nltk
from math import log
from nltk.corpus import wordnet
from nltk.corpus import stopwords
nltk.download('stopwords')
import json

class ntlk_tf_idf:
    """docstring for ntlk_tf_idf"""
    def __init__(self):
        self.rf_List = []
        self.all_content = ""
        self.UnwantList = []

    def searchForTitleTFIDF (self, data):
        self.all_content = data
        tokens = self.all_content.split()
        print tokens
        text = nltk.Text(tokens)
        text.collocations()
        fdist = text.vocab()
        for rank, word in enumerate(fdist):
            dist = {"rank": rank, "word": word, "count": fdist[word]}
            self.rf_List.append(dist)
        return self.rf_List;

    def extractTitleLemma(self, title):
        title = title.split(" ")
        for text in title:
            syns = wordnet.synsets(text)
            # print "syns: %s" %syns 
            array = [l.name for s in syns for l in s.lemmas]
            # print "array first: %s" %array 
            array = [word for word in array if word not in self.UnwantList]
            # print "array: %s" %array
            self.UnwantList.extend(array)
        print "UnwantList:%s"% self.UnwantList

    def removeWord(self, textArray):
        textArray = [ word for word in textArray if word not in stopwords.words("english")]
        textArray = [ word for word in textArray if word not in self.UnwantList]
        return textArray

    def tf(self, level):
        tfResult = []
        docConpute = ""
        for doc in level:
            docConpute = docConpute + doc + " "
        docConpute = docConpute.lower().split()
        docConpute = self.removeWord(docConpute)
        print docConpute
        text = nltk.Text(docConpute)
        text.collocations()
        fdist = text.vocab()
        for rank, word in enumerate(fdist):
            dist = {"rank": rank, "word": word, "tf": fdist[word]}
            tfResult.append(dist)
        return tfResult


    def idf(self, level, resultArray):
        num_tests_with_term = 0
        for doc in resultArray:
            num_tests_with_term = len([True for text in level if doc['word'] in text.lower().split()])
            doc['df']=num_tests_with_term
            try:
                doc['idf'] = 1.0 + log(float(len(level))/doc['df'])
            except ZeroDivisionError:
                doc['idf'] = 1.0
        return resultArray

    def computeTFIDf(self, resultArray):
        for doc in resultArray:
            doc['tfidf'] = doc['tf'] * doc['idf']
        return resultArray


if __name__ == '__main__':
    nltkTFIDF = ntlk_tf_idf()
   #  levelDict = { '1':
   # [ 'Spatio-temporal frequency analysis for removing rain and snow from videos',
   #   'A Multi-Layered Display with Water Drops' ],
   #  '2':
   # [ 'Detection and removal of rain from videos',
   #   'When does a camera see rain',
   #   'Why is Snow So Bright',
   #   'RAIN REMOVAL IN VIDEO BY COMBINING TEMPORAL AND CHROMATIC PROPERTIES',
   #   'A projector-camera system for creating a display with water drops',
   #   'An Immaterial Depth-Fused 3D Display' ] }
    json_data=open('data2.json')
    levelDict = json.load(json_data)
    json_data.close()
    for x in xrange(1,len(levelDict)+1):
        levelUse = levelDict[str(x)]
        print nltkTFIDF.computeTFIDf(nltkTFIDF.idf(levelUse, nltkTFIDF.tf(levelUse)))
        print        