from .context import models
DirectedGraph = models.graph.DirectedGraph
import unittest

class DirectedGraphCanBeInitialized(unittest.TestCase):
	def test_Initialize(self):
		self.dg = DirectedGraph([1, 2, 3, 4, 5])
		assert self.dg
		assert self.dg.num_nodes() == 5
		assert self.dg.num_edges() == 0

	def random_graph_assertions(nodes: list, num_edges: int, guaranteed_edges: list[list]=[]):
		expected_nodes = len(nodes)
		expected_edges = len(guaranteed_edges)+num_edges

		if expected_edges > ((expected_nodes-1)*expected_nodes):
			expected_edges = (expected_nodes-1)*expected_nodes

		dg: DirectedGraph = DirectedGraph.random_graph(nodes, num_edges, guaranteed_edges=guaranteed_edges)
		
		assert dg.has_edges(guaranteed_edges)

		for node in nodes:
			assert node in dg.nodes
		
		assert dg.num_edges() == expected_edges
		assert dg.num_nodes() == expected_nodes

	def test_random_graph(self):
		DirectedGraphCanBeInitialized.random_graph_assertions(
			[1, 2, 3, 4, 5],
			2,
			guaranteed_edges=[[1, 2]]
		)

	def test_random_complete_graph(self):
		nodes = [1, 2, 3, 4]
		edgelist = [
			[1, 2], [1, 3], [1, 4], 
			[2, 3], [2, 4], [3, 4],
			[4, 3], [4, 2], [4, 1],
			[3, 2], [3, 1], [2, 1]
		]

		DirectedGraphCanBeInitialized.random_graph_assertions(nodes, 0, guaranteed_edges=edgelist)
		DirectedGraphCanBeInitialized.random_graph_assertions(nodes, 5, guaranteed_edges=edgelist)

	def test_random_empty_graph(self):
		nodelist = []
		DirectedGraphCanBeInitialized.random_graph_assertions(nodelist, 0)


class DirectedGraphCanAddEdges(unittest.TestCase):
	def setUp(self):
		self.dg: DirectedGraph = DirectedGraph([1, 2, 3, 4, 5])

	def test_CanAddEdges(self):
		assert self.dg.num_edges() == 0
		self.dg.add_edge(1, 2)

		assert self.dg.num_edges() == 1
		assert self.dg.has_edge(1, 2)
		assert not self.dg.has_edge(2, 1)

		self.dg.add_edge(2, 1)
		assert self.dg.num_edges() == 2
		assert self.dg.has_edge(2, 1)
		assert self.dg.has_edge(1, 2)

	def test_BadNodeRaisesError(self):
		try:
			self.has_edge(2, 3)
			assert False # exception not raised
		except:
			assert True # exception raised

	def test_CanAddSeveralEdges(self):
		self.dg.add_edge(1, 2)
		assert self.dg.num_edges() == 1

		self.dg.add_edge(2, 3)
		assert self.dg.num_edges() == 2

		self.dg.add_edge(1, 3)
		assert self.dg.num_edges() == 3

class DirectedGraphCanRemoveEdges(unittest.TestCase):
	def setUp(self):
		self.dg: DirectedGraph = DirectedGraph([1, 2, 3, 4, 5])
		self.dg.add_edge(1, 2)

	def test_CanRemoveEdges(self):
		assert self.dg.has_edge(1, 2)

		self.dg.remove_edge(1, 2)
		assert not self.dg.has_edge(1, 2)
		assert self.dg.num_edges() == 0

		self.dg.add_edge(1, 2)
		self.dg.add_edge(1, 3)
		assert self.dg.num_edges() == 2

		self.dg.remove_edge(1, 2)
		assert self.dg.has_edge(1, 3)
		assert not self.dg.has_edge(1, 2)
		assert self.dg.num_edges() == 1
		assert self.dg.num_nodes() == 5	

	def test_RemovingEdgeReturnsCorrectBools(self):
		assert not self.dg.remove_edge(1, 3)

		assert self.dg.remove_edge(1, 2)
		assert not self.dg.remove_edge(2, 1)

		self.dg.add_edge(2, 1)
		assert self.dg.remove_edge(2, 1)
		assert not self.dg.remove_edge(2, 1)

class DirectedGraphCanAddObjects(unittest.TestCase):
	def test_InitializingObjectGraph(self):
		self.dg = DirectedGraph(
			[DirectedGraph([1, 2, 3]), DirectedGraph([1])]
		)
	

if __name__ == '__main__':
	unittest.main()