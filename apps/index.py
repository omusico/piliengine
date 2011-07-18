# -*- coding: utf-8 -*-

import pili

class my_stock(pili.base):

    def _allx(self, *args):
        return args

    def _index(self):
        self.echo(web.ctx.env)
        return 'hello world'

    def _default(self):
        return '_default'

    def report(self,*args):
        return 'this is report at /my/stock/report/' + str(args)

    def noParam(self):
        return 'noParam'

    def paramMin1Max1(self, k):
        return (k)

    def paramMin0Max1(self, k=3):
        return (k)

    # 2,3
    def paramMin2Max3(self, k, g, b=4):
        return (k,g,b)
        pass

    def paramMin1Max3(self, k, g=2, b=3):
        return (k,g,b)

    def parmUnlimit(self, *args):
        return args

pili.go(globals(), ('/my/stock/{simple_route}','my_stock'))
#pili.go(globals(), ('/my/stock/{simple_route:10}','my_stock'))
#pili.go(globals(), ('/my/stock/?([^/]+)?/?([^/]+)?/?([^/]+)?/?([^/]+)?/?','my_stock'))
#pili.go(globals(), ('/my/stock/?(abc|def)?/?(\d+)?','my_stock'))


