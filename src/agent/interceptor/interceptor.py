#!/usr/bin/env python

# Intended to be a full fledged daemon/*nix service.
# For now, will be simple code that will start,
# load a file of malicious urls, populate
# the MetaCache, and look it up whenever
# it encounters a URL.

from src.agent.metacache import http_metacache
from src.agent.metacache import tcp_metacache
from src.agent.metacache import https_metacache
from src.agent.metadb import metadb

SUPPORTED_URL_PROTOCOLS = ['http', 'https']

class DamoclesInterceptor(object): 

    def process_url(self, url):
        # First, get the URL's protocol.
        url_protocol = url.split("://")[0].lower()
        if url_protocol not in SUPPORTED_URL_PROTOCOLS:
            print "Unsupported protocol %s found, treating as blacklisted" % url_protocol
            return True
        # Else, check in the protocol's metacache.
        if url_protocol == 'http':
            metacache = self.http_metacache
        elif url_protocol == 'https':
            metacache = self.https_metacache
        # TBD: Handle other protocols later.

        # Now, check with metacache, whether this url is blacklisted.
        return metacache.is_url_blacklisted(url)

    def init_all_metacaches(self):
        # Initialize metacaches for HTTP/TCP/HTTPS
        # Note, we don't actually put in anything into these caches now,
        # for efficiency.
        self.http_metacache = http_metacache.HttpMetaCache(self.blacklist_source_session)
        self.https_metacache = https_metacache.HttpsMetaCache(self.blacklist_source_session)
        self.tcp_metacache = tcp_metacache.TcpMetaCache(self.blacklist_source_session)


    def __init__(self, init_file="/etc/damocles/damocles_agent.ini"):
        # First, read in all config from a file.
        # For now, we simply hardcode these.
        # self.load_init_params(init_file)

        # Open a session to the source of blacklist entries.
        blacklist_url_file = '/Users/vbhamidipati/damocles/blacklist_url_list'
        self.blacklist_source_session = metadb.MetaDBSession(blacklist_url_file)

        # Initializes all its components.
        self.init_all_metacaches()
        # we're done for now.

def main():
    damoclesi = DamoclesInterceptor()
    # Now, run the "source" that gives us HTTP URLs to check against.
    # For now, just open a file and read from it.
    input_file = '/Users/vbhamidipati/damocles/input_url_list'
    blacklisted_url_list = []
    with open(input_file) as f:
        for url in f:
            print "Read in url from input file : %s " % url
            # Remove the newline at the end of the url
            if url[-1] == '\n':
                url = url[:-1]
            is_blacklisted = damoclesi.process_url(url)
            print "blacklisted url %s : %s " % (url, is_blacklisted)
            if is_blacklisted:
                blacklisted_url_list.append(url)
    # At the end, print out the list.
    print "\n Printing blacklisted URLs below: \n"
    for url in blacklisted_url_list:
        print url + "\n"





