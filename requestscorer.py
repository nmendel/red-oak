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
    count = 1
    csvfile = open('scored_test.csv', 'w', newline='') # scored_pizza_request_dataset 
    swriter = csv.writer(csvfile)
    swriter.writerow(['id', 'received_pizza', 'text_student', 'text_money',
		'text_job', 'text_family', 'text_desire', 'meta_num_words', 
		'meta_account_age', 'meta_length_of_time_on_raop', 'request_type'])
    for datnum in dataset:
        reqI = RequestInfo(datnum)
        req = reqI.score_narrative()

        #Set the request type. For every five data, one will be marked test, the other four will be marked train
        if count%5 == 0 :
            request_type = 'test'
            count = 1
        else:
            request_type = 'train'
            count += 1

        #Write the data to the csv
        swriter.writerow([datnum['request_id'],
                          str(datnum.get('requester_received_pizza','false')).lower(),
						  req['student'], req['money'], req['job'], req['family'], req['desire'],
                          reqI.score_request_length(),
                          reqI.score_requester_account_age_in_days_at_request(),
                          reqI.score_requester_days_since_first_post_on_raop_at_request(),
                          request_type])

        
if __name__ == '__main__':
    path = './pizza_request_dataset/test.json' #pizza_request_dataset.json'
    dataset = read_dataset(path)
    #print_text(dataset)
    write_csv(dataset)
