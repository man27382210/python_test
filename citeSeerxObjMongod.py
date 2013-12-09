from BeautifulSoup import BeautifulSoup, NavigableString
import urllib2
import sys
import re, string
from paperMiningSchema import Paper


'''
    _id = Field(str) #10.x.x...
    title = Field(str) #paper title
    abstart = Field(str) #paper abstart
    url = Field(str) #paper url
    defpaper = Field([str]) #put ref paper id
    citebypaper = Field([str]) #put cite paper id

'''
def fullUrl(url):
    return "http://citeseerx.ist.psu.edu"+url

def rePunctuation(title):
        out = re.sub('[%s]' % re.escape(string.punctuation), "", title)
        return out

def parsePaper(urlUse, level):
    soup = BeautifulSoup(urllib2.urlopen(fullUrl(urlUse)))
    node = Paper()
    node.defpaper = []
    try:
        node.title = rePunctuation(soup.find('div', {"id":"viewHeader"}).find('h2').text)
        node.url = urlUse
        print "title :%s" % node.title
        print "url :%s" % node.url
        print "level :%s" % level
        if level < 3:
            try:
                refList = soup.find("div",{"id":"citations"})
                refListUse = refList.findAll("tr")
                for ref in refListUse:
                    refDict = {"title":rePunctuation(ref.find("a").text), "url":ref.find("a")['href']}
                    if refDict["title"].find("et al") == -1:
                        node.defpaper.append(refDict)
                    else:
                        print "have et al"
            except Exception, e:
                print ('no ref')
            node.m.save()
        for refDictUse in node.defpaper:
            parsePaper(refDictUse['url'], level+1)
    except Exception, e:
        print "error"
        pass


if __name__ == '__main__':
    url = "/viewdoc/summary;jsessionid=9AB39FDEB4EEB5114CB04EDBC01C940C?doi=10.1.1.163.5292"
    parsePaper(url, 0)
        