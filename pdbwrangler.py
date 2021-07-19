"""
Some tools for dealing with poetry sourced using the PoetryDB api, whose
documentation can be found here:
https://github.com/thundercomb/poetrydb/blob/master/README.md

"""
from poem import Poem
import requests


class PdbWrangler(object):
    """
    This class provides a straightforward way to deal with the PoetryDB api.
    """
    def __init__(self):
        self._baseUrl = "https://poetrydb.org/"

    def get_poems(self, author=None, title=None, lines=None, linecount=None,
                  poemcount=None, abs=False, d=" % "):
        """
        Returns a set of Poems from poetryDataBase matching given criteria.

        Parameter author: The author of a poem (the author must be present
        in the poetrydb database)
        Precondition: author is a string.
        Parameter title: A word or words present in the title of a poem
        Precondition: title is a string
        Parameter lines: A word or words present in the lines of a poem.
        Precondition: lines is a string.
        Parameter linecount: The number of lines of a poem.
        Precondition: linecount is an int.
        Parameter poemcount: The number of poems to return from poetrydb.
        Precondition: poemcount is an int.
        Parameter abs: True if all parameters should be matched exactly. Refer
        to the poetrydb api docs for more on how abs is handled.
        """
        self._d = d
        args = {"author": author, "title": title, "lines": lines,
                "linecount": linecount, "poemcount": poemcount}
        input = []
        search = []
        for key in args:
            if args[key] is not None:
                input.append(key)
                if abs:
                    search.append(args[key]+":abs")
                else:
                    search.append(args[key])
        input = ','.join(input)
        search = ';'.join([str(x) for x in search])
        url = self._baseUrl + input + '/' + search
        poems_json = self._get_json(url)
        poems = self._to_poem(poems_json)
        return poems

    def get_random_poems(self, num, d=" % "):
        """
        Returns a set of a given number of random Poems.

        Parameter num: The number of random poems to return.
        Precondition: d is an int.
        Parameter d: The delimiter to use between lines in the Poems.
        Precondition: d is a string.
        """
        self._d = d
        url = self._baseUrl + "random/" + str(num)
        poems_json = self._get_json(url)
        poems = self._to_poem(poems_json)
        return poems

    def _to_poem(self, json_file):
        """
        Converts Json from poetrydb into a set of Poem objects.

        Parameter json_file: The Json file to convert.
        Precondition: json_file is a valid Json file generated by poetrydb
        Parameter delim: The character(s) to place between lines in each poem.
        Precondition: delim is a string.
        """
        poems = set()
        for i in json_file:
            t = i["title"]
            a = i["author"]
            lines = i["lines"]
            text = self._d.join(lines)
            poem = Poem(text.lower(), author=a, title=t, delimiter=self._d)
            poems.add(poem)
        return poems

    def _get_json(self, url):
        """
        A helper function for fetching json data from poetrydb.
        """
        data = requests.get(url)
        json_data = data.json()
        return json_data
