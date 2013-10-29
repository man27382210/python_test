from BeautifulSoup import BeautifulSoup, NavigableString
import urllib2
import sys
import re

class paperObj:
    def __init__(self):
        self.title = ""
        self.url = ""
        #self.abstarct = ""
    def insert(self, title, url):
        self.title = title #remove em
        self.url = url

class citeGraph:
    def __init__(self):
        self.node_List  = []
        self.tree_List = []
        self.search_list = [] #change to citeTree
        self.next_count = 0 # change to citeTree
        self.cite_url = "http://citeseerx.ist.psu.edu"

    def search_title(self, search_text): #change to cite Tree
        #text_parse
        search_text = search_text.replace(" ", "+");
        #return self.search('http://citeseerx.ist.psu.edu/search?q=Adapting+to+Network+and+Client+Variation+Using+Active+Proxies&submit=Search&sort=rlv&t=doc') 
        return self.search('http://citeseerx.ist.psu.edu/search?q='+search_text+'&submit=Search&sort=rlv&t=doc')

    def search(self, search_text):
        search_resp = urllib2.urlopen(search_text)
        search_soup = BeautifulSoup(search_resp)
        search_result = search_soup.findAll("div", {"class":"result"})
        for search_url in search_result:
            try:
                #print search_url.find("a",{"class":"remove doc_details"})['href']
                #dataTitle =  search_url.find("a",{"class":"remove doc_details"}).text
                #self.striphtml(search_url.find("a",{"class":"remove doc_details"}).text)
                #dataTitle = self.striphtml(dataTitle)
                #print search_url.find("a",{"class":"remove doc_details"}).text;

                paper_title_search = urllib2.urlopen(self.cite_url+search_url.find("a",{"class":"remove doc_details"})['href'])
                paper_title_search_soup = BeautifulSoup(paper_title_search)
                #print paper_title_search_soup.find('div', {"id":"viewHeader"}).find('h2').text
                #print ("print %s" % search_url.find("a",{"class":"remove doc_details"}).contents)
                #search_url.find("a",{"class":"remove doc_details"}).contents
                # print search_url.find("span",{"class":"authors"}).text
                # print search_url.find("span",{"class":"pubvenue"}).text
                # print search_url.find("span",{"class":"pubyear"}).text
                # print search_url.find("div",{"class":"snippet"}).text
                searchObj = paperObj()
                searchObj.insert(paper_title_search_soup.find('div', {"id":"viewHeader"}).find('h2').text, search_url.find("a",{"class":"remove doc_details"})['href'])
                nodeSearch = SeerXNode()
                nodeSearch.paper = searchObj
                self.search_list.append(nodeSearch)
            except Exception, e:
                print ("exception search push in to list")
        self.next_count = self.next_count +1
        try:
            search_url_next = search_soup.find('div',{"id":"pager"}).find('a')['href']
            if search_url_next and self.next_count<2:
                search_url_next = self.citeseerx_url + str(search_url_next)
                self.search(search_url_next)
        except Exception, e:
            print ("exception search find next page")
        return self.search_list
    
    def click_search(self, nodeIndex):
        print nodeIndex
        newSearchNode = SeerXNode()
        newSearchNode = self.search_list[nodeIndex]
        self.node_List.append(newSearchNode)
        newSearchNode.get_doc()
        #newSearchNode.printRefCite()
        return newSearchNode;
        #self.click(newSearchNode.ref_list[1])

    def click(self, nextNode):
        print ("next Node : %s " % nextNode.paper.url)
        self.node_List.append(nextNode)
        nextNode.get_doc()
        nextNode.printRefCite()

    def printNode(self, NodeNeedPrint):
        NodeNeedPrint.printRefCite()


class SeerXNode:
    def __init__(self):
        self.paper = paperObj()
        self.citeseerx_url = "http://citeseerx.ist.psu.edu" #change to every on need
    	self.ref_list = [] # SeerXNode(s)
    	self.cite_list = [] # SeerXNode(s)
        self.doc_soup = ""
        self.titleMerge = ""
        self.tfidfFdist = {}

    def get_doc(self):
        self.doc_soup = BeautifulSoup(urllib2.urlopen(self.citeseerx_url+str(self.paper.url)))
        #self.paper.insert() insert title, url
        #ref
        all_ref_tar = self.doc_soup.find("div",{"id":"citations"})
        all_ref_tar = all_ref_tar.findAll("tr")
        self.get_ref(all_ref_tar)
        #cite
        cite_url = self.doc_soup.find("tr",{"id":"docCites"})
        cite_url = self.citeseerx_url + cite_url.find('a')['href']
        self.get_cite(cite_url)

        return self

    def get_ref(self, all_ref):
        for ref in all_ref:
            ref_obj = paperObj()
            ref_obj.insert(ref.find("a").text, ref.find("a")['href'])
            refNode = SeerXNode()
            refNode.paper = ref_obj
            self.ref_list.append(refNode)

    def get_cite(self, citation_url):
        citation_soup = BeautifulSoup(urllib2.urlopen(citation_url))
        all_citation_tar = citation_soup.find("div",{"id":"result_list"})
        all_citation_tar = all_citation_tar.findAll("div",{"class":"result"})
        for cite in all_citation_tar:
            try:
                # print cite.find("a",{"class":"remove doc_details"}).text
                # print cite.find("a",{"class":"remove doc_details"})['href']
                # print search_url.find("span",{"class":"authors"}).text
                # print search_url.find("span",{"class":"pubvenue"}).text
                # print search_url.find("span",{"class":"pubyear"}).text
                # print search_url.find("div",{"class":"snippet"}).text
                citeObj = paperObj()
                citeObj.insert(cite.find("a",{"class":"remove doc_details"}).text, cite.find("a",{"class":"remove doc_details"})['href'])
                citeNode = SeerXNode()
                citeNode.paper = citeObj
                self.cite_list.append(citeNode)
            except Exception, e:
                print ("exception cite")
        try:
            citation_url_next = citation_soup.find('div',{"id":"pager"}).find('a')['href']
            if citation_url_next:
                citation_url_next = self.citeseerx_url + str(citation_url_next)
                self.get_cite(citation_url_next)
        except Exception, e:
                print ("exception push in")

    def printRefCite(self):
        for ref in self.ref_list:
            print ("ref title : %s" % ref.paper.title)
            print ("ref url : %s" % ref.paper.url)
            print ("")
        for cite in self.cite_list:
            print ("cite title :%s" % cite.paper.title)
            print ("cite url :%s" % cite.paper.url)
            print ("")
    
    def mergePaperTitle():
        for ref in self.ref_list:
            self.titleMerge.append(ref.paper.title+', ')
        for cite in self.cite_list:
            self.titleMerge.append(cite.paper.title+', ')
        print self.titleMerge

    def tfidfCount(data):
        return tfidfFdist
if __name__ == '__main__':
    testGraph = citeGraph()
    #testGraph.search_title("text")
    textSearch = 'Adapting to Network and Client Variation Using Active Proxies'
    testGraph.search_title(textSearch)
    testGraph.click_search(0)