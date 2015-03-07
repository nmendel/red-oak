# This module will contain functionality to train agents genetically

import sys
import csv

from Agent import Agent

AGENT_HEADER_IGNORE = ['request_id', 'request_type']
DEFAULT_NUM_TEAMS = 30


class GeneticAlgorithm(object):
	genNumber = 0
	agentID = 999

	def __init__(self, dataFile, numAgents=DEFAULT_NUM_TEAMS, numGenerations=0):
		self.dataFile = dataFile
		self.numAgents = int(numAgents)
		self.numGenerations = int(numGenerations)
		
		fh = open(self.dataFile, 'r')
		reader = csv.reader(fh)
		header = reader.next()
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
			results = self.runGeneration(generation)
			generation = self.createGeneration(generation, results)
			
		# TODO: run against test data
		# report on results, pickAgent, etc...	

	"""
	Loops through each agent in the generation and runs Agent.scoreRequest(request) on each request.  Keeps track of the accuracy of the results in a datastructure or db entry and returns them.
	"""
	# TODO: implement
	def runGeneration(self, generation):
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
				agent = Agent(self.agentID, self.agentHeader)
				
			agents.append(agent)
		
		return agents

	"""
	Uses the results to determine percentage chance that each Agent will be chosen as a parent.  Create numAgents new agents by calling self.breed on 2 parents numAgents times.  Then call self.mutate on each new Agent.
	"""
	# TODO: implement
	def breedGeneration(self, generation, results):
		return Agent(self.agentID, self.agentHeader)

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


def usage():
	print 'Usage:\nGeneticAlgorithm.py dataFile.csv [numTeamsPerRound] [numGenerations]'

if __name__=='__main__':
	if len(sys.argv) < 3:
		usage()
	else:
		dataFile = sys.argv[1]
		
		numTeams = DEFAULT_NUM_TEAMS
		if len(sys.argv) == 3:
			numTeams = sys.argv[2]
			
		numGenerations = 0
		if len(sys.argv) == 4:
			numGenerations = sys.argv[3]
		
		ga = GeneticAlgorithm(dataFile, numTeams, numGenerations)
		ga.main()
	