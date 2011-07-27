# -*- coding: utf-8 -*-

from pili import base
#from pili.ext import webapp2

#class webapp(webapp2.RequestHandler):
#    def _all(self, *args):
#        self.response.write("_all")

#    def _request(self, handler_method):
#        self.response.write(handler_method)

class WebApp(base.Base):
    def _init(self):
        pass

    def _index(self):
        pass

    def a(self):
        self.echo('hihih')

"""
app = webapp2.WSGIApplication([
    webapp2.Route(r"%s/<:(\w+)>/?" % prefix, webapp, handler_method='_request'),
    #webapp2.Route(r"/_pili/test/base/", webapp, name="name", handler_method="_all"),
    webapp2.Route(r"%s.*" % prefix, webapp, name="all", handler_method="_all"),
    ])
"""

def main():
    base.pilirun('/_pili/test/base', WebApp)
    #base.route(r'/test/products', handler='handlers.ProductsHandler:list_products', name='products-list')

if __name__ == "__main__":
    main()

