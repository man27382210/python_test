from ming import Session, create_datastore
from ming import Document, Field, schema

bind = create_datastore('paperMiningTest')
session = Session(bind)

class Paper(Document):

    class __mongometa__:
        session = session
        name = 'paper'

    _id = Field(str) #10.x.x...
    title = Field(str) #paper title
    abstart = Field(str) #paper abstart
    url = Field(str) #paper url
    defpaper = Field([str]) #put ref paper id
    citebypaper = Field([str]) #put cite paper id


class InvertedIndex(Document):
    class __mongodmeta__:
        session = session
        name = 'InvertedIndex'
    _id = Field(schema.ObjectId)
    term = Field(str) #the term
    docs = Field([dict(id=str, tf=int)])