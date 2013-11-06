from bottle import Bottle, run, route, request, response, template
import bottle
import json
import citeSeerxObj
import googlePlusTF_IDF

app = bottle.Bottle()
testGraph = citeSeerxObj.citeGraph()
nltkTFIDF = googlePlusTF_IDF.ntlk_tf_idf()
resultObj = citeSeerxObj.SeerXNode()
app.config['mixTitle'] = ''
print app.config

@app.route('/hello')
def hello():
    return "Hello World!"

@app.route('/search')
def index():
	
	textSearch = request.query.queryString
	results = testGraph.search_title(textSearch)
	jsonList = []
	jsonob = {}
	for result in results:
		jsonob = {"title":result.paper.title,"url":result.paper.url}
		jsonList.append(jsonob)
	jsonObj = json.dumps(jsonList)
	return jsonObj

@app.route('/searchIndex')
def index():
	textIndex = request.query.queryIndex
	resultObj = testGraph.click_search(int(textIndex))
	app.config['mixTitle'] = resultObj.titleMerge
	jsonob = {}
	jsonRefArray = []
	jsonCiteArray = []
	for cite in resultObj.cite_list:
		jsonCiteArray.append({"title":cite.paper.title, 'url':cite.paper.url})
	for ref in resultObj.ref_list:
		jsonRefArray.append({"title":ref.paper.title, 'url':ref.paper.url})
	jsonob["title"] = resultObj.paper.title
	jsonob["url"] = resultObj.paper.url
	jsonob["jsonCiteArray"] = jsonCiteArray
	jsonob["jsonRefArray"] = jsonRefArray
	jsonObj = json.dumps(jsonob)
	return jsonObj

@app.route('/counttfidf')
def index():
	print app.config['mixTitle']
	print nltkTFIDF.searchForTitleTFIDF(app.config['mixTitle'])
	jsonObj = json.dumps(nltkTFIDF.searchForTitleTFIDF(app.config['mixTitle']))
	return jsonObj

run(app, host='localhost', port=8080)