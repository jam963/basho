import networkx as nx
from node import *


class WordGraph(object):
    """
    A instance is a graph of words from a set of Poems.
    """

    def __init__(self, poems):
        self._g = nx.DiGraph()
        for p in poems:
            words = p.get_words()
            for i in range(len(words)):
                if i == 0:
                    if words[i] not in self._g:
                        self._g.add_node(words[i], occurrences=1)
                    else:
                        self._g.nodes[words[i]]["occurrences"] += 1
                else:
                    if words[i] not in self._g:
                        self._g.add_node(words[i], occurrences=1)
                        self._g.add_edge(words[i-1], words[i], weight=1)
                    else:
                        self._g.nodes[words[i]]["occurrences"] += 1
                        if words[i-1] in self._g.predecessors(words[i]):
                            self._g.edges[words[i-1], words[i]]["weight"] += 1
                        else:
                            self._g.add_edge(words[i-1], words[i], weight=1)

    def get_graph(self):
        return self._g

    def get_gexf(self, name):
        """
        Returns a .gexf file of the graph g
        Parameter name: the filename
        Precondition: name is a string ending in ".gexf"
        """
        nx.write_gexf(self._g, name)
