import networkx as nx


class bGraph(object):
    """
    A base class for other graphs. Has useful getters, setters, and other
    functions common to other graphs. Ideally, this would be a subclass of
    nx.Graph(), but it is not (yet).
    """

    def __init__(self):
        """
        Initializes an empty networkx undirected Graph.
        """
        self._g = nx.Graph()

    def get_graph(self):
        return self._g

    def get_nodes(self):
        """
        Returns a view of the nodes in the Graph.
        """
        return self._g.nodes

    def get_edges(self):
        """
        Returns the edges of the Graph.
        """
        return self._g.edges

    def write_gexf(self, name):
        """
        Writes .gexf file of the graph to the folder "gephi"

        Parameter name: the filename or path
        Precondition: name is a string ending in ".gexf"
        """
        nx.write_gexf(self._g, "gexf/"+name)

    def get_num_nodes(self):
        """
        Returns the number of nodes in the Graph.
        """
        return self._g.number_of_nodes()

    def is_directed(self):
        """
        Return True if the graph is directed, False otherwise.
        """
        return self._g.is_directed()
