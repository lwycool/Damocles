#!/usr/bin/python

# This provides a Trie implementation of a bucket
# for a set of URLs - without the https://fqdn:port
# in them.

from src.agent.lib import trie

class UrlBucket(object):

    def __init__(self):
        # Initialize an empty trie.
        self.url_trie = trie.Trie()


    def add_url_to_bucket(self, pared_url):
        # Add the url to the trie
        # if it isn't already there.
        self.url_trie.add_to_trie(pared_url)
        print "Added " + pared_url + " to trie"
        print "**********"
        print "Printing trie below:"
        print self.url_trie.trie
        print "**********"


    def remove_url_from_bucket(self, pared_url):
        # Remove the url from the trie
        # if it isn't already not there.
        pass

    def is_url_in_bucket(self, pared_url):
        return self.url_trie.is_in_trie(pared_url)

