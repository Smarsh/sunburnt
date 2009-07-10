from __future__ import absolute_import

import cgi
import urllib

import httplib2
from lxml.builder import ElementMaker
from lxml import etree
import simplejson

h = httplib2.Http(".cache")
E = ElementMaker()

def force_utf8(s):
    if isinstance(s, str):
        return s
    else:
        return s.encode('utf-8')


class SolrException(Exception):
    pass


class SolrConnection(object):
    def __init__(self, url):
        self.url = url.rstrip("/") + "/"
        self.update_url = self.url + "update/"
        self.select_url = self.url + "select/"

    def add(self, docs):
        self.update(self._make_update_doc(docs))

    def update(self, update_doc):
        body = force_utf8(update_doc)
        headers = {"Content-Type":"text/xml; charset=utf-8"}
        r, c = h.request(self.update_url, method="POST", body=body,
                         headers=headers)
        if r.status != 200:
            raise SolrException(r, c)

    def select(self, **kwargs):
        kwargs['wt'] = 'json'
        qs = urllib.urlencode(kwargs)
        url = "%s?%s" % (self.select_url, qs)
        r, c = h.request(url)
        if r.status != 200:
            raise SolrException(r, c)
        return simplejson.loads(c)

    @staticmethod
    def _make_update_doc(docs):
        if hasattr(docs, "items"):
            docs = [docs]
        xml = E.add(*[
                E.doc(*[
                        E.field({'name':k}, v)
                        for k, v in doc.items()])
                      for doc in docs])
        return etree.tostring(xml, encoding='utf-8')


s = SolrConnection("http://localhost:8983/solr")
s.add({"key1":"value1", "key2":"value2"})
print s.select(q="solr")
