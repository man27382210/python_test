import sys
from dataset_statuses import Dataset

dataset = Dataset()
statuses = dataset.statuses()
flag = 0
count = 10
q = 'mapreduce'
for status in statuses:
	if status['Name']=='Papers':
		print status['Name'],status['Count']

def show_paper(text):
	for paper in text:
		print paper['title']


for(){
    
}
dataset.set_parameters('flag',flag)
dataset.set_parameters('count',count)
dataset.set_parameters('q',q)
text = dataset.get_papers()
show_paper(text)
