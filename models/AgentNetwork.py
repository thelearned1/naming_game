from .Agent import Agent
from .graph import Graph
import random

class AgentNetwork:
	def __str__(self):
		return (''+
			'====== Adjacencies: ======\n'+
			str(self._graph)+'\n'+ 
			'========= Agents: ========\n'+
			'\n'.join([str(agent) for agent in self.agents])
		)
	def __init__(self, agents: list[Agent], min_edge_coeff: float, max_edge_coeff: float):
		self.agents = agents
		max_edges = Graph.max_edges_for_n_nodes(len(agents))
		target_edges = round(max_edges*random.uniform(min_edge_coeff, max_edge_coeff))

		# construct a random graph with approximately target_edges
		self._graph = Graph.random_graph(
			agents,
			target_edges
		)

		# add the minimum number of edges to make a connected graph
		self._graph.merge_subgraphs()

	def random_neighbor(self, agent) -> Agent:
		return random.choice(self._graph.adjacent_nodes(agent))
	
	def random_agent(self) -> Agent:
		return random.choice(self.agents)
	
__all__ = [ 'AgentNetwork' ]