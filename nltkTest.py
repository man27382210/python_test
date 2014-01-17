import nltk
import json

json_data=open('data2.json')
levelDict = json.load(json_data)
json_data.close()

token_dict = {}
for x in xrange(1,len(levelDict)+1):
    levelUse = levelDict[str(x)]
    token_list = []
    for title in levelUse:
        text = nltk.word_tokenize(title)
        # print nltk.pos_tag(text)
        token_list.append(nltk.pos_tag(text))
    token_dict[str(x)] = token_list

with open('token.json', 'w') as outfile:
    json.dump(token_dict, outfile)
       