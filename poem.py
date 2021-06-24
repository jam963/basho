class Poem:
    """
    Each instance represents a Poem from a corpus. Poems have text, which is composed
    of individual words. The text has a lenghth (in words) and a number of linesself.

    More attributes may be added to Poem later (rhetorical devices, statistical properties,
    etc.).
    """

    def __init__(self, text):
        """
        Parameter text: the text of a poem from a corpus.
        Precondition: text is a string, where line breaks in a poem are indicated by "/"
        """
        self._text = text.replace("/", " % ")
        self._words = self._text.split()
        self._length = len(text)
        self._lines = self._text.count("\n") + 1

    def get_text(self):
        return self._text

    def get_words(self):
        return self._words

    def get_length(self):
        return self._length

    def num_lines(self):
        return self._lines
