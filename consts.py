"""
Constants for bashobot.
"""
import os

# Discord bot token
TOKEN = os.getenv("BASHOBOT_TOKEN")

# Prefix that summons the bot
PREFIX = "--"

# A header that describes what kind of poems the Poet writes
HEADER = "Writes haikus in the style of Basho"

# The corpus from which poems are sampled. See poets.py for more information.
CORPUS = "basho_corpus.json"

# Number of poems to be sampled. An int. (larger numbers are more financially expensive)
SIZE = 5
