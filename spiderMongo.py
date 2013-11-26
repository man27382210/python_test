from pymongo import Connection
import googlePlusTF_IDF
nltkTFIDF = googlePlusTF_IDF.ntlk_tf_idf()
class mongoTest:
    def __init__(self):
        con = Connection()
        db = con.test
        shows = db.show
        shows = shows.find()
        show = shows[0]
        self.showRef = show["defpaper"]
        self.refs = {}

    def mix(self):
        for x in xrange(0,len(self.showRef)):
            i = str(x)
            array = self.showRef[i]
            for ref in array:
                if i in self.refs:
                    arrayUse = self.refs[i]
                    arrayUse.append(ref['title'])
                    self.refs[i]=arrayUse
                else:
                    self.refs[i] = []
                    self.refs[i].append(ref['title'])
        return self.refs

if __name__ == '__main__':
      mongoTs = mongoTest()
      print mongoTs.mix()
# for x in xrange(0,len(refs)):
#     levelUse = refs[str(x)]
#     print "nltk:%s" %nltkTFIDF.computeTFIDf(nltkTFIDF.idf(levelUse, nltkTFIDF.tf(levelUse)))
#     print
