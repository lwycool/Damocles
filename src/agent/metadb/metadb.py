#!/usr/bin/python

# This is intended to be an interface to different metadb backends.
# For now, we implement it as a sqlite3 db. No sqlalchemy etc for now.

import sqlite3

class MetaDBSession(object):

    def __init__(self, input_file_source=None):

        try:
            # First, create a sqlite db.
            #import pdb; pdb.set_trace()
            self.db_session = sqlite3.connect('/Users/vbhamidipati/damocles/blacklisted_url_db')
            # Create a single table in it for now, called "blacklisted_http_urls"
            self.db_cursor = self.db_session.cursor()
            self.db_cursor.execute('''CREATE TABLE blacklisted_http_urls(url TEXT unique)''')
            self.db_session.commit()
            # Populate the db.
            # NOTE - Canonicalize the urls?
            if input_file_source:
                # Read each url from the input file,
                # and insert into the db.
                with open(input_file_source) as f:
                    for line in f:
                        if line[-1] == '\n':
                            line = line[:-1]
                        self.db_cursor.execute('''INSERT INTO blacklisted_http_urls(url) VALUES(?)''', (line,))
                self.db_session.commit()
        except Exception, e:
            print e.message
            raise e
        # We keep the db_session open until the process quits.
        return

    #TBD
    def add_url_to_blacklist(self, url):
        pass

    def del_url_from_blacklist(self, url):
        pass