
import csv
from random import random, uniform
from pprint import pprint
 
import Constants as C


 
class Agent(object):


    score = -1

    """
    Create a new instance of Agent using values for its weights and thresholds if it is passed in, otherwise using random values.
    """
    def __init__(self, id, generation, header, values={}):
        self.id = id
        self.fields = header
        self.generation = generation
        
        if values == {}:
            values = self.generateValues()
        
        self.values = values
        self.maxScore = self.getMaxScore()
        
        #pprint("New Agent: %s" % values)
    
    # How agents are represented in interactive prompt
    def __repr__(self):
        return "<Agent id:%s gen:%s score:%s vals:%s>" \
            % (self.id, self.generation, self.score, self.values)

    # How agents are represented when printing
    def __str__(self):
        return "<Agent id:%s gen:%s score:%s vals:%s>" \
            % (self.id, self.generation, self.score, self.values)
        
    """
    Return all of the agent's information in a list.  Used to write out agents to csv files.
    """
    def getAllInfo(self):
        vals = [self.id, self.generation, self.score, self.values[threshLabel(C.PIZZA)]]
        for field in self.fields:
            vals.append(self.values[weightLabel(field)])
            vals.append(self.values[threshLabel(field)])
            
        return vals
        
    """
    create randomized values for all weights and thresholds
    """
    def generateValues(self):
        values = {}
        for field in self.fields:
            values['%s_%s' % (field, C.WEIGHT)] = round(random(), 2)
            values['%s_%s' % (field, C.THRESH)] = round(random(), 2)
            
        values[threshLabel(C.PIZZA)] = round(uniform(0, C.MAX_PIZZA_THRESH), 2)
        
        return values
	
    """
    Loop through self.values and get 
    """
    def getMaxScore(self):
        maxScore = 0.0
        for key, value in self.values.items():
            if key.endswith('_' + C.WEIGHT):
                maxScore += value
        
        return maxScore
	
    """
    Scores a request based on the request's values and the agent's values and returns a boolean on whether the Agent thinks the request will be pizza'd
    """
    def scoreRequest(self, request, returnPercent=False):
        totalScore = 0.0
        numKeys = 0
                
        for key, value in request.items():
            if key in C.AGENT_HEADER_IGNORE:
                continue
                
            value = float(value)
            numKeys += 1
            thresh = self.values.get(threshLabel(key), 1)
            weight = self.values.get(weightLabel(key), 0)
            
            if value >= thresh:
                totalScore += weight # value * weight
        
        SCORE_MULTIPLIER = 4
        finalScore = SCORE_MULTIPLIER * (totalScore / float(numKeys))
        
        if returnPercent:
            return min(finalScore, 1.0)
            
        # requestScore = (totalScore / self.maxScore)
        receivesPizza = finalScore >= (SCORE_MULTIPLIER * self.values[threshLabel(C.PIZZA)])
        
        #print('Final Score: %s, %s, %s, %s' \
        #    % (finalScore, requestScore, self.values['pizza_thresh'], receivesPizza))
        
        return receivesPizza
        
    
def weightLabel(key):
    return '%s_%s' % (key, C.WEIGHT)

def threshLabel(key):
    return '%s_%s' % (key, C.THRESH)
    
def deserializeAgentFromLog(logfile, id):
    fh = open(logfile, 'r')
    reader = csv.reader(fh)
    header = reader.__next__()
    
    for agent in reader:
        if agent[0] == str(id):
            break
    
    for field in ['ID', 'Gen', 'Score']:
        header.remove(field)
    
    return deserializeAgent(header, agent)
    
def deserializeAgent(header, agent):
    id = agent[0]
    gen = agent[1]
    
    # remove non-scoring fields from agent and header
    agent = agent[3:]
    
    # convert agent scoring fields from strings to floats
    agent = [float(v) for v in agent]
    values = dict(zip(header, agent))

    return Agent(id, gen, header, values)

