from ming import Session, create_datastore
from ming import Document, Field, schema

bind = create_datastore('tutorial')
session = Session(bind)

class WikiPage(Document):

    class __mongometa__:
        session = session
        name = 'wiki_page'

    _id = Field(schema.ObjectId)
    title = Field(str)
    text = Field(str)