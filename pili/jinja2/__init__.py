from jinja2 import Environment,FileSystemLoader
from python_loader import PythonLoader
import jinjafilter

from google.appengine.api import memcache

"""
tpl = jinja2.create_jinja("../../tpls")
tpl.assign({"name":"pili engine"})
self.response.write(tpl.render("index.html"))
"""
class create_jinja:

    def __init__(self, *a, **kwargs):
        self._data = {}
        extensions = kwargs.pop('extensions', [])
        globals = kwargs.pop('globals', {})

        self._lookup = Environment(loader=PythonLoader(*a, **kwargs), extensions=extensions)
        self._lookup.globals.update(globals)

        #now is not available to use byteccode cache
        #from jinja2.bccache import MemcachedBytecodeCache
        #from google.appengine.api import memcache
        #self._render._lookup.bytecode_cache = MemcachedBytecodeCache(memcache, self.config.CACHE_KEY_PREFIX)

        #add useful filters
        self._lookup.filters.update({'urlencode':jinjafilter.__dict__['urlencode']})

    # add filter/modifier
    # tpl.add_filter({'urlencode':urlencode_func})
    def add_filter(filters):
        self._lookup.filters.update(filters)

    # tpl.assign({"name":"pili"})
    # tpl.assign("name", "pili")
    def assign(self, *args):
        if len(args) == 1:
            self._data.update(data)
        elif len(args) == 2:
            self._data[args[0]] = args[1]

    # once cache_time set, cache will be enable
    # template directory and template file construct a cache key by default
    # you appened extra cache_key to determine different data
    def render(self, tpl, data=None, cache_time=None, cache_key=None):
        if data is not None:
            self.assign(data)
        return self._lookup.get_template(tpl).render(self._data)

