#Request Scorer
import codecs
import json
import os
import csv
from RequestInfo import RequestInfo

def read_dataset(path):
    with codecs.open(path, 'r', 'utf-8') as myFile:
        content = myFile.read()
    dataset = json.loads(content)
    return dataset

def print_text(dataset):
    for datnum in dataset:
        req = RequestInfo(datnum)
        print(req.score_narrative())        
        input()

def write_csv(dataset):
    csvfile = open('output.csv', 'w')
    swriter = csv.writer(csvfile)
    swriter.writerow(['id', 'received_pizza', 'student', 'money', 'job', 'family', 'desire'])
    for datnum in dataset:
        reqI = RequestInfo(datnum)
        req = reqI.score_narrative()
        swriter.writerow([datnum['request_id'], datnum['requester_received_pizza'], req['student'], req['money'], req['job'], req['family'], req['desire']])
        
if __name__ == '__main__':
    path = './train.json'
    dataset = read_dataset(path)
    #print_text(dataset)
    write_csv(dataset)
