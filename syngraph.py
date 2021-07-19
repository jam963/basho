from bgraph import bGraph
from nltk.corpus import wordnet as wn
import re


class SynGraph(bGraph):
    """
    A graph of words based on synsets. The graph is either hypernymic (by
    default) or hyponimic, i.e. edges represent words that share
    hypo/hypernyms.
    """

    def __init__(self, poem, hyp=True, regex=r"\W+"):
        """
        Initializer for the SynGraph class.

        Parameter poem: the Poem from which to construct the SynGraph.
        Precondition: poem is a valid Poem object.
        Parameter hyp: True if the SynGraph is hypernymic (default) or
        hyponymic.
        Parameter regex: A regular expression or function to be applied to the
        Poem's words.
        Precondition: regex is a valid regular expression or function to be
        passed to re.sub().
        """
        super(SynGraph, self).__init__()
        self._syn_word = {}
        for word in poem.get_words():
            # Remove non-alphanumeric chars from words except for those
            # specified in nonalpha.
            w = re.sub(regex, "", word)
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
                    self._hyp_adder(syn, w, self._g, self._syn_word, hyp)

    def _hyp_adder(self, syn, word, graph, dict, h):
        """
        A helper function for the initializer.

        h is True for hypernyms, False for hyponyms.
        """
        if h:
            hy = syn.hypernyms()
        else:
            hy = syn.hyponyms()
        for nym in hy:
            if nym not in dict:
                dict.update({nym: {word}})
            else:
                others = dict[nym]
                for other in others:
                    if other != word:
                        graph.add_edge(word, other, synset=nym.name())
                dict[nym].add(word)

    def get_syns(self):
        """
        Returns a dictionary of {synset: [word]} pairs for the SynGraph.
        """
        return self._syn_word

    def get_syn_count(self):
        """
        Returns a dictionary of {synset: [count]} pairs, where synset is a
        string representation of a synset in the SynGraph, and count is
        the length of the list of words associated with that synset.
        """
        syn_counts = {}
        for key, value in self._syn_word:
            syn_counts.update({key.name(): [len(value)]})
        return syn_counts

    def get_syn_frac(self):
        """
        Returns a dictionary of {synset: [fraction]} pairs, where synset is a
        string representation of a synset in the SynGraph, and fraction is the
        length of the list of words associated with that synset divided by the
        total number of nodes in the graph.
        """
        syn_counts = {}
        for key, value in self._syn_word:
            frac = len(value)/self.get_num_nodes()
            syn_counts.update({key.name(): [frac]})
        return syn_counts
