#!/usr/bin/python

from src.agent.metacache import metacache
from src.agent.lib import urlbucket

class HttpsMetaCache(metacache.MetaCache):

    def __init__(self, blacklist_source_session):
        super(HttpsMetaCache, self).__init__(blacklist_source_session)
        self.metacache = {}
        self.protocol = "https"


    def get_fqdn_from_url(self, url):
        return url.split("://")[1].split("/")[0]


    def fqdn_has_port(self, fqdn):
        # The fqdn is either like
        # <dnsName> or <dnsName>:<port>
        if len(fqdn.split(":")) == 2:
            return True
        else:
            return False


    def pare_url(self, url, fqdn_key):
        return url[len(fqdn_key)+1:]

    def is_url_in_bucket(self, url):
        # The url is a complete URL.
        # Search metacache for the fqdn key.
        # Then search in the bucket.
        fqdn = self.get_fqdn_from_url(url)
        fqdn_key = self.prepare_fqdn_key(fqdn)
        bucket = self.metacache[fqdn_key]
        if not bucket:
            return False
        return bucket.is_url_in_bucket(self.pare_url(url, fqdn_key))


    def is_url_blacklisted(self, url):
        # First, extract the fqdn and port.
        fqdn = self.get_fqdn_from_url(url)
        # Create this fqdn's bucket in the
        # metacache - this is idempotent.
        # NOTE - change this later, I don't like this,
        # it's confusing. Just put a check if it exists
        # and create it if it doesn't.
        self.create_fqdn_bucket(fqdn)
        # Now that we have created the bucket,
        # query it for this url.
        ##import pdb; pdb.set_trace()
        return self.is_url_in_bucket(url)


    def prepare_fqdn_key(self, fqdn):
        if not self.fqdn_has_port(fqdn):
            # Use 80, we're http.
            # Don't append a / at the end.
            # We'll treat that as part of the
            # rest of the URL.
            # NOTE: How much effect will doing
            # that have on the trie in the bucket?
            fqdn_key = self.protocol + "://" + fqdn + ":80"
        else:
            fqdn_key = self.protocol + "://" + fqdn
        return fqdn_key


    def print_metacache(self):
        ##import pdb; pdb.set_trace()
        for key in self.metacache.keys():
            print "key: " + str(key) + " Value: " + str(self.metacache[key].url_trie.trie)


    def create_fqdn_bucket(self, fqdn):
        fqdn_key = self.prepare_fqdn_key(fqdn)
        # Check if metacache already has this key.
        if fqdn_key in self.metacache:
            # Just return. We're good.
            return
        else:
            # Create it.
            print "\nCreating bucket for %s" % fqdn_key
            self.metacache[fqdn_key] = urlbucket.UrlBucket()
            # Populate the bucket with all blacklisted URLs
            # gleaned from the metadb for this fqdn_key
            blacklisted_urls_for_fqdn_key = self.metadb_session.db_cursor.execute('''SELECT url from blacklisted_http_urls where url like ? ''', (fqdn_key+'%',))
            for row in blacklisted_urls_for_fqdn_key:
                # row[0] gives us the url.
                url = row[0]
                print "Read in url from db: " + url
                # strip the fqdn_key from the url before adding
                # it to the bucket.
                url_in_bucket = self.pare_url(url, fqdn_key)
                print "url_in_bucket is: " + str(url_in_bucket)
                self.metacache[fqdn_key].add_url_to_bucket(url_in_bucket)
                # TDB: CHECK FOR CORNER CASES LIKE when the url is just http://blah.blah/.
        # At this stage, the metacache contains the key and the bucket with trie filled up with the malicious URLs.
        # Our job here is done.
        print "After populating the bucket for fqdnkey " + fqdn_key + " , printing metacache below:"
        self.print_metacache()