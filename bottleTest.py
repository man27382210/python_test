from bottle import Bottle, run, route, request, response, template
import json
import citeSeerxObj

app = Bottle()
testGraph = citeSeerxObj.citeGraph()

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


run(app, host='localhost', port=8080)