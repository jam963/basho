import networkx as nx
import networkx.algorithms as algs


class WordGraph(object):
    """
    A instance is a DiGraph of words from a set of Poems.
    """
    _g = nx.DiGraph()

    def __init__(self, poems):
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

    def write_gexf(self, name):
        """
        Writes .gexf file of the graph g
        Parameter name: the filename
        Precondition: name is a string ending in ".gexf"
        """
        nx.write_gexf(self._g, name)

    def update_betweenness(self):
        """
        """
        betweenness = algs.betweenness_centrality(self._g)
        for key in betweenness:
            self._g.nodes[key]["betweenness"] = betweenness[key]
