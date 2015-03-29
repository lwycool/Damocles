#!/usr/bin/python

# Implementation of trie shamelessly lifted from:
# https://reterwebber.wordpress.com/2014/01/22/data-structure-in-python-trie/

class Trie(object):

    def __init__(self, *trie_strings):
        self.trie = {}

    def is_in_trie(self, trie_string):
        # Return true or false
        # based on whether the trie
        # contains the string or not.

        # Assume we're getting valid strings.
        temp_trie = self.trie
        for letter in trie_string:
            if letter not in temp_trie:
                return False
            temp_trie = temp_trie[letter]

        if  "_end_" in temp_trie:
            return True
        else:
            return False

    def add_to_trie(self, trie_string):
        print "in add_to_trie, trie_string is " + str(trie_string)
        #import pdb; pdb.set_trace()
        temp_trie = self.trie
        for letter in trie_string:
            temp_trie = temp_trie.setdefault(letter, {})
        temp_trie = temp_trie.setdefault('_end_', '_end_')


    #TBD
    def remove_from_trie(self, trie_string):
        pass