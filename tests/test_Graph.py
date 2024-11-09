from .context import models
Graph = models.graph.Graph 
import unittest

class GraphCanBeInitialized(unittest.TestCase):
	def test_Initialize(self):
		self.dg = Graph([1, 2, 3, 4, 5])
		assert self.dg
		assert self.dg.num_nodes() == 5
		assert self.dg.num_edges() == 0

	def test_InitializeEmptyGraph(self):
		self.dg = Graph([])
		assert self.dg
		assert self.dg.num_nodes() == 0
		assert self.dg.num_edges() == 0

	def test_initialize_random_graph(self):
		g: Graph = Graph.random_graph([1, 2, 3, 4, 5], 3, [
			[1, 2],
			[3, 4]
		])

		assert g.has_edges([[1, 2], [3, 4], [2, 1], [4, 3]])
		assert g.num_edges() == 5
		assert g.num_nodes() == 5

class GraphCanAddEdges(unittest.TestCase):
	def setUp(self):
		self.dg: Graph = Graph([1, 2, 3, 4, 5])

	def test_CanAddEdges(self):
		assert self.dg.num_edges() == 0
		self.dg.add_edge(1, 2)

		assert self.dg.num_edges() == 1
		assert self.dg.has_edge(1, 2)
		assert self.dg.has_edge(2, 1)

		self.dg.add_edge(2, 1)
		assert self.dg.num_edges() == 1
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
		assert self.dg.has_edge(1, 2)
		assert self.dg.has_edge(2, 1)

		self.dg.add_edge(2, 3)
		assert self.dg.num_edges() == 2
		assert self.dg.has_edge(2, 3)
		assert self.dg.has_edge(1, 2)

		self.dg.add_edge(1, 3)
		assert self.dg.num_edges() == 3
		assert self.dg.has_edge(1, 3)

class GraphCanRemoveEdges(unittest.TestCase):
	def setUp(self):
		self.dg = Graph([1, 2, 3, 4, 5])
		self.dg.add_edge(1, 2)

	def test_CanRemoveEdges(self):
		assert self.dg.has_edge(1, 2)

		self.dg.remove_edge(1, 2)
		assert not self.dg.has_edge(1, 2)
		assert not self.dg.has_edge(2, 1)
		assert self.dg.num_edges() == 0

		self.dg.add_edge(1, 2)
		self.dg.add_edge(1, 3)
		assert self.dg.num_edges() == 2

		self.dg.remove_edge(1, 2)
		assert self.dg.has_edge(1, 3)
		assert not self.dg.has_edge(1, 2)
		assert not self.dg.has_edge(2, 1)
		assert self.dg.num_edges() == 1
		assert self.dg.num_nodes() == 5	

	def test_RepeatedAddAndRemove(self):
		self.dg.remove_edge(2, 1)
		assert not (self.dg.has_edge(2, 1) or self.dg.has_edge(1, 2))
		self.dg.add_edge(1, 2)
		assert (self.dg.has_edge(2, 1) and self.dg.has_edge(1, 2))
		self.dg.remove_edge(1, 2)
		assert not (self.dg.has_edge(2, 1) or self.dg.has_edge(1, 2))

class GraphCanGetConnectedSubgraphs(unittest.TestCase):
	def setUp(self):
		self.num_nodes: int = 10
		self.g: Graph = Graph(range(self.num_nodes))

	def test_empty_graph_case (self):
		self.g = Graph([])
		assert len(self.g.connected_subgraphs()) == 1

	def test_five_tuple_case (self):
		g = self.g
		num_nodes = self.num_nodes

		for n in range(0, num_nodes-1, 2):
			g.add_edge(n, n+1)
		
		connected_subgraphs: list[Graph] = g.connected_subgraphs()
		assert len(connected_subgraphs) == max((num_nodes // 2), (num_nodes+1)//2)

		for cg, i in zip(connected_subgraphs, range(1, num_nodes-1, 2)):
			assert cg.num_nodes() == 2 # will fail for odd numbers
			assert cg.num_edges() == 1
			assert cg.has_edge(i, i-1)
			try:
				assert not cg.has_edge(i, i+1)
			except:
				continue
	
	def test_spoke_case (self):
		g = self.g 
		num_nodes = self.num_nodes

		for i in range(num_nodes-1):
			g.add_edge(i, num_nodes-1)

		connected_subgraphs = g.connected_subgraphs()
		assert len(connected_subgraphs) == 1
		assert connected_subgraphs[0].num_edges() == self.num_nodes-1

	def test_tree_case (self):
		g = self.g
		num_nodes = self.num_nodes

		for i in range(num_nodes):
			child = (2*i)+1
			if (child) < num_nodes:
				g.add_edge(child, i)
			child+=1
			if (child) < num_nodes:
				g.add_edge(child, i)
			
		assert g.num_edges() == num_nodes-1
		connected_subgraphs = g.connected_subgraphs()
		assert (len(connected_subgraphs)) == 1
		assert (connected_subgraphs[0].num_edges() == g.num_edges())

	def test_multiple_groups (self):
		g = self.g
		num_nodes = self.num_nodes

		for i in reversed(range(1, num_nodes-1)):
			g.add_edge(i, i+1)

		connected_subgraphs = g.connected_subgraphs()
		assert len(connected_subgraphs) == 2
		assert connected_subgraphs[0].num_nodes() == 1
		assert connected_subgraphs[0].num_edges() == 0
		assert connected_subgraphs[1].num_nodes() == num_nodes-1
		assert connected_subgraphs[1].num_edges() == num_nodes-2

	def test_circular_graph (self):
		g = Graph([1, 2, 3])
		g.add_edge(1, 2)
		g.add_edge(2, 3)
		g.add_edge(1, 3)
		assert len(g.connected_subgraphs()) == 1

	def test_barbell_graph (self):
		num_nodes = 7
		g = Graph(range(num_nodes))

		for i in range(num_nodes-1):
			g.add_edge(i, i+1)

		g.add_edge(0, 2)
		g.add_edge(4, 6)

		assert len(g.connected_subgraphs()) == 1

	def test_three_cycles (self):
		num_nodes = 9
		g = Graph(range(num_nodes))

		for i in range(3):
			n = 3*i
			g.add_edge(n, n+1)
			g.add_edge(n, n+2)
			g.add_edge(n+1, n+2)

		connected_subgraphs = g.connected_subgraphs()
		assert len(connected_subgraphs) == 3
		for graph in connected_subgraphs:
			assert graph.num_edges() == 3
			assert graph.num_nodes() == 3

class GraphCanMergeSubgraphs(unittest.TestCase):
	def check_merge (num_nodes: int, edgelist: list[list[int]]):
		g = Graph(range(num_nodes))
		for edge in edgelist:
			g.add_edge(*edge)

		num_subgraphs = len(g.connected_subgraphs())

		g.merge_subgraphs()

		assert len(g.connected_subgraphs()) == 1

		if num_subgraphs <= 1:
			assert g.num_edges() == len(edgelist)
		else:
			assert g.num_edges() > len(edgelist)

		assert g.num_nodes() == num_nodes

		assert g.has_edges(edgelist)


	def test_can_merge_barbell(self):
		# initial graph:
		#   0         4
		#  / \   3   / \
		# 1 - 2     5 - 6
		GraphCanMergeSubgraphs.check_merge(7, 
			[
				[0, 1],
				[0, 2],
				[1, 2],
				[4, 5],
				[4, 6],
				[5, 6],
			]
		)
	
	def test_can_merge_empty_graph(self):
		GraphCanMergeSubgraphs.check_merge(0, [])

	def test_can_merge_lines(self):
		edgelist = [[1,0],[3,2],[5,4],[7,6],[9,8]]
		num_nodes = 10
		GraphCanMergeSubgraphs.check_merge(
			num_nodes, edgelist
		)

	def test_can_merge_singleton(self):
		num_nodes = 2
		edgelist = [[0, 1]]
		GraphCanMergeSubgraphs.check_merge(num_nodes, edgelist)

	def test_can_merge_singlets(self):
		GraphCanMergeSubgraphs.check_merge(5, [])
	

if __name__ == '__main__':
	unittest.main()