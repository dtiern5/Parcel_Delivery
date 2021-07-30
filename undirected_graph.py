# This class is slightly modified from zyBooks C950: Data Structures and Algorithms II Section 6.6

class UndirectedGraph:

    def __init__(self):
        self.adjacency_list = {}
        self.edge_weights = {}

    def add_vertex(self, new_vertex):
        """
        Adds a vertex to the graph. The Distance table provides addresses which we use as vertexes.
        :param new_vertex: The vertex to add
        :return: None
        Time Complexity: O(1)
        """
        self.adjacency_list[new_vertex] = []

    def add_directed_edge(self, from_vertex, to_vertex, weight):
        """
        Adds a directed edge to the graph. This is called by add_undirected_edge since the distances
        to and from addresses are identical
        :param from_vertex: Start location
        :param to_vertex: End location
        :param weight: Distance between locations
        :return: None
        Time Complexity: O(1)
        """
        self.edge_weights[(from_vertex, to_vertex)] = weight
        self.adjacency_list[from_vertex].append(to_vertex)

    def add_undirected_edge(self, vertex_a, vertex_b, weight):
        """
        Calls add_directed_edge to and from each location.
        This isn't needed with the current implementation of the application, as the
        CSV has been modified to mirror all distances for us. However, I've decided to keep
        it in the program for the future, as we may decide the time spent updating the CSV file
        to be too costly.
        :param vertex_a: First location
        :param vertex_b: Second location
        :param weight: Distance between locations
        :return:
        Time Complexity: O(1)
        """
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)
