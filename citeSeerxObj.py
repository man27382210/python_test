from bs4 import BeautifulSoup
import urllib2
import sys

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

    def search_title(self, search_text): #change to cite Tree
        #text_parse
        return self.search('http://citeseerx.ist.psu.edu/search?q=Adapting+to+Network+and+Client+Variation+Using+Active+Proxies&submit=Search&sort=rlv&t=doc')

    def search(self, search_text):
        search_resp = urllib2.urlopen(search_text)
        search_soup = BeautifulSoup(search_resp)
        search_result = search_soup.find_all("div", {"class":"result"})
        for search_url in search_result:
            try:
                #print search_url.find("a",{"class":"remove doc_details"})['href']
                #print search_url.find("a",{"class":"remove doc_details"}).text
                # print search_url.find("span",{"class":"authors"}).text
                # print search_url.find("span",{"class":"pubvenue"}).text
                # print search_url.find("span",{"class":"pubyear"}).text
                # print search_url.find("div",{"class":"snippet"}).text
                searchObj = paperObj()
                searchObj.insert(search_url.find("a",{"class":"remove doc_details"}).text, search_url.find("a",{"class":"remove doc_details"})['href'])
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
    # def click(self, nodeIndex):
    #     newNode = SeerXNode()
    #     newNode = self.node_List[nodeIndex]
    #     newNode.get_doc()



class SeerXNode:
    def __init__(self):
        self.paper = paperObj()
        self.citeseerx_url = "http://citeseerx.ist.psu.edu" #change to every on need
    	self.ref_list = [] # SeerXNode(s)
    	self.cite_list = [] # SeerXNode(s)
        self.doc_soup = ""

    def get_doc(self, paper_url):
        self.doc_soup = BeautifulSoup(urllib2.urlopen(self.citeseerx_url+str(paper_url)))
        #self.paper..insert() insert title, url
        #ref
        all_ref_tar = self.doc_soup.find("div",{"id":"citations"})
        all_ref_tar = all_ref_tar.find_all("tr")
        self.get_ref(all_ref_tar)
        #cite
        cite_url = self.doc_soup.find("tr",{"id":"docCites"})
        cite_url = self.citeseerx_url + cite_url.find('a')['href']
        self.get_cite(cite_url)

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
        all_citation_tar = all_citation_tar.find_all("div",{"class":"result"})
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

testGraph = citeGraph()
testGraph_List = []
testGraph_List = testGraph.search_title("text")

test = SeerXNode()
#test_list = []
#test_list = test.search_title("text")
#parse to frontend, select which index
test.get_doc(testGraph_List[0].paper.url)
print ("list_url:%s" % testGraph_List[0].paper.url)
test.printRefCite()

#next node
# print ("url:%s" % test.ref_list[1].paper.url)
# test.get_doc(test.ref_list[1].paper.url)
# test.printRefCite()