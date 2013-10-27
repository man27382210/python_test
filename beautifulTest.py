import re
from BeautifulSoup import BeautifulSoup

# ht = '''
# <div id="abc">
#     some long text goes <a href="/"> here </a> and hopefully it 
#     will get picked up by the parser as content
# </div>
# '''

ht = '''
[u'\n  The ', <em>Network</em>, u' Weather Service: A Distributed Resource Performance Forecasting Service\n                  ']

'''
# soup = BeautifulSoup(ht)

# anchors = soup.findAll('em')
# for a in anchors:
# 	print a.previousSibling
# 	print a.string
#   	a.previousSibling.replaceWith(a.previousSibling + a.string)


# results = soup.findAll(text=lambda(x): len(x) > 20)

# print results


def flatten_tags(s, tags):
   pattern = re.compile(r"<(( )*|/?)(%s)(([^<>]*=\\\".*\\\")*|[^<>]*)/?>"%(isinstance(tags, basestring) and tags or "|".join(tags)))
   return pattern.sub("", s)
tag = '<em>'
print flatten_tags(ht, tag)