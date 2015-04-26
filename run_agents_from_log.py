import csv
import Agent
import GeneticAlgorithm
import json
# set the log file, how many agents to test, and the goal
logfile = 'logs/RAOP-20150425175651-log.csv'
numAgents = 5000
goal = 0.65
kaggleRequests = []
fh = open('kaggle/kaggle_test.csv', 'r')
reader = csv.reader(fh)
header = reader.__next__()
for line in reader:
    data = dict(zip(header, line))
    data['received_pizza'] = json.loads(data['received_pizza'].lower())
    kaggleRequests.append(data)

fh.close()

fh = open(logfile, 'r')
reader = csv.reader(fh)
header = reader.__next__()
for field in ['ID', 'Gen', 'Score']:
    header.remove(field)

bestScore = 0.0
bestAgent = None
for i, agent in enumerate(reader):
    if i >= numAgents:
        break
    
    agentObj = Agent.serializeAgent(header, agent)
    score = GeneticAlgorithm.runAgentAgainstTest(agentObj, kaggleRequests, True)
    if score > bestScore:
        bestScore = score
        bestAgent = agentObj
    
    if bestScore > goal:
        GeneticAlgorithm.runAgentAgainstTest(agentObj, kaggleRequests, False)
        break

fh.close()
