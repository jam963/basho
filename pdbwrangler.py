"""
Some tools for dealing with poetry sourced using the PoetryDB api, whose
documentation can be found here:
https://github.com/thundercomb/poetrydb/blob/master/README.md

"""
from poem import *
import requests
import json


class PdbWrangler(object):
    """
    """

    def __init__(self):
        self._baseUrl = "https://poetrydb.org/"

    def get_poems(self, author=None, title=None, lines=None, linecount=None,
                  poemcount=None, abs=False, d=" % "):
        """
        Returns a set of Poems from poetryDataBase matching given criteria.


        author=None,
        title=None,
        lines=None,
        linecount=None,
        poemcount=None
        """
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
        poems = self._to_poem(poems_json, delim=d)
        return poems

    def get_random_poems(self, num, d=" % "):
        """
        Returns a given number of random Poems.
        """
        url = self._baseUrl + "random/" + str(num)
        poems_json = self._get_json(url)
        poems = self._to_poem(poems_json, delim=d)
        return poems

    def _to_poem(self, json_file, delim):
        """
        """
        poems = set()
        for i in json_file:
            t = i["title"]
            a = i["author"]
            lines = i["lines"]
            text = delim.join(lines)
            poem = Poem(text.lower(), author=a, title=t, delimiter=delim)
            poems.add(poem)
        return poems

    def _get_json(self, url):
        """
        """
        data = requests.get(url)
        json_data = data.json()
        return json_data
