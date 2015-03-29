#!/usr/bin/python

# Base class of all metacache types.
from src.agent.metadb import metadb

class MetaCache(object):
    def __init__(self, mdb_session):
        self.metadb_session = mdb_session

