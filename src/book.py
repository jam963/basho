import networkx.algorithms as algs
import textdistance as td
from pandas import DataFrame
from basho.src.syngraph import SynGraph


class Book(object):
    """
    A container for Poems or Poem-like objects.

    Books store these objects in a dictionary, Book.pages. Books can have
    any number or type of attribute set via keyword arguments.
    Book expects values in pages to have a "text" attribute.
    """

    def __init__(self, pages, **kwargs):
        """
        Parameter pages: the objects that go into the Book.
        Precondition: pages is a dictionary.

        Additional keyword arguments set additional Book attributes.
        """
        self.pages = {key: value for (key, value) in pages.items()}
        self.size = len(self.pages)
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def from_poems(cls, poems, by="label", **kwargs):
        """
        Initializes a Book object from an iterable of Poems.

        Parameter poems: the Poems to put in the book.
        Precondition: poems is an iterable of Poems.
        Parameter by: the poem attribute to use as a key for the pages
        dictionary.
        Precondition: by is a valid attribute for all poems in poems.
        """
        pages = {getattr(poem, by): poem for poem in poems}
        return cls(pages, **kwargs)

    def __getitem__(self, item):
        """
        """
        return self.pages[item]

    def __iter__(self):
        """
        Returns an iterator object for the pages dictionary.
        """
        return iter(self.pages)

    def keys(self):
        """
        Returns a view of the keys in the pages dictionary.
        """
        return self.pages.keys()

    def pages(self):
        """
        Returns a view of the values in the pages dictionary.
        """
        return self.pages.values()

    def items(self):
        """
        Returns a view of items in the pages dictionary.
        """
        return self.pages.items()

    def update(self, key, value):
        """
        Updates the pages dictionary with a {key: value} pair.
        """
        self.pages.update({key: value})

    def graph_edit_distance(self, exclude=None, gen=False, bound=1000, time=10):
        """

        """
        poems = {}
        if gen:
            for key, poem in self.pages.items():
                poem.gen_sg()
        if exclude:
            for key, value in self.pages.items():
                if getattr(value, exclude[0]) != exclude[1]:
                    poems.update({key: value})
        else:
            poems = self.pages
        dist = {"Labels": []}
        summary = {"Nodes": [], "Edges": []}
        for key, poem in poems.items():
            dist["Labels"].append(key)
            steps = {key: []}
            summary["Nodes"].append(poem.get_num_nodes())
            summary["Edges"].append(poem.get_num_edges())
            for i, j in poems.items():
                if i == key:
                    steps[key].append(0)
                else:
                    ged = algs.graph_edit_distance(poem.sg.get_graph(),
                                                   j.sg.get_graph(),
                                                   upper_bound=bound,
                                                   timeout=time)
                    steps[key].append(ged)
            dist.update(steps)
        summary.update({"Labels": dist["Labels"]})
        dist_frame = DataFrame(data=dist)
        dist_frame.set_index("Labels")
        summary_frame = DataFrame(data=summary)
        summary_frame.set_index("Labels")
        return [dist_frame, summary_frame]







    def get_distance(self, alg="jaccard"):
        """
        Returns a pandas DataFrame of of pairwise
        textdistance comparisons for all elements of pages.
        """
        pass

    def df(self, attribute):
        """
        """
        pass
