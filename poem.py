from nxwordgraph import *
import networkx as nx
import networkx.algorithms as algs


class Poem:
    """
    Each instance represents a Poem from a corpus. Poems have text, which is composed
    of individual words. The text has a lenghth (in words) and a number of lines.
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
        self._text = text.replace("/", delimiter)
        self._words = self._text.split()
        self._length = len(self._words)
        self._lines = self._text.count(delimiter) + 1
        self._author = author
        self._title = title
        self._label = label
        self._wg = None
        self._density = None
        self._num_nodes = None
        self._cycles = []
        self._num_cycles = None

    def get_text(self):
        return self._text

    def get_words(self):
        return self._words

    def get_length(self):
        return self._length

    def get_wg(self):
        if self._wg is None:
            raise Exception("WordGraph for this Poem does not exist.")
        return self._wg

    def get_graph(self):
        if self._wg is None:
            raise Exception("WordGraph for this Poem does not exist.")
        return self._wg.get_graph()

    def get_author(self):
        return self._author

    def get_title(self):
        return self._title

    def get_label(self):
        return self._label

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
        self._author = author

    def set_title(self, title):
        self._title = title

    def set_label(self, label):
        self._label = label

    def gen_wg(self):
        """
        Generate a WordGraph of the Poem.
        """
        selfset = {self}
        self._wg = WordGraph(selfset)
        self._num_nodes = nx.number_of_nodes(self._wg.get_graph())
        self._density = nx.density(self._wg.get_graph())

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
