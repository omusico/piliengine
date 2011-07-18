# -*- coding: utf-8 -*-
import pili

class my(pili.base):
    def _index(self):
        return 'my index'

    def a(self):
        echo('this is a')

    #def _all(self, *args):
    #    return 'this is super all'

    def _default(self, *args):
        echo('not found page')

pili.go(globals(), [('/my/*{simple_route}', my)])
#pili.go(globals(), [('/my/', my)])

