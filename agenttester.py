#TODO This module will contain functionality to test previously trained agents
import json
import codecs

#TODO Finish implementing and testing
class AgentTester():
    def testAgentOnFile(self, agent, testfile):
        dataset = self.read_dataset(testfile)
        results = self.testAgent(agent, dataset)
        return results

    def testAgent(self, agent, testdata):
        results = []

        #test agent on data
        #to generate result list
        for testdatum in testdata:
            result = self.evaluate(agent, testdatum)
            results.append(result)

        return results


    def read_dataset(self, path):
        with codecs.open(path, 'r', 'utf-8') as myFile:
            content = myFile.read()
        dataset = json.loads(content)
        return dataset

    #TODO implement
    def evaluate(self, agent, testdatum):
        testResult = TestResult()
        testResult.key = testdatum.key
        testResult.predicted = 0
        testResult.actual = testdatum.wasSuccessful
        return testResult

#class to hold the result of an agent test
class TestResult():
    key = -1
    predicted = -1
    actual = -1

    def __init__(self, key, predicted, actual):
        self.key = key
        self.predicted = predicted
        self.actual = actual