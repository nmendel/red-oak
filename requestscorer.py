#Request Scorer
import codecs
import json
import os
from RequestInfo import RequestInfo

def read_dataset(path):
    with codecs.open(path, 'r', 'utf-8') as myFile:
        content = myFile.read()
    dataset = json.loads(content)
    return dataset

def print_text(dataset):
    for datnum in dataset:
        req = RequestInfo(datnum)
        req.score_request();
        input()

if __name__ == '__main__':
    path = './train.json'
    dataset = read_dataset(path)
    print_text(dataset)
