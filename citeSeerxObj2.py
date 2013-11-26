from BeautifulSoup import BeautifulSoup, NavigableString
import urllib2
import sys
import re
from paperMiningSchema import Paper, InvertedIndex

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
        self.paperXMLURL = 'http://citeseerx.ist.psu.edu/oai2?verb=GetRecord&metadataPrefix=oai_dc&identifier=oai:CiteSeerX.psu:'
        self.refDict = {}


    def search_title(self, search_text): #change to cite Tree
        #text_parse
        search_text = search_text.replace(" ", "+");
        return self.search('http://citeseerx.ist.psu.edu/search?q='+search_text+'&submit=Search&sort=rlv&t=doc')

    def search(self, search_text):
        search_resp = urllib2.urlopen(search_text)
        search_soup = BeautifulSoup(search_resp)
        search_result = search_soup.findAll("div", {"class":"result"})
        for search_url in search_result:
            try:
                paperString = search_url.find("a",{"class":"remove doc_details"})['href']
                paperString = paperString.split('=')[2]
                paper_title_search = urllib2.urlopen(self.paperXMLURL+paperString)
                paper_title_search_soup = BeautifulSoup(paper_title_search)
                searchObj = paperObj()
                searchObj.insert(paper_title_search_soup.find('dc:title').text, paperString)
                nodeSearch = SeerXNode()
                nodeSearch.paper = searchObj
                self.search_list.append(nodeSearch)
                return self.search_list
            except Exception, e:
                print ("exception search push in to list")
        # self.next_count = self.next_count +1
        # try:
        #     search_url_next = search_soup.find('div',{"id":"pager"}).find('a')['href']
        #     if search_url_next and self.next_count<2:
        #         search_url_next = self.citeseerx_url + str(search_url_next)
        #         self.search(search_url_next)
        # except Exception, e:
        #     print ("exception search find next page")
        #return self.search_list
    
    def click_search(self, nodeIndex):
        #print nodeIndex
        newSearchNode = SeerXNode()
        newSearchNode = self.search_list[nodeIndex]
        self.get_doc_Two(newSearchNode.paper.url, 0)
        return self.refDict
    
    def get_doc_Two(self, url, levelCount):
        print ('\n %d' %levelCount)
        soup = BeautifulSoup(urllib2.urlopen(self.paperXMLURL+url))
        node = SeerXNode()
        node.paper.title = soup.find('dc:title').text
        node.paper.url = url
        print ('node url:%s' % node.paper.url) 
        if levelCount == 2:
            print ('count 2, node %s' % node.paper.title)
            return node
        else :
            try:
                refList = soup.findAll("dc:relation")
                for ref in refList:
                    print ('ref %s' % ref.text)
                    node.ref_list.append(self.get_doc_Two(ref.text, levelCount+1))
                if levelCount+1 in self.refDict:
                    listUse = self.refDict[levelCount+1]
                    listUse.extend(node.ref_list)
                    self.refDict[levelCount+1] = listUse
                else:
                    self.refDict[levelCount+1] = node.ref_list
            except Exception, e:
                print ('no ref')
            return node
            


    # def click(self, nextNode):
    #     print ("next Node : %s " % nextNode.paper.url)
    #     self.node_List.append(nextNode)
    #     nextNode.get_doc()
    #     nextNode.mergePaperTitle()
    #     return nextNode;
    #     #nextNode.printRefCite()

    # def printNode(self, NodeNeedPrint):
    #     NodeNeedPrint.printRefCite()


class SeerXNode:
    def __init__(self):
        self.paper = paperObj()
        #self.citeseerx_url = "http://citeseerx.ist.psu.edu" #change to every on need
    	self.citeseerx_url ='http://citeseerx.ist.psu.edu/oai2?verb=GetRecord&metadataPrefix=oai_dc&identifier=oai:CiteSeerX.psu:'
        self.ref_list = [] # SeerXNode(s)
    	#self.cite_list = [] # SeerXNode(s)
        self.doc_soup = ""
        self.titleMerge = ""

    # def get_doc(self):
    #     self.doc_soup = BeautifulSoup(urllib2.urlopen(self.citeseerx_url+str(self.paper.url)))
    #     #self.paper.insert() insert title, url
    #     #ref
    #     try:
    #         all_ref_tar = self.doc_soup.findAll("dc:relation")
    #         self.get_ref(all_ref_tar)
    #     except Exception, e:
    #         print "no ref"
        
        # #cite
        # try:
        #     cite_url = self.doc_soup.find("tr",{"id":"docCites"})
        #     cite_url = self.citeseerx_url + cite_url.find('a')['href']
        #     self.get_cite(cite_url)
        # except Exception, e:
        #     print "no cite"
        

        # return self

    # def get_ref(self, all_ref):
    #     for ref in all_ref:
    #         ref_soup = BeautifulSoup(urllib2.urlopen(self.citeseerx_url+str(ref.text)))
    #         ref_obj = paperObj()
    #         ref_obj.insert(ref_soup.find('dc:title').text, ref.text)
    #         refNode = SeerXNode()
    #         refNode.paper = ref_obj
    #         self.ref_list.append(refNode)
        

    # def get_cite(self, citation_url):
    #     citation_soup = BeautifulSoup(urllib2.urlopen(citation_url))
    #     all_citation_tar = citation_soup.find("div",{"id":"result_list"})
    #     all_citation_tar = all_citation_tar.findAll("div",{"class":"result"})
    #     for cite in all_citation_tar:
    #         try:
    #             # print cite.find("a",{"class":"remove doc_details"}).text
    #             # print cite.find("a",{"class":"remove doc_details"})['href']
    #             # print search_url.find("span",{"class":"authors"}).text
    #             # print search_url.find("span",{"class":"pubvenue"}).text
    #             # print search_url.find("span",{"class":"pubyear"}).text
    #             # print search_url.find("div",{"class":"snippet"}).text
    #             citeObj = paperObj()
    #             citeObj.insert(cite.find("a",{"class":"remove doc_details"}).text, cite.find("a",{"class":"remove doc_details"})['href'])
    #             citeNode = SeerXNode()
    #             citeNode.paper = citeObj
    #             self.cite_list.append(citeNode)
    #         except Exception, e:
    #             print ("exception cite")
    #     try:
    #         citation_url_next = citation_soup.find('div',{"id":"pager"}).find('a')['href']
    #         if citation_url_next:
    #             citation_url_next = self.citeseerx_url + str(citation_url_next)
    #             self.get_cite(citation_url_next)
    #     except Exception, e:
    #             print ("exception push in")

    # def printRefCite(self):
    #     for ref in self.ref_list:
    #         print ("ref title : %s" % ref.paper.title)
    #         print ("ref url : %s" % ref.paper.url)
    #         print ("")
    #     for cite in self.cite_list:
    #         print ("cite title :%s" % cite.paper.title)
    #         print ("cite url :%s" % cite.paper.url)
    #         print ("")
    
    # def mergePaperTitle(self):
    #     for ref in self.ref_list:
    #         self.titleMerge = self.titleMerge + ref.paper.title+' '
    #     # for cite in self.cite_list:
    #     #     self.titleMerge = self.titleMerge + cite.paper.title+', '
    #     print self.titleMerge

if __name__ == '__main__':
    testGraph = citeGraph()
    #testGraph.search_title("text")
    textSearch = 'Fast Reactive Control for Illumination Through Rain and Snow'
    testGraph.search_title(textSearch)
    levelZeroNode = SeerXNode()
    testGraph.click_search(0)
    # print testGraph.refDict
    # for node in testGraph.refDict[1]:
    #     print node.paper.url
    # print ('\n')
    # for node in testGraph.refDict[2]:
    for x in xrange(1,4):
        for node in testGraph.refDict[x]:
            print "level: %d, node url:%s" % (x, node.paper.url)
        