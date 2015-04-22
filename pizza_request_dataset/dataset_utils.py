import codecs
import json
import os

def read_dataset(path):
    with codecs.open(path, 'r', 'utf-8') as myFile:
        content = myFile.read()
    dataset = json.loads(content)
    return dataset

def create_kfolds(dataset):
    #Run loop five times to generate five k-folds for training/testing
    for x in range(0, 5):
        testdataset = []
        traindataset = []
        count = x
        dirname = r'kfold%d' % x
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        for datum in dataset:
            #line to ignore data in kaggle set
            if '"in_test_set": true,' not in datum:
                if count % 5 == 0:
                    testdataset.append(datum)
                else:
                    traindataset.append(datum)
                count += 1
        testfilename = r'./kfold%d/test_data_fold%d.json' % (x, x)
        with open(testfilename, 'w') as testfile:
            json.dump(testdataset, testfile, indent=4, separators=(',', ': '))
        trainfilename = r'./kfold%d/train_data_fold%d.json' % (x, x)
        with open(trainfilename, 'w') as trainfile:
            json.dump(traindataset, trainfile, indent=4, separators=(',', ': '))

if __name__ == '__main__':
    path = './pizza_request_dataset.json'
    dataset = read_dataset(path)
    create_kfolds(dataset)
