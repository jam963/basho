

class Book(object):
    """
    A container for Poems or Poem-like objects.

    Books store these objects in a dictionary, Book.pages. Books can have
    any number or type of attribute set via keyword arguments.
    """

    def __init__(self, pages, **kwargs):
        """
        Parameter pages: the objects that go into the Book.
        Precondition: pages is a dictionary.

        Additional keyword arguments set additional Book attributes.
        """
        self.pages = pages
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
