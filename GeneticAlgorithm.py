# This module will contain functionality to train agents genetically

import sys
import csv
import json
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
        # create initial generation
        generation = self.createGeneration()
        
        while self.genNumber <= self.numGenerations or self.numGenerations == 0:
            # run it
            self.runGeneration(generation)
            
            # save it and its results to file
            self.archiveGeneration(generation)
            
            # create the next generation
            generation = self.createGeneration(generation)
            
            
        # run against test data
        self.runGeneration(generation, False)
        
        # report on results, pickAgent, etc...  
        # TODO: implement this part
        pprint(generation)

    """
    Loops through each agent in the generation and runs Agent.scoreRequest(request) on each request.
    Calculates the accuracy/score of each agent and sets agent.score to it.
    """
    def runGeneration(self, generation, training=True):
        results = {}
    
        # pick which requests to run against
        requests = self.trainingRequests
        if not training:
            requests = self.testRequests
        
        for request in requests:
            for agent in generation:
                # what does the agent think will happen
                prediction = agent.scoreRequest(request)
                
                # was it correct?
                correct = prediction == request.get('received_pizza')
                results.setdefault(agent.id, []).append(correct)
                
        # set agent.score to the percent of requests that each agent got correct
        for agent in generation:
            scores = results[agent.id]
            agent.score = len([s for s in scores if s]) / float(len(scores))
        
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
        self.agentID += 1
        
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
    # TODO: implement
    def breedGeneration(self, generation):
        agents = []
        
        # TODO: get the scores from all of the agents and put them in a data structure
        #       that makes it easy to select parents based on their scores
        # something like this maybe: http://stackoverflow.com/questions/2570690/python-algorithm-to-randomly-select-a-key-based-on-proportionality-weight
        parents = {}
        # TODO: implement, Note: the parents variable is visible in the scope of this function
        def selectAgent():
            return None
        
        # breed the new agents, selecting parents based on their success rates
        for _ in range(self.numAgents):
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
    # TODO: implement
    def breed(self, agent1, agent2):
        self.agentID += 1
        return Agent(self.agentID, self.genNumber, self.agentHeader)
    
    """
    Loop through all of the weights and thresholds of the Agent and mutate them if a randomly generated number is less than the mutation constant (a constant for the GeneticAlgorithm that we can tweak between, but not during, runs)
    """
    # TODO: implement
    def mutate(self, agent):
        pass
        
    """
    Save the generation to disk or db in whatever way we decide to store them
    """
    # TODO: implement
    def archiveGeneration(self, generation):
        pass
        
    """
    Loop through the csv reader, create a dict of data for each request, and keep it in either
    self.testRequests or self.trainingRequests depending on which it is.
    """
    def cacheRequests(self, reader, header):
        for line in reader:
            data = dict(zip(header, line))
            data['received_pizza'] = json.loads(data['received_pizza'])
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
    