import typing, random

T = typing.TypeVar('T')
EdgeMapping = dict[T, set[T]]

class DirectedGraph(typing.Generic[T]):
	def __init__(self, nodes: list[T]):
		self.nodes: set[T] = set(nodes)
		self.edges: EdgeMapping = {
			node: set() for node in self.nodes
		}

	def has_node(self, node: T):
		return node in self.nodes

	def has_nodes(self, *nodes: T):
		return all([
			self.has_node(node) for node in nodes
		])
	
	def num_nodes(self):
		return len(self.nodes)
	
	def __validate_all_nodes(self, *args):
		if not self.has_nodes(*args):
			s = f'all arguments must be elements of graph (args {args})'
			raise ValueError(s)

	def has_edge (self, source: T, target: T):
		self.__validate_all_nodes(source, target)
		return target in self.edges[source]

	def has_edges (self, edgelist: list[list[T]]) -> bool:
		for edge in edgelist:
			if not self.has_edge(*edge):
				return False
		return True 

	def add_edge (self, source: T, target: T) -> None:
		if target == source:
			raise ValueError('cannot add edges from self to self')
		self.edges[source].add(target)
	
	def remove_edge(self, source: T, target: T) -> bool:
		self.__validate_all_nodes(source, target)
		
		edges = self.edges[source]
		if target in edges:
			edges.remove(target)
			return True
		else: 
			return False

	def num_edges(self) -> int:
		return sum(len(self.edges[node]) for node in self.nodes)
	
	@staticmethod
	def max_edges_for_n_nodes(n: int):
		return (n-1)*n
	
	def max_edges(self):
		# dumb hack, but we want this to work for child types that may
		# override max_edges_for_n_nodes (and I got sick of trying to
		# figure out the syntax for something more elegant)
		return self.__class__.max_edges_for_n_nodes(self.num_nodes())
	
	def complete(self):
		nodes = list(self.nodes)
		for n, i in zip(nodes, range(len(nodes))):
			for m in nodes[i+1:]:
				self.add_edge(n, m)
				self.add_edge(m, n)
	
	@classmethod
	def random_graph (
		cls,
		nodes: list[T], 
		num_edges: int, 
		guaranteed_edges: list[list[T]]=[],
	):
		# optimization for later: if we're constructing an almost-complete
		# graph, start with a complete graph and then remove edges

		dg = cls(nodes)

		# it's very slow to construct a complete graph by picking random edges,
		# so if we're asking for one, just do it from the start
		#
		# this also gets us the case for graphs with zero or one nodes for
		# free
		if len(guaranteed_edges) + num_edges >= dg.max_edges():
			dg.complete()
			return dg

		for edge in guaranteed_edges:
			dg.add_edge(*edge)
		
		for i in range(num_edges):
			if dg.num_edges() == dg.num_nodes()*(dg.num_nodes()-1):
				return dg
			
			n1 = random.choice(nodes)
			n2 = random.choice(nodes)

			# guarantees we add a new, valid edge each time
			while (n1 == n2 or dg.has_edge(n1, n2)):
				n1 = random.choice(nodes)
				n2 = random.choice(nodes)

			dg.add_edge(n1, n2)

		return dg

	def adjacent_nodes(self, node) -> list[T]:
		if node in self.nodes:
			return list(self.edges[node])
		raise ValueError("node not element of graph")

__all__ = ['DirectedGraph']