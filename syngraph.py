"""
A module for creating graphs based on WordNet synsets.
"""

from nltk.corpus import wordnet as wn
import networkx as nx
import re


class SynGraph(object):
    """
    A graph of words based on synsets. The graph is either hypernymic (by
    default) or hyponimic, i.e. edges represent words that share either an
    element of their synset and/or hypo/hypernyms.
    """
    _dict = {}
    _g = nx.Graph()

    def __init__(self, poem, hyp=True):
        """
        Initializer for the SynGraph class.

        Parameter poem: the Poem from which to construct the SynGraph.
        Precondition: poem is a valid Poem object.
        Parameter hyp: True if the SynGraph is hypernymic (default) or
        hyponymic.

        """
        for word in poem.get_words():
            # Remove non-alphanumeric chars from words
            w = re.sub(r"\W+", "", word)
            # Do not create nodes for empty strings
            # For non-empty words, add all synsets associated with the word
            # to the graph _g. For duplicate synsets, update occurrences.
            if w != '':
                syns = wn.synsets(w)
                if w not in self._g:
                    self._g.add_node(w, occurrences=1)
                else:
                    self._g.nodes[w]["occurrences"] += 1
                for syn in syns:
                    if syn not in self._dict:
                        self._dict.update({syn: {w}})
                    else:
                        others = self._dict[syn]
                        for other in others:
                            if other != w:
                                self._g.add_edge(w, other, synset=syn.name())
                        self._dict[syn].add(w)
                    self._hyp_adder(syn, w, self._g, self._dict, hyp)

    def _hyp_adder(self, syn, word, graph, dict, h):
        """
        A helper function for the initializer.

        h is True for hypernyms, False for hyponyms.
        """
        if h:
            hy = syn.hypernyms()
        else:
            hy = syn.hyponyms()
        for h in hy:
            if h not in dict:
                dict.update({h: {word}})
            else:
                others = dict[h]
                for other in others:
                    if other != word:
                        graph.add_edge(word, other, synset=h.name())
                dict[h].add(word)
