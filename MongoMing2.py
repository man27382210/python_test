from ming import Session, create_datastore
from ming import Document, Field, schema

bind = create_datastore('mongodb://114.34.79.27:27017/paperMiningTest')
session = Session(bind)

class Paper(Document):

    class __mongometa__:
        session = session
        name = 'paperWithAbs'

    # _id = Field(str) #10.x.x...
    title = Field(str) #paper title
    abstart = Field(str) #paper abstart
    url = Field(str) #paper url
    defpaper = Field([dict(title=str, url=str)])
    citebypaper = Field([dict(title=str, url=str)]) #put cite paper id


class InvertedIndex(Document):
    class __mongodmeta__:
        session = session
        name = 'InvertedIndex'
    _id = Field(schema.ObjectId)
    term = Field(str) #the term
    docs = Field([dict(id=str, tf=int)]) #doc id and tf in the document