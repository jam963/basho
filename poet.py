"""
Generates text in the style of a poet from a provided seed.

To create more variety in the results without altering the engine's parameters,
a random selection of poems are taken from a corpus and passed to OpenAI whenever
generate() is called. This also reduces costs.
"""
import openai
import os
import json
import random
from poem import Poem


class Poet(object):
    """
    A Poet that can write poems in a given style using OpenAI's api.

    OpenAI can be financially expensive, so individual examples used in the corpus should be kept short. However,
    since the generate() method samples examples from the corpus, the corpus itself can
    be as large as needed. OpenAI doesn't seem to need too many examples (in some cases,
    more examples seem to return worse results). Default OpenAI parameter values are hardcoded here,
    since these have produced the best results so far.
    """

    openai.api_key = os.getenv("OPENAI_API_KEY")

    def __init__(self, header, corpus, engine="davinci", temp=0.75, max_len=64,
                 tp=0.7, freq_pen=0.6, pres_pen=0.6):
        """
        Initializer for the Poet class.

        This initializes a Poet.

        Parameter header: A short description of what the Poet will write.
        Precondition: header is a string (preferably a short one, such as "Writes
        haikus in the style of Basho"
        Parameter corpus: A json file composed of (label, poem) pairs, where poems have
        lines separated by "/".
        Precondition: corpus is a valid json file.
        Parameter engine: The OpenAI engine to use to generate the poem.
        Precondition: engine is a valid engine.
        Parameter temp: temperature parameter for OpenAI
        Precondition: temp is a float between 0.0 and 1.0.
        Parameter max_len: The maximum number of tokens to be generated by OpenAI.
        Precondition: max_len is a float (preferably a small one, to reduce costs).
        Paramter tp: tp is the top_p paramter for OpenAI.
        Precondition: tp is a float between 0.0 and 1.0.
        Paramter freq_pen: freq_pen is the frequency_penalty parameter for OpenAI.
        Precondition: freq_pen is a float between 0.0 and 1.0.
        Paramter pres_pen: pres_pen is the presence_penalty paramter for OpenAI.
        Precondition: pres_pen is a float between 0.0 and 1.0.
        """
        self._header = header + "\n\n"
        with open(corpus) as json_file:
            self._corpus = json.load(json_file)
        self._engine = engine
        self._temp = temp
        self._max_len = max_len
        self._tp = tp
        self._freq_pen = freq_pen
        self._pres_pen = pres_pen

    # Getters and setters
    def get_header(self):
        return self._header

    def get_corpus(self):
        return self._corpus

    def get_engine(self):
        return self._engine

    def get_temp(self):
        return self._temp

    def get_max_len(self):
        return self._max_len

    def get_tp(self):
        return self._tp

    def get_freq_pen(self):
        return self._freq_pen

    def get_pres_pen(self):
        return self._pres_pen

    def set_header(self, header):
        """
        Parameter header: header is the new header (a short description of what the engine
        is to do)
        Precondition: header is a one-sentence or shorter string
        """
        self._header = header

    def set_corpus(self, corpus):
        """
        Parameter corpus: A json file of label, poem pairs.
        Precondition: corpus is a valid json file.
        """
        with open(corpus) as json_file:
            self._corpus = json.load(json_file)

    def set_engine(self, engine):
        """
        Parameter engine: an OpenAI engine. Refer to the OpenAI documentation for more info.
        Precondition: engine is a valid OpenAI engine (as a string)
        """
        self._engine = engine

    def set_temp(self, temp):
        """
        Parameter temp: the temperature parameter for the engine.
        Precondition: temp is a float between 0.0 and 1.0
        """
        self._temp = temp

    def set_max_len(self, ml):
        """
        Parameter ml: the maximum length (in tokens) of the generated text.
        Precondition: ml is an int < 2048 (bearing in mind financial costs of longer texts)
        """

        self._max_len = ml

    def set_tp(self, tp):
        """
        Parameter tp: tp is the top_p paramter for OpenAI.
        Precondition: tp is a float between 0.0 and 1.0.
        """
        self._tp = tp

    def set_freq_pen(self, fp):
        """
        Parameter fp: freq_pen is the frequency_penalty parameter for OpenAI.
        Precondition: freq_pen is a float between 0.0 and 1.0.
        """
        self._freq_pen = fp

    def set_pres_pen(self, pp):
        """
        Parameter pp: pres_pen is the presence_penalty paramter for OpenAI.
        Precondition: pres_pen is a float between 0.0 and 1.0.
        """
        self._pres_pen = pp

    def generate(self, size, seed):
        """
        Returns a poem (with the poem's lines separated by "/") as a string.

        This method will generate OpenAI Completion output. The poem has an leading space
        and ends in "\n", which is a little annoying, but easily remedied later.

        Parameter size: The number of examples to be sampled from the corpus.
        Precondition: size is an int less than the size of the corpus.
        Parameter seed: a word used to generate the poem.
        Precondition: seed is a (one or two word) string.
        """
        p = self.build_prompt(size, self._corpus, self._header) + "Seed: " + seed + "\nPoem:"
        response = openai.Completion.create(
           engine=self._engine,
           prompt=p,
           temperature=self._temp,
           max_tokens=self._max_len,
           top_p=self._tp,
           frequency_penalty=self._freq_pen,
           presence_penalty=self._pres_pen,
           stop=["###"]
         )
        return response.choices[0]["text"]

    def generate_poem(self, size, seed):
        """
        """
        text = self.generate(size, seed)
        return Poem(text)

    def random_keys(self, size, dict):
        """
        Returns a list of pseudorandom keys from a provided dictionary of a given
        number of labeled examples of poems.

        Parameter size: the number of examples to be sampled from the corpus.
        Precondition: size is an int, where 0 <= size < corpus.size().
        Parameter dict: the corpus to be sampled.
        Precondition: dict is a dictionary of labeled examples which are (preferably)
            short in length, to reduce financial costs.
        """
        corpus_keys = list(dict.keys())
        sample_keys = []
        while len(sample_keys) < size:
            key_ix = random.randint(0, len(corpus_keys)-1)
            if corpus_keys[key_ix] not in sample_keys:
                sample_keys.append(corpus_keys[key_ix])
        return sample_keys

    def build_prompt(self, size, dict, header):
        """
        Builds a prompt for OpenAI given a corpus of labeled examples.

        Parameter size: the number of examples to be sampled from a given corpus.
        Precondition: size is a positive int < the size of dict.
        Parameter dict: a corpus of labeled examples.
        Precondition: dict is a dictionary composed of (key, value) pairs of examples,
            which are strings (preferably short ones).
        Parameter header: header is a brief description of the poems to be generated.
        Precondition: header is a string (a short one) ending in two trailing "\n".
        """
        sample_keys = self.random_keys(size, dict)
        prompt = header
        for key in sample_keys:
            prompt += "Seed: {}\nPoem: {}\n###\n".format(key, dict[key])
        return prompt
