
from random import random
from pprint import pprint
 
class Agent(object):

	"""
	Create a new instance of Agent using values for its weights and thresholds if it is passed in, otherwise using random values.
	"""
	def __init__(self, id, header, values={}):
		self.id = id
		self.fields = header
		
		if values == {}:
			values = self.generateValues()
		
		self.values = values
		
		#pprint("New Agent: %s" % values)
		
	"""
	create randomized values for all weights and thresholds
	"""
	def generateValues(self):
		values = {}
		for field in self.fields:
			values['%s_weight' % field] = round(random(), 2)
			values['%s_thresh' % field] = round(random(), 2)
		
		return values
		
	"""
	Scores a request based on the request's values and the agent's values and returns a boolean on whether the Agent thinks the request will be pizza'd
	"""
	# TODO: implement
	def scoreRequest(self, request):
		return true
	

"""
returns an instance of an Agent given its ID in the datastore (how this is done is obviously dependent on how our datastore works).  In other words, look up values in the db and return Agent(values).
"""
# TODO: might not be necessary
def initAgent(agentID):
	pass

