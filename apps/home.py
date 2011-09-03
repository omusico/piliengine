from pili import base
from pili import jinja2
from pili.ext import webapp2

import os
import time

class WebApp(base.Base):
    def _init(self):
        pass

    def _index(self):
        self.response.write('this is index')

    def test(self,*args):
        self.response.write('this is test')

    # conflict name
    def echo_(self, *args):
        self.echo(args)

app = webapp2.WSGIApplication(base.create_simple_route('', WebApp))
def main():
    app.run()

if __name__ == "__main__":
    main()

