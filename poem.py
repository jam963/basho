import networkx as nx
import networkx.algorithms as algs
from nxwordgraph import WordGraph
from syngraph import SynGraph


class Poem:
    """
    Each instance represents a Poem from a corpus. Poems have text, which is composed
    of individual words. The text has a length (in words) and a number of lines.
    One can define an author, title, and/or label, as well as a line delimiter
    (default is " % "). Poem's constructor expects poem text to have lines
    delimited by "/"
    """

    def __init__(self, text, author=None, title=None, label=None,
                 delimiter=" % "):
        """
        Parameter text: the text of a poem from a corpus.
        Precondition: text is a string, where line breaks in a poem are
                      indicated by "/" or " % "
        Parameter author (optional): The author of the Poem.
        Precondition: author is a string.
        Parameter title (optional): The title of the Poem.
        Precondition: title is a string.
        Parameter label (optional): A label for the Poem.
        Precondition: label is a string.
        """
        self.text = text.replace("/", delimiter).lower()
        self._words = self.text.split()
        self._length = len(self._words)
        self._lines = self.text.count(delimiter) + 1
        self._density = None
        self._num_nodes = None
        self._cycles = []
        self._num_cycles = None
        self.author = author
        self.title = title
        self.label = label
        self.sg = None
        self.wg = None

    def get_text(self):
        return self.text

    def get_words(self):
        return self._words

    def get_length(self):
        return self._length

    def get_sg(self):
        if self._sg is None:
            raise Exception("SynGraph for this poem does not exist.")
        return self._sg

    def get_wg(self):
        if self._wg is None:
            raise Exception("WordGraph for this Poem does not exist.")
        return self._wg

    def get_author(self):
        return self.author

    def get_title(self):
        return self.title

    def get_label(self):
        return self.label

    def get_cycles(self):
        return self._cycles

    def get_num_cycles(self):
        return self._num_cycles

    def get_density(self):
        if self._wg is None:
            raise Exception("WordGraph for this Poem does not exist.")
        return self._density

    def get_num_nodes(self):
        if self._num_nodes is None:
            raise Exception("WordGraph for this Poem does not exist.")
        return self._num_nodes

    def num_lines(self):
        return self._lines

    def set_author(self, author):
        self.author = author

    def set_title(self, title):
        self.title = title

    def set_label(self, label):
        self.label = label

    def gen_wg(self):
        """
        Generate a WordGraph of the Poem.
        """
        selfset = {self}
        self._wg = WordGraph(selfset)
        self._num_nodes = nx.number_of_nodes(self._wg.get_graph())
        self._density = nx.density(self._wg.get_graph())

    def gen_sg(self, nym=True):
        """
        Generate a SynGraph of the Poem.

        Parameter nym: Whether the SynGraph is heteronymic (True) or hyponymic
        (False).
        Precondition: nym is a bool.
        """
        self._sg = SynGraph(self, nym)

    def update_cycles(self):
        """
        Updates the number of cycles in the Poem's WordGraph. Raises an
        Exception if a WordGraph for the Poem does not exist.
        """
        if self._wg is None:
            raise Exception("WordGraph for this Poem does not exist.")
        cycle_generator = algs.simple_cycles(self._wg.get_graph())
        for i in cycle_generator:
            self._cycles.append(i)
        self._num_cycles = len(self._cycles)

    def betweenness(self, syn=True, normal=True):
        """
        Returns a dictionary of betweenness centrality for all nodes in _g.

        Parameter syn: True for betweenness of the Poem's SynGraph, False for
        WordGraph.
        Precondition: syn is a bool.
        Parameter normal: Whether betweenness is normalized.
        Precondition: normal is a bool.
        """
        if syn:
            if self._sg is None:
                raise Exception("SynGraph for this Poem does not exist.")
            return algs.betweenness_centrality(self._sg.get_graph(),
                                               normalized=normal)
        else:
            if self._wg is None:
                raise Exception("WordGraph for this Poem does not exist.")
            return algs.betweenness_centrality(self._wg.get_graph(),
                                               normalized=normal)
