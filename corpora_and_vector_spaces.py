import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, models, similarities

# documents = ["Human machine interface for lab abc computer applications",
#             "A survey of user opinion of computer system response time",
#             "The EPS user interface management system",
#             "System and human system engineering testing of EPS",
#             "Relation of user perceived response time to error measurement",
#             "The generation of random binary unordered trees",
#             "The intersection graph of paths in trees",
#             "Graph minors IV Widths of trees and well quasi ordering",
#             "Graph minors A survey"]

documents = ["The Neatest Little Guide to Stock Market Investing",
            "Investing For Dummies, 4th Edition",
            "The Little Book of Common Sense Investing: The Only Way to Guarantee Your Fair Share of Stock Market Returns"
            "The Little Book of Value Investing",
            "Value Investing: From Graham to Buffett and Beyond",
            "Rich Dad's Guide to Investing: What the Rich Invest in, That the Poor and the Middle Class Do Not!",
            "Investing in Real Estate, 5th Edition",
            "Stock Investing For Dummies",
            "Rich Dad's Advisors: The ABC's of Real Estate Investing: The Secrets of Finding Hidden Profits Most Investors Miss"]

stoplist = set('and edition for in little of the to'.split())
texts = [[word for word in document.lower().split() if word not in stoplist]
        for document in documents]

all_tokens = sum(texts, [])

tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word)==1)
texts = [[word for word in text if word not in tokens_once]
        for text in texts]

print "texts :%s" %texts

dictionary = corpora.Dictionary(texts)

dictionary.save('/tmp/deerwester.dict') # store the dictionary, for future reference
print "dictionary : %s" % dictionary
print "dictionary token : %s" % dictionary.token2id

#new_doc = "Human computer interaction" [(0, 1), (1, 1)] <- interaction not in dic
new_doc = "Human computer system" #[(0, 1), (1, 1), (5, 1)]
new_vec = dictionary.doc2bow(new_doc.lower().split())
print "new_vec : %s" %new_vec # the word "interaction" does not appear in the dictionary and is ignored
corpus = [dictionary.doc2bow(text) for text in texts]

corpora.MmCorpus.serialize('/tmp/deerwester.mm', corpus) # store to disk, for later use
print "corpus : %s" %corpus

#---------------------------------------------------------------------

tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model
doc_bow = new_vec
print "tfidf : %s " % tfidf[doc_bow]
corpus_tfidf = tfidf[corpus]
for doc in corpus_tfidf:
    print "doc : %s" %doc
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2) # initialize an LSI transformation
corpus_lsi = lsi[corpus_tfidf] # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi
print ""
lsi.print_topics(2)
for doc in corpus_lsi:
    print "doc : %s" % doc
lsi.save('/tmp/model.lsi') # same for tfidf, Lda, ....
lsi = models.LsiModel.load('/tmp/model.lsi')

