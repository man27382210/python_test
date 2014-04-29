import json, re, string
from ming import Session, create_datastore
from ming import Document, Field, schema

bind = create_datastore('mongodb://140.118.175.200:27017/citeSeerDataSet')
# bind = create_datastore('mongodb://localhost/citeSeerDataSet')
session = Session(bind)

def rePunctuation(title):
    out = re.sub('[%s]' % re.escape(string.punctuation), "", title)
    out = ''.join(i for i in out if not i.isdigit())
    return out.lower()

class paperItem(Document):
    """docstring for paperItem"""
    class __mongometa__:
        session = session
        name = 'citeSeerx_copy'
    paperTitle = Field(str)
    authors = Field(str)
    year = Field(str)
    conf = Field(str)
    citationNumber = Field(str)
    _id = Field(str)
    arnetid = Field(str)
    ref = Field([])
    cite = Field([])
    abs = Field(str)



if __name__ == '__main__':
    dict = {}
    paperFirst = paperItem.m.find({"_id":"87696"}).first()
    arrayCiteFirst = []
    arrayCiteSec = []
    arrayCiteThi = []

    arrayRefFirst =[]
    arrayRefSec = []
    arrayRefThi = [] 

    for cite in paperFirst['cite']:
        print "cite : %s" % cite
        pa = paperItem.m.find({"_id":cite}).first()
        arrayCiteFirst.extend(pa['cite'])
    # for ref in paperFirst['ref']:
    #     print "ref : %s" % ref
    #     pa = paperItem.m.find({"_id":ref}).first()
    #     print pa['ref']
    #     arrayRefFirst.append(pa['ref'])
    # # print arrayCiteFirst
    # print arrayRefFirst

    # for citeFirstPaper in arrayCiteFirst:
    #     arrayCiteSec.extend(paperItem.m.find({"_id":citeFirstPaper["_id"]}).first()['cite'])
    # for refFirstPaper in arrayRefFirst:
    #     arrayRefSec.extend(paperItem.m.find({"_id":refFirstPaper["_id"]}).first()['ref'])
