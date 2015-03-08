# This module will contain functionality to train agents genetically

import sys
import csv
from pprint import pprint

from Agent import Agent

AGENT_HEADER_IGNORE = ['request_id', 'request_type', 'received_pizza']
DEFAULT_NUM_TEAMS = 30


class GeneticAlgorithm(object):
    genNumber = 0
    agentID = 999
    
    trainingRequests = []
    testRequests = []

    """
    Set up the genetic algorithm. Set the number of agents, number of generations,
    and agent fields.  Also get all of the pizza requests into memory.
    """
    def __init__(self, dataFile, numAgents=DEFAULT_NUM_TEAMS, numGenerations=0):
        self.dataFile = dataFile
        self.numAgents = int(numAgents)
        self.numGenerations = int(numGenerations)
        
        fh = open(self.dataFile, 'r')
        reader = csv.reader(fh)
        header = reader.next()
        self.cacheRequests(reader, header)
        fh.close()
        
        for field in AGENT_HEADER_IGNORE:
            header.remove(field)
            
        self.agentHeader = header
        
        print "Running genetic algorithm with %s agents for %s generations using data file %s" \
                % (self.numAgents, self.numGenerations, self.dataFile)

    """
    runs the genetic algorithm for self.numGenerations generations, running indefinitely if it is 0
    """
    def main(self):
        generation = self.createGeneration()
        while self.genNumber <= self.numGenerations or self.numGenerations == 0:
            self.runGeneration(generation)
            #self.archiveGeneration(generation)
            generation = self.createGeneration(generation)
            
        # run against test data
        self.runGeneration(generation)
        
        # report on results, pickAgent, etc...  
        # TODO: implement this part
        pprint(generation)

    """
    Loops through each agent in the generation and runs Agent.scoreRequest(request) on each request.  Keeps track of the accuracy of the results in a datastructure or db entry and returns them.
    """
    # TODO: implement
    def runGeneration(self, generation, training=True):
        results = {}
    
        requests = self.trainingRequests
        if not training:
            requests = self.testRequests
            
        for request in requests:
            for agent in generation:
                prediction = agent.scoreRequest(request)
                correct = prediction == request.get('received_pizza')
                
                results.setdefault(agent.id, []).append(correct)
                
        #for agent in generation:
        #    score = 
        #    agent.score = 
                
        return []
        
    """
    Create a new generation of self.numAgents agents.  A generation can either be an instance
    of a Generation class if we go that route, or could just be a list or dict of Agent
    objects.  If the currentGen and results arguments are passed in, this function will call self.breedGeneration(currentGen, results), otherwise it will create new Agents with random
    values for each field.
    """
    def createGeneration(self, currentGen=None, results=None):
        self.genNumber += 1
        self.agentID += 1
        agents = []
        
        for _ in range(self.numAgents):
            if currentGen:
                agent = self.breedGeneration(currentGen, results)
            else:
                agent = Agent(self.agentID, self.genNumber, self.agentHeader)
                
            agents.append(agent)
        
        return agents

    """
    Uses the results to determine percentage chance that each Agent will be chosen as a parent.  Create numAgents new agents by calling self.breed on 2 parents numAgents times.  Then call self.mutate on each new Agent.
    """
    # TODO: implement
    def breedGeneration(self, generation, results):
        return Agent(self.agentID, self.genNumber, self.agentHeader)

    """
    Breed the 2 passed in Agents together to create and return a new Agent.  Use a single crossover point in the values of the 2 agents, with the first n values coming from the first agent and the rest coming from the second.
    """
    # TODO: implement
    def breed(self, agent1, agent2):
        pass
    
    """
    Loop through all of the weights and thresholds of the Agent and mutate them if a randomly generated number is less than the mutation constant (a constant for the GeneticAlgorithm that we can tweak between, but not during, runs)
    """
    # TODO: implement
    def mutate(self, agent):
        pass
        
    def cacheRequests(self, reader, header):
        for line in reader:
            data = dict(zip(header, line))
            if data.get('request_type') == 'test':
                self.testRequests.append(data)
            else:
                self.trainingRequests.append(data)

def usage():
    print 'Usage:\nGeneticAlgorithm.py dataFile.csv [numTeamsPerRound] [numGenerations]'

if __name__=='__main__':
    if len(sys.argv) < 3:
        usage()
    else:
        # score data file, currently assumed to be a csv file
        dataFile = sys.argv[1]
        
        # how many teams per generation
        numTeams = DEFAULT_NUM_TEAMS
        if len(sys.argv) == 3:
            numTeams = sys.argv[2]
            
        # how many generations to run for
        numGenerations = 0
        if len(sys.argv) == 4:
            numGenerations = sys.argv[3]
        
        # run the genetic algorithm
        ga = GeneticAlgorithm(dataFile, numTeams, numGenerations)
        ga.main()
    