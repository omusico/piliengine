from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import time

class MainPage(webapp.RequestHandler):
    def get(self,a='default'):
        #self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!'+str(time.time()))

application = webapp.WSGIApplication([('/webapp/(.*)/?$', MainPage)], debug=True)
#application = webapp.WSGIApplication([('/webapp', MainPage)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
