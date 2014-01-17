import MongoMing2
import json
# from nltk.corpus import wordnet
# from nltk.corpus import stopwords
# nltk.download('stopwords')

if __name__ == '__main__':
    levelZero = []
    levelOne = []
    levelTwo = []
    firstNode = MongoMing2.Paper.m.find({"url":"/viewdoc/summary?doi=10.1.1.163.5292"}).first()
    for paper in firstNode['defpaper']:
        dict = {"title":paper['title'], "url":paper['url']}
        levelZero.append(dict)

    for levelZeroPaper in levelZero:
        oneNode = MongoMing2.Paper.m.find({'url':levelZeroPaper['url']}).first()
        try:
            for paperOne in oneNode['defpaper']:
                # print "title : %s" % paperOne['title']
                dict = {"title":paperOne['title'], "url":paperOne['url']}
                levelOne.append(dict)    
        except Exception, e:
            print "no ref"

    for levelOnePaper in levelOne:
        secNode = MongoMing2.Paper.m.find({'url':levelOnePaper['url']}).first()
        try:
            for paperTwo in secNode['defpaper']:
                # print "title : %s" % paperTwo['title']
                dict = {"title":paperTwo['title'], "url":paperTwo['url']}
                levelTwo.append(dict)    
        except Exception, e:
            print "no ref"



    # arrayZeroTitle = ""
    # arrayOneTitle = ""
    # arrayTwoTitle = ""
    
    # for paper in levelZero:
    #     arrayZeroTitle = arrayZeroTitle + paper['title'] + " "
    # for paper in levelOne:
    #     arrayOneTitle = arrayOneTitle + paper['title'] + " " 
    # for paper in levelTwo:
    #     arrayTwoTitle = arrayTwoTitle + paper['title'] + " "
    # f = open('data.json', 'w')
    # f.write(arrayZeroTitle.encode("utf-8")+'\n')
    # f.write(arrayOneTitle.encode("utf-8")+'\n')
    # f.write(arrayTwoTitle.encode("utf-8"))

    listZeroTitle = []
    listOneTitle = []
    listTwoTitle = []
    for paper in levelZero:
        listZeroTitle.append(paper['title'])
    for paper in levelOne:
        listOneTitle.append(paper['title']) 
    for paper in levelTwo:
        listTwoTitle.append(paper['title'])
    dic = {'1':listZeroTitle, '2':listOneTitle, '3':listTwoTitle}

    print 'listZeroTitle :%s' % len(listZeroTitle)
    print 'listOneTitle :%s' % len(listOneTitle)
    print 'listTwoTitle :%s' % len(listTwoTitle)

    # with open('data2.json', 'w') as outfile:
    #     json.dump(dic, outfile)
    