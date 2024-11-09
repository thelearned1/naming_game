import typing
import random
from . import DirectedGraph

T = typing.TypeVar('T')
EdgeMapping = dict[T, set[T]]

class Graph(DirectedGraph):
	def __init__(self, nodes):
		super().__init__(nodes)

	def add_edge (self, node1: T, node2: T) -> None:
		super().add_edge(node1, node2)
		super().add_edge(node2, node1)
	
	def remove_edge(self, source: T, target: T) -> bool:
		return (
			super().remove_edge(source, target) and
			super().remove_edge(target, source)
		)

	def num_edges(self):
		return super().num_edges() // 2
	
	def __construct_connected_subgraph(self, node):
		node_stack = list()
		seen_nodes = set()
		node_stack.append(node)

		while(node_stack):
			curr = node_stack.pop()
			seen_nodes.add(curr)
			for adjacent_node in self.edges[curr]:
				if adjacent_node not in seen_nodes:
					node_stack.append(adjacent_node)

		g = Graph(list(seen_nodes))

		for node in seen_nodes:
			for adjacency in self.edges[node]:
				g.add_edge(node, adjacency)

		return g
	
	def connected_subgraphs(self):
		if self.num_nodes() == 0:
			return [ Graph(list()) ]
		
		seen_nodes: set[T] = set()
		graphs: list[Graph] = list()

		for node in self.nodes:
			if node not in seen_nodes:
				g = self.__construct_connected_subgraph(node)
				graphs.append(g)
				for subgraph_node in g.nodes:
					seen_nodes.add(subgraph_node)
		
		return graphs
	
	def merge_subgraphs(self):
		connected_subgraphs = self.connected_subgraphs()
		working_subgraphs = list(connected_subgraphs)
		while (len(working_subgraphs) > 1):
			subgraph1 = working_subgraphs.pop()
			subgraph2 = random.choice(working_subgraphs)
			self.add_edge(
				random.choice(list(subgraph1.nodes)),
				random.choice(list(subgraph2.nodes))
			)		

	def max_edges_for_n_nodes(n: int):
		return (n*(n-1)) // 2
__all__ = ["Graph"]
