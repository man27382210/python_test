from bs4 import BeautifulSoup
import urllib2
import sys
import xml.sax


class ABContendHandler(xml.sax.ContentHandler):
 	def __init__(self):
 		xml.sax.ContentHandler.__init__(self)

 	def startElement(self, name, attrs):
 		print("startElement:"+name)
 		#if name=="article":
 		#	print("attribute type:" + attrs.getValue("mdate"))

 	def endElement(self, name):
 		print("endElement:"+ name)

 	def characters(self, content):
 		print("charactres:"+content)
        
def main(sourceFileName):
	source=open(sourceFileName)
	xml.sax.parse(source, ABContendHandler())

if __name__=="__main__":
	main("test.xml")