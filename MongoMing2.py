from ming import Session, create_datastore
from ming import Document, Field, schema

# bind = create_datastore('mongodb://114.34.79.27:27017/paperMiningTest')
bind = create_datastore('mongodb://localhost/paperMiningTest')
session = Session(bind)

class Paper(Document):

    class __mongometa__:
        session = session
        name = 'paperVGI'
        # name = 'paperYearOp'

    # _id = Field(str) #10.x.x...
    title = Field(str) #paper title
    abstart = Field(str) #paper abstart
    url = Field(str) #paper url
    # paperid = Field(str) #10.x.x...
    year = Field(str) #20xx
    # defpaper = Field([dict(title=str, url=str)])
    # citebypaper = Field([dict(title=str, url=str)]) #put cite paper id


class InvertedIndex(Document):
    class __mongodmeta__:
        session = session
        name = 'InvertedIndex'
    _id = Field(schema.ObjectId)
    term = Field(str) #the term
    docs = Field([dict(id=str, tf=int)]) #doc id and tf in the document

if __name__ == '__main__':
    print len(Paper.m.find().all())