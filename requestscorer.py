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

def write_csv(dataset, path):
    count = 1
    csvfile = open(path, 'w', newline='') # scored_pizza_request_dataset
    swriter = csv.writer(csvfile)
    swriter.writerow(['id', 'received_pizza', 'text_student', 'text_money',
                      'text_job', 'text_family', 'text_desire',
                      'meta_num_words',
                      'meta_account_age',
                      'meta_length_of_time_on_raop',
                      'requester_account_age_in_days_at_retrieval',
                      'requester_upvotes_minus_downvotes_at_request',
                      'requester_upvotes_minus_downvotes_at_retrieval',
                      'requester_upvotes_plus_downvotes_at_request',
                      'requester_upvotes_plus_downvotes_at_retrieval',
                      #'post_was_edited',
                      'requester_number_of_comments_at_request',
                      'requester_number_of_comments_at_retrieval',
                      'requester_number_of_posts_at_request',
                      'requester_number_of_posts_at_retrieval',
                      'requester_number_of_subreddits_at_request',
                      'requester_user_flair',
                      'requester_number_of_comments_in_raop_at_request',
                      'requester_number_of_comments_in_raop_at_retrieval'
                      ])
    for datnum in dataset:
        reqI = RequestInfo(datnum)
        req = reqI.score_narrative()

        #Write the data to the csv
        swriter.writerow([datnum['request_id'],
                          str(datnum.get('requester_received_pizza','false')).lower(),
                          req['student'], req['money'], req['job'], req['family'], req['desire'],
                          reqI.score_request_length(),
                          reqI.score_requester_account_age_in_days_at_request(),
                          reqI.score_requester_days_since_first_post_on_raop_at_request(),
                          reqI.score_requester_account_age_in_days_at_retrieval(),
                          reqI.score_requester_upvotes_minus_downvotes_at_request(),
                          reqI.score_requester_upvotes_minus_downvotes_at_retrieval(),
                          reqI.score_requester_upvotes_plus_downvotes_at_request(),
                          reqI.score_requester_upvotes_plus_downvotes_at_retrieval(),
                          #reqI.score_post_was_edited(),
                          reqI.score_requester_number_of_comments_at_request(),
                          reqI.score_requester_number_of_comments_at_retrieval(),
                          reqI.score_requester_number_of_posts_at_request(),
                          reqI.score_requester_number_of_posts_at_retrieval(),
                          reqI.score_requester_number_of_subreddits_at_request(),
                          reqI.score_requester_user_flair(),
                          reqI.score_requester_number_of_comments_in_raop_at_request(),
                          reqI.score_requester_number_of_comments_in_raop_at_retrieval()
                          ])


if __name__ == '__main__':
    # path = './pizza_request_dataset/test.json' #pizza_request_dataset.json'
    # dataset = read_dataset(path)
    # #print_text(dataset)
    # write_csv(dataset)
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".json"):
                path = (os.path.join(root, file))
                dataset = read_dataset(path)
                (csvPath, ext) = os.path.splitext(path)
                csvPath += '.csv'
                write_csv(dataset, csvPath)
