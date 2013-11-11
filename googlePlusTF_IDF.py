# Explore some of NLTK's functionality by exploring the data. 
# Here are some suggestions for an interactive interpreter session.

import nltk
nltk.download('stopwords')
class ntlk_tf_idf:
    """docstring for ntlk_tf_idf"""
    def __init__(self):
        self.rf_List = []
        self.all_content = ""

    def searchForTitleTFIDF (self, data):
        self.all_content = data
        tokens = self.all_content.split()
        text = nltk.Text(tokens)
        text.collocations()
        fdist = text.vocab()
        for rank, word in enumerate(fdist):
            dist = {"rank": rank, "word": word, "count": fdist[word]}
            #print rank, word, fdist[word]
            self.rf_List.append(dist)
        return self.rf_List;

    def tf(self, data):
        
        print data

    def idf(self, data):
        print data

    def computeTFIDf(self, data):
        print data  
if __name__ == '__main__':
    nltkTFIDF = ntlk_tf_idf()
    #testGraph.search_title("text")
    textSearch = 'Adapting to Network and Client Variation Using Active Proxies, Sony magiclink pda., et al. TranSend web accelerator proxy. Free service deployed by UC'
    print nltkTFIDF.searchForTitleTFIDF(textSearch)

# # Download ancillary nltk packages if not already installed
# nltk.download('stopwords')
# # for a in activity_results:
# #     print a['object']['content']

# #all_content = " ".join([ a['object']['content'] for a in activity_results ])

# # Approximate bytes of text
# #print len(all_content)
# all_content = ''' Mr. Green killed Colonel Mustard in the study with the " + \
#            "candlestick. Mr. Green is not a very nice fellow. '''
# tokens = all_content.split()
# text = nltk.Text(tokens)

# # Examples of the appearance of the word "open"
# #text.concordance("open")

# # Frequent collocations in the text (usually meaningful phrases)
# text.collocations()

# # Frequency analysis for words of interest
# fdist = text.vocab()
# # fdist["open"]
# # fdist["source"]
# # fdist["web"]
# # fdist["2.0"]

# # Number of words in the text
# #print len(tokens)

# # Number of unique words in the text

# #print len(fdist.keys())

# # Common words that aren't stopwords
# #
# # Number of URLs
# #print len([w for w in fdist.keys() if w.startswith("http")])

# # Enumerate the frequency distribution
# for rank, word in enumerate(fdist): 
#     print rank, word, fdist[word]