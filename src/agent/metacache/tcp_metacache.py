#!/usr/bin/python

from src.agent.metacache import metacache

class TcpMetaCache(metacache.MetaCache):

    def __init__(self, blacklist_source_session):
        super(TcpMetaCache, self).__init__(blacklist_source_session)
        self.metacache = {}