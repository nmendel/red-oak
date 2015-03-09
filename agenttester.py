#TODO This module will contain functionality to test previously trained agents
import json
import codecs


"""
FIXME Finish implementing and testing
"""
class AgentTester():
    def testAgentOnFile(self, agent, testfile):
        dataset = self.read_dataset(testfile)
        results = self.testAgent(agent, dataset)
        return results


    """
    test agent on data to generate result list
    """
    def testAgent(self, agent, testdata):
        results = []

        for testdatum in testdata:
            result = self.evaluate(agent, testdatum)
            results.append(result)

        return results


    """
    Function to read data from a file to a json dataset
    """
    def read_dataset(self, path):
        with codecs.open(path, 'r', 'utf-8') as myFile:
            content = myFile.read()
        dataset = json.loads(content)
        return dataset

    """
    Evaluates the passed request using the given agent, adds whether or not the request was actually successful, and generates a result
    """
    def evaluate(self, agent, request):
        #FIXME Replace request_id and received_pizza with field names for scored requests
        key = request.request_id
        predicted = agent.scoreRequest(request)
        actual = request.requester_received_pizza
        testResult = TestResult(key, predicted, actual)
        return testResult


"""
class to hold the result of an agent test
"""
class TestResult():
    key = -1
    predicted = -1
    actual = -1

    def __init__(self, key, predicted, actual):
        self.key = key
        self.predicted = predicted
        self.actual = actual

"""
Dummy Agent to test functionality
"""
class DummyAgent():
    def scoreRequest(self, request):
        return True



if __name__ == '__main__':
    agentTester = AgentTester()
    #FIXME Replace with ScoredRequest Test File
    path = './pizza_request_dataset/kfold0/test_data_fold0.json'
    agent = DummyAgent()
    print agentTester.testAgentOnFile(agent, path)