from BeautifulSoup import BeautifulSoup, NavigableString
import urllib2
import sys
import re, string
# from paperMiningSchema import Paper
from MongoMing2 import Paper

def fullUrl(url):
    return "http://citeseerx.ist.psu.edu"+url

def rePunctuation(title):
        out = re.sub('[%s]' % re.escape(string.punctuation), "", title)
        out = ''.join(i for i in out if not i.isdigit())
        return out.lower()

def yearFromTitle(title):
    try:
        m = re.search(r"\(([A-Za-z0-9_]+)\)", title)
        return m.group(1)
    except Exception, e:
        return '0'

def parsePaperList(urlUse):
    soup = BeautifulSoup(urllib2.urlopen(fullUrl(urlUse)))
    papersSearch = soup.find("div",{"id":"result_list"})
    papersSearch = papersSearch.findAll("div",{"class":"result"})
    for cite in papersSearch:
        url = cite.find("a",{"class":"remove doc_details"})['href']
        parsePaperDetial(url)
    try:
        citation_url_next = soup.find('div',{"id":"pager"}).find('a')['href']
        if citation_url_next:
            # citation_url_next = fullUrl(citation_url_next)
            parsePaperList(citation_url_next)
    except Exception, e:
            print ("exception push in")


def parsePaperDetial(urlPaper):
    soup = BeautifulSoup(urllib2.urlopen(fullUrl(urlPaper)))
    node = Paper()
    try:
        titleAndYear = soup.find('div', {"id":"viewHeader"}).find('h2').text
        node.title = rePunctuation(titleAndYear)
        node.url = urlPaper
        node.abstart = soup.find('div', {"id":"abstract"}).find('p').text
        node.year = yearFromTitle(titleAndYear)
        print node.year
        # if(node.year != 0):
        #     node.m.save()
        # else:
        #     print "no year, don't save"
        print node
        node.m.save()
    except Exception, e:
        print (e)
        node.abstart = " "
        pass
    # print papersSearch
    # try:
    #     raise
    # except Exception, e:
    #     raise
    # node = Paper()
    # node.defpaper = []
    # node.citebypaper = []
    # try:
    #     node.title = rePunctuation(soup.find('div', {"id":"viewHeader"}).find('h2').text)
    #     node.url = urlUse
    #     node.abstart = soup.find('div', {"id":"abstract"}).find('p').text
    #     print "title :%s" % node.title
    #     print "url :%s" % node.url
    #     print "level :%s" % level
    #     print "abs: %s" % node.abstart
    #     if level < 3:
    #         try:
    #             refList = soup.find("div",{"id":"citations"})
    #             refListUse = refList.findAll("tr")
    #             for ref in refListUse:
    #                 refDict = {"title":rePunctuation(ref.find("a").text), "url":ref.find("a")['href']}
    #                 if refDict["title"].find("et al") == -1:
    #                     node.defpaper.append(refDict)
    #                 else:
    #                     print "have et al"
    #         except Exception, e:
    #             print ('no ref')
    #         # try:
    #         #     citeUrl = soup.find("tr",{"id":"docCites"})
    #         #     citeUrl = fullUrl(citeUrl.find('a')['href'])
    #         #     getCite(citeUrl, node)
    #         # except Exception, e:
    #         #     print ('no citetation')
    #         node.m.save()
    #     for refDictUse in node.defpaper:
    #         parsePaper(refDictUse['url'], level+1)
    #     # for citeDictUse in node.citebypaper:
    #     #     parsePaper(citeDictUse['url'], level+1)
    # except Exception, e:
    #     print "e :%s" % e
    #     print "Exception %s" %Exception
    
# def getCite(citationUrl, node):
#     citation_soup = BeautifulSoup(urllib2.urlopen(citationUrl))
#     all_citation_tar = citation_soup.find("div",{"id":"result_list"})
#     all_citation_tar = all_citation_tar.findAll("div",{"class":"result"})
#     for cite in all_citation_tar:
#         try:
#             citeDict = {"title":rePunctuation(cite.find("a",{"class":"remove doc_details"}).text), "url":cite.find("a",{"class":"remove doc_details"})['href']}
#             if citeDict["title"].find("et al") == -1:
#                 node.citebypaper.append(citeDict)
#             else:
#                 print "have et al"
#         except Exception, e:
#             print ("exception cite")
#     try:
#         citation_url_next = citation_soup.find('div',{"id":"pager"}).find('a')['href']
#         if citation_url_next:
#             citation_url_next = fullUrl(citation_url_next)
#             getCite(citation_url_next, node)
#     except Exception, e:
#             print ("exception push in")

if __name__ == '__main__':
    # url = "/search?q=%22mapreduce%22&submit=Search&sort=rlv&t=doc"
    url = "/search?q=%22volunteered+geographic+information%22&submit=Search&sort=rlv&t=doc"
    # url = "/viewdoc/summary?doi=10.1.1.51.5013"
    parsePaperList(url)  
    # s = "MapReduce: Simplified Data Processing on Large Clusters" 
    # m = re.search(r"\(([A-Za-z0-9_]+)\)", s)
    