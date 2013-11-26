from bottle import Bottle, run, route, request, response, template
import bottle
import json
import citeSeerxObj2
import googlePlusTF_IDF
import spiderMongo

app = bottle.Bottle()
testGraph = citeSeerxObj2.citeGraph()
nltkTFIDF = googlePlusTF_IDF.ntlk_tf_idf()
mongoTS = spiderMongo.mongoTest()
resultDict = {}
resultUse = {}

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
    resultDict = testGraph.click_search(int(textIndex))
    # resultDict = {1:[docs], 2:[docs]...}
    for x in xrange(1,len(resultDict)+1):
        for doc in resultDict[x]:
            if x in resultUse:
                    resultUse[x].append(doc.paper.title)
            else:
                resultUse[x] = []
                resultUse[x].append(doc.paper.title)
    return resultUse

@app.route('/counttfidf')
def index():
    # resultUse = {1: [u'Spatio-temporal frequency analysis for removing rain and snow from videos', u'A Multi-Layered Display with Water Drops'], 2: [u'Detection and removal of rain from videos', u'When does a camera see rain', u'Why is Snow So Bright', u'RAIN REMOVAL IN VIDEO BY COMBINING TEMPORAL AND CHROMATIC PROPERTIES', u'A projector-camera system for creating a display with water drops', u'An Immaterial Depth-Fused 3D Display']}
    
    print resultUse
    levelUse = []
    levelDict = {}
    levelResult = {}
    for x in xrange(1,len(resultUse)+1):
        levelUse = resultUse[x]
        levelUse = nltkTFIDF.computeTFIDf(nltkTFIDF.idf(levelUse, nltkTFIDF.tf(levelUse)))
        levelDict[x] = levelUse
    levelResult['levelDict'] = levelDict
    levelResult['resultUse'] = resultUse
    print levelResult
    return levelResult

@app.route('/counttfidftwo')
def index():
    # resultUse = {1: [u'Spatio-temporal frequency analysis for removing rain and snow from videos', u'A Multi-Layered Display with Water Drops'], 2: [u'Detection and removal of rain from videos', u'When does a camera see rain', u'Why is Snow So Bright', u'RAIN REMOVAL IN VIDEO BY COMBINING TEMPORAL AND CHROMATIC PROPERTIES', u'A projector-camera system for creating a display with water drops', u'An Immaterial Depth-Fused 3D Display']}
    resultUse = mongoTS.mix()
    nltkTFIDF.extractTitleLemma("MapReduce simplified data processing on large clusters")
    levelUse = []
    levelDict = {}
    levelResult = {}
    for x in xrange(0,len(resultUse)):
        i = str(x)
        levelUse = resultUse[i]
        levelUse = nltkTFIDF.computeTFIDf(nltkTFIDF.idf(levelUse, nltkTFIDF.tf(levelUse)))
        levelDict[i] = levelUse
    levelResult['levelDict'] = levelDict
    levelResult['resultUse'] = resultUse
    # print levelResult
    return levelResult
run(app, host='localhost', port=8080)