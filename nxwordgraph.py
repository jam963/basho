from bgraph import bGraph
import networkx as nx
import networkx.algorithms as algs


class WordGraph(bGraph):
    """
    A instance is a DiGraph of words from a set of Poems.
    """

    def __init__(self, poems):
        super(WordGraph, self).__init__()
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

    def update_betweenness(self):
        """
        Updates betweenness centrality for all nodes in the graph.
        """
        betweenness = algs.betweenness_centrality(self._g)
        for key in betweenness:
            self._g.nodes[key]["betweenness"] = betweenness[key]
