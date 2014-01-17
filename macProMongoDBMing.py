from ming import Session, create_datastore
from ming import Document, Field, schema

# bind = create_datastore('mongodb://114.34.79.27:27017/citeSeerDataSet')
bind = create_datastore('mongodb://localhost/citeSeerDataSet')
# bind = create_datastore('mongodb://140.118.175.200:27017/citeSeerDataSet')
session = Session(bind)

class paperItem(Document):
    """docstring for paperItem"""
    class __mongometa__:
        session = session
        name = 'citeSeerx_copy'
    #name = 'citeSeerx'
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
    papers = paperItem.m.find().all()
    for paper in papers:
        for ref in paper['ref']:
            print ref
            # for citePaper in papers:
            #     if citePaper['_id'] == ref:
            #         citePaper['cite'].append(ref)
            citePaper = paperItem.m.find({"_id":ref}).first()
            if citePaper is None:
                print "no this paper"
            else:
                citePaper['cite'].append(ref)
                print citePaper['cite']