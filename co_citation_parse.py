from ming import Session, create_datastore
from ming import Document, Field, schema
import json
import urllib2

bind = create_datastore('mongodb://localhost/paperMiningTest')
session = Session(bind)

class Paper(Document):

    class __mongometa__:
        session = session
        name = 'paperCoCitation'

    id = Field(str) 
    cocitation = Field([]) #put cite paper id

if __name__ == '__main__':
    baseUrl = "http://140.118.175.209/paper/cocitation.php?ids="
    with open('paperId.json') as data_file:
        data = json.load(data_file)
    for paperId in data["CitationId"]:
        url = baseUrl + str(paperId)
        cocitationRelationDic = json.load(urllib2.urlopen(url))[0]
        if len(cocitationRelationDic) is not 0:
            paperRel = Paper(dict(id = cocitationRelationDic["id"],cocitation = cocitationRelationDic["co_citation"]))
            paperRel.m.save()
            print paperRel
        else:
            print "No cocitation"
    