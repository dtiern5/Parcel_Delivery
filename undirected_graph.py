
# Class is slightly modified from Section 6.6 of ZyBooks
class UndirectedGraph:

    # Time complexity: O(1)
    # Space complexity: O(1)
    def __init__(self):
        self.adjacency_list = {}
        self.edge_weights = {}

    # Time complexity: O(1)
    # Space complexity: O(1)
    def add_vertex(self, new_vertex):
        self.adjacency_list[new_vertex] = []

    # Time complexity: O(1)
    # Space complexity: O(1)
    def add_directed_edge(self, from_vertex, to_vertex, weight):
        self.edge_weights[(from_vertex, to_vertex)] = weight
        self.adjacency_list[from_vertex].append(to_vertex)

    # Time complexity: O(1)
    # Space complexity: O(1)
    def add_undirected_edge(self, vertex_a, vertex_b, weight):
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)

