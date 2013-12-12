require(tm)
require(jsonlite)
inputfile <- "data2.json"
result = fromJSON(inputfile)
for (i in result['1']){
  print(i)
}