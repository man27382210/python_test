from BeautifulSoup import BeautifulSoup, NavigableString
import urllib2

#how to get the 10.x.x.x... in cite seer
search_resp = urllib2.urlopen('http://citeseerx.ist.psu.edu/showciting?doi=10.1.1.42.2177')
search_soup = BeautifulSoup(search_resp)
splitString = search_soup.find("a", {"class":"remove doc_details"})['href']
print splitString.split('=')[2]