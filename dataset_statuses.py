import urllib,urllib2,sys,json

class Dataset:
	def __init__(self):
		self.CALLBACK_URL = 'http://140.118.175.209/paper/'
		self.flag = 0
		self.count = 20
		self.q = ''

	def set_parameters(self,key,value):
		if key =='flag':
			self.flag = value
		elif key == 'count':
			self.count = value
		elif key =='q':
			self.q = value
		else:
			return "Key or Value format error."

	def get_papers(self):
		data = urllib.urlencode({"count":self.count, "flag":self.flag, "q":self.q})
		u =  urllib2.urlopen(self.CALLBACK_URL+'?%s' % data)
		result = u.read()
		papers = json.loads(result)
		return papers
		#for paper in papers:
		#	print paper['IndexId'],paper['PaperTitle']

	def statuses(self):
		result = urllib2.urlopen(self.CALLBACK_URL+'statuses.php').read()
		status = json.loads(result)
		return status
