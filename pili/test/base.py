# -*- coding: utf-8 -*-
from pili import base
from pili import jinja2
import os
import time
#from pili.ext import webapp2

#class webapp(webapp2.RequestHandler):
#    def _all(self, *args):
#        self.response.write("_all")

#    def _request(self, handler_method):
#        self.response.write(handler_method)

class WebApp(base.Base):
    def _init(self):
        self.tpl = jinja2.create_jinja("../../tpls")
        pass

    def _index(self):
        self.tpl.assign({"data":"yoyo"})
        self.echo(self.tpl.render("index.html"))
        pass

    def a(self):
        self.echo('this is a')

    def cache(self):
        if self.tpl.is_cached('index.html') is False:
            self.tpl.assign('data', str(time.time()))
        self.echo(self.tpl.render('index.html', '', 5))
    
    def cache2(self):
        if self.tpl.is_cached('index.html') is False:
            self.tpl.assign({'data':str(time.time())})
        self.echo(self.tpl.render('index.html', cache_time=5))

def main():
    base.pilirun('/_pili/test/base', WebApp)
    #base.route(r'/test/products', handler='handlers.ProductsHandler:list_products', name='products-list')

if __name__ == "__main__":
    main()

