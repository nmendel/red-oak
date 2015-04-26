# This module will contain functionality to train agents genetically

from random import randint, random, uniform
import sys
import os
import csv
import json
from datetime import datetime
from pprint import pprint

import Constants as C
from Agent import Agent, weightLabel, threshLabel

DEFAULT_NUM_TEAMS = 30


class GeneticAlgorithm(object):
    genNumber = 0
    agentID = 1000
    
    trainingRequests = []
    testRequests = []
    kaggleRequests = []

    """
    Set up the genetic algorithm. Set the number of agents, number of generations,
    and agent fields.  Also get all of the pizza requests into memory.
    """
    def __init__(self, dataFile, testFile, numAgents=DEFAULT_NUM_TEAMS, numGenerations=0, kaggleFile=None):
        self.dataFile = dataFile
        self.testFile = testFile
        self.numAgents = int(numAgents)
        self.numGenerations = int(numGenerations)
        self.kaggleFile = kaggleFile
        
        fh = open(self.dataFile, 'r')
        fh2 = open(self.testFile, 'r')
        trainreader = csv.reader(fh)
        testreader = csv.reader(fh2)
        header = trainreader.__next__()
        testreader.__next__()
        self.cacheRequests(trainreader, testreader, header)
        fh.close()
        fh2.close()
        
        for field in C.AGENT_HEADER_IGNORE:
            # print('field is ', field)
            header.remove(field)
            
        self.agentHeader = header
        
        logfolder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logs')
        
        if not os.path.exists(logfolder):
            os.makedirs(logfolder)
        
        # setup csv log to write all agents to
        logfile = "RAOP-%s-log.csv" % datetime.now().strftime('%Y%m%d%H%M%S')
        logfile = os.path.join(logfolder, logfile)
        self.log_fh = open(logfile, 'w', newline='')
        self.log = csv.writer(self.log_fh)
        
        # write out the header row
        logHeader = ['ID', 'Gen', 'Score', 'thresh_pizza']
        for field in self.agentHeader:
            logHeader.append(threshLabel(field))
            logHeader.append(weightLabel(field))
            
        self.log.writerow(logHeader)
        
        print("Running genetic algorithm with %s agents for %s generations using data file %s" \
                % (self.numAgents, self.numGenerations, self.dataFile))

    """
    runs the genetic algorithm for self.numGenerations generations, running indefinitely if it is 0
    """
    def main(self):
        generation = None

        bestAgentOfAllGens = None
        bestAgentScore = 0

        while ((self.genNumber <= self.numGenerations or self.numGenerations == 0)
                and bestAgentScore < C.SCORE_THRESHOLD):
            # create the next generation
            generation = self.createGeneration(generation)
        
            # run against test every N number of generations
            if (self.genNumber % C.CHECK_AGAINST_TEST_AFTER_N_GENS) == 0:
                self.runGeneration(generation, test=True)
                
                # Replace best agent if this generation had a better agent
                for agent in generation:
                    if agent.score > bestAgentScore:
                        bestAgentOfAllGens = agent
                        bestAgentScore = agent.score
            
            # run the generation against train even if it was run against test
            # (agent.score will be overwritten) so we don't use the test data for training
            self.runGeneration(generation)
            
            # Replace best agent if this generation had a better agent
            for agent in generation:
                if agent.score > bestAgentScore:
                    bestAgentOfAllGens = agent
                    bestAgentScore = agent.score
            
            # save it and its results to file
            self.archiveGeneration(generation)
            
        # run against test data
        self.runAgainstTest(generation, bestAgentOfAllGens, self.testRequests)
        
        if self.kaggleFile:
            self.runAgainstTest(generation, bestAgentOfAllGens,
                                self.kaggleRequests, False)
        
        # report on results, pickAgent, etc...  
        self.archiveGeneration(generation)
        #pprint(generation)

    """
    Loops through each agent in the generation and runs Agent.scoreRequest(request) on each request.
    Calculates the accuracy/score of each agent and sets agent.score to it.
    """
    def runGeneration(self, generation, test=False):
        results = {}
        # keep track of each individual prediction by each agent 
        # so we know if they're always guessing false
        predictions = {}
    
        # pick which requests to run against
        requests = self.trainingRequests
        if test:
            requests = self.testRequests
        
        for request in requests:
            for agent in generation:
                # what does the agent think will happen
                prediction = agent.scoreRequest(request)
                
                # was it correct?
                correct = prediction == request.get('received_pizza')
                results.setdefault(agent.id, []).append(correct)
                predictions.setdefault(agent.id, []).append(prediction)
                
        # set agent.score to the percent of requests that each agent got correct
        for agent in generation:
            scores = results[agent.id]
            agent.score = len([s for s in scores if s]) / float(len(scores))
            
            # if the agent guessed more than MAX_FALSE_PERCENTAGE did not receive pizza,
            # penalize their score.  This helps combat a local maximum of guessing false
            # for every or nearly every request
            agentPredictions = predictions[agent.id]
            percentFalse = len([p for p in agentPredictions if not p]) / float(len(agentPredictions))
            if percentFalse >= C.MAX_FALSE_PERCENTAGE:
                agent.score = max(agent.score - C.TOO_MANY_FALSE_PENALTY, 0.01)
            
            
    def runAgainstTest(self, generation, bestAgentTotalRun, requests, doscore=True):
        # pick best agent
        bestAgent = None
        bestScore = 0.0
        for agent in generation:
            if agent.score > bestScore:
                bestAgent = agent
                bestScore = agent.score

        #Compare best from last generation to best of the entire run
        if bestAgent.score < bestAgentTotalRun.score:
            bestAgent = bestAgentTotalRun
            print('The best agent was not from the last generation, it was from generation %s with id %s'
                % (bestAgent.generation, bestAgent.id))
          
        if not doscore:
            fh = open('kaggle_results.csv', 'w', newline='')
            writer = csv.writer(fh)
            writer.writerow(['request_id', 'requester_received_pizza'])
    
        total = 0
        numCorrect = 0
        totalFalse = 0
        falsePositive = 0
        falseNegative = 0
        for request in requests:
            prediction = bestAgent.scoreRequest(request)
            
            #print(prediction)
            if not doscore:
                writer.writerow([request['id'], int(prediction)])
            else:
                total += 1
                if not prediction:
                    totalFalse += 1
                
                correct = prediction == request.get('received_pizza')
                
                if correct:
                    numCorrect += 1
                else:
                    if prediction:
                        falsePositive += 1
                    else:
                        falseNegative += 1
        
        if doscore:
            print('Best agent: %s' % bestAgent)
            print("Success rate: %s, %s out of %s"
                % (numCorrect/float(total), numCorrect, total))
            print("False positives: %s, false negatives: %s"
                % (falsePositive, falseNegative))
            print("Number predicted to be false: %s out of %s"
                % (totalFalse, total))
                
        
    """
    Create a new generation of self.numAgents agents.  A generation can either be an instance
    of a Generation class if we go that route, or could just be a list or dict of Agent
    objects.  If the currentGen and results arguments are passed in, this function will call self.breedGeneration(currentGen, results), otherwise it will create new Agents with random
    values for each field.
    """
    def createGeneration(self, currentGen=None):
        agents = []
        
        # increment the generation number
        self.genNumber += 1
        
        # If there is no current generation, we've just started, create random agents.
        # Otherwise breed new agents using results from the current generations.
        if currentGen:
            agents = self.breedGeneration(currentGen)
        else:
            for _ in range(self.numAgents):
                self.agentID += 1
                agents.append(Agent(self.agentID, self.genNumber, self.agentHeader))
        
        return agents

    """
    Uses the results to determine percentage chance that each Agent will be chosen as a parent.  Create numAgents new agents by calling self.breed on 2 parents numAgents times.  Then call self.mutate on each new Agent.
    """
    def breedGeneration(self, generation):
        agents = []        
        agentscores = {}
        agentsById = {}
        
        bestAgent = None
        bestScore = 0.0
        
        #getting all scores and putting into a dictionary
        #keys will be agent id's and value will agent.score
        for agent in generation:
             agentscores[agent.id] = agent.score
             agentsById[agent.id] = agent
             
             if agent.score > bestScore:
                bestAgent = agent
                bestScore = agent.score
        
        # keep the best agent as-is for the next generation
        agents.append(bestAgent)
        
        #picking a score based on it's weighted value
        def pickbasedonscoreweight(dictionary):
            sumscores = 0.0
            #random number from 0 to sum of scores
            randomnum = uniform(0, sum(dictionary.values()))
            #looping through dictionary
            for key, values in dictionary.items():
                sumscores += values
                if sumscores >= randomnum: 
                   return key
            return key
        
        #using the weightedvalue scorer to choose the key then finding which key that belongs to
        #aka finding the agent that has that id and returning it
        def selectAgent():
             key = pickbasedonscoreweight(agentscores)
             return agentsById[key]
         
        # breed the new agents, selecting parents based on their success rates
        for _ in range(self.numAgents - 1):
            agent1 = selectAgent()
            agent2 = selectAgent()
            agents.append(self.breed(agent1, agent2))
            
        # mutate generation
        for agent in agents:
            self.mutate(agent)
            
        return agents

    """
    Breed the 2 passed in Agents together to create and return a new Agent.  Use a single crossover point in the values of the 2 agents, with the first n values coming from the first agent and the rest coming from the second.
    """
    def breed(self, agent1, agent2):
        self.agentID += 1
        newValues= {}

        for key in self.agentHeader:
            x = randint(0, 1)
            if x == 0:
                newValues[weightLabel(key)] = agent1.values.get(weightLabel(key))
                newValues[threshLabel(key)] = agent1.values.get(threshLabel(key))
            else:
                newValues[weightLabel(key)] = agent2.values.get(weightLabel(key))
                newValues[threshLabel(key)] = agent2.values.get(threshLabel(key))
                
        # overall pizza thresh only has a threshold
        key = C.PIZZA
        x = randint(0, 1)
        if x == 0:
            newValues[threshLabel(key)] = agent1.values.get(threshLabel(key))
        else:
            newValues[threshLabel(key)] = agent2.values.get(threshLabel(key))
                
        return Agent(self.agentID, self.genNumber, self.agentHeader, newValues)
        
    
    """
    Loop through all of the weights and thresholds of the Agent and mutate them if a randomly generated number is less than the mutation constant (a constant for the GeneticAlgorithm that we can tweak between, but not during, runs)
    """
    def mutate(self, agent):
        for key in agent.values:
            x = randint(0, 100)
            if x < C.MUTATION_CONSTANT:
                # pizza thresh has a configurable max instead of 1
                if key == threshLabel(C.PIZZA):
                    agent.values[key] = round(uniform(0, C.MAX_PIZZA_THRESH), 2)
                else:
                    agent.values[key] = round(random(), 2)
        
    """
    Save the generation to disk in the csv log file
    """
    def archiveGeneration(self, generation):
        for agent in generation:
            agentInfo = agent.getAllInfo()
            self.log.writerow(agentInfo)
        
        self.log_fh.flush()
        
    """
    Loop through the csv reader, create a dict of data for each request, and keep it in either
    self.testRequests or self.trainingRequests depending on which it is.
    """
    def cacheRequests(self, trainreader, testreader, header):
        def readCSV(reader, type='train'):
            for line in reader:
                data = dict(zip(header, line))
                data['received_pizza'] = json.loads(data['received_pizza'])
                if type == 'test':
                    self.testRequests.append(data)
                elif type == 'train':
                    self.trainingRequests.append(data)
                else:
                    self.kaggleRequests.append(data)
					
        readCSV(trainreader, 'train')
        readCSV(testreader, 'test')
        
        if self.kaggleFile:
            fh = open(self.kaggleFile, 'r')
            kagglereader = csv.reader(fh)
            kagglereader.__next__()
            readCSV(kagglereader, 'kaggle')
            fh.close()
            
        
def usage():
    print('Usage:\nGeneticAlgorithm.py trainFile.csv testFile.csv [numTeamsPerRound] [numGenerations]')

if __name__=='__main__':
    if len(sys.argv) < 3:
        usage()
    else:
        # score data file, currently assumed to be a csv file
        dataFile = sys.argv[1]
        testFile = sys.argv[2]
		
        # how many teams per generation
        numTeams = DEFAULT_NUM_TEAMS
        if len(sys.argv) >= 4:
            numTeams = sys.argv[3]

        # how many generations to run for
        numGenerations = 0
        if len(sys.argv) >= 5:
            numGenerations = sys.argv[4]
            
        # run against Kaggle?
        kaggleFile = None
        if len(sys.argv) >= 6:
            kaggleFile = sys.argv[5]
            
        # run the genetic algorithm
        ga = GeneticAlgorithm(dataFile, testFile, numTeams,
                              numGenerations, kaggleFile)
        ga.main()
