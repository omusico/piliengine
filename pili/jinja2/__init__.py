from pili.ext import jinja2
from pili.ext.jinja2 import Environment,FileSystemLoader
from pili.ext.jinja2.python_loader import PythonLoader
from pili.ext.jinja2 import jinjafilter

class create_jinja:
    """Rendering interface to Jinja2 Templates
    Example:
        render= render_jinja('templates')
        render.hello(name='jinja2')
    """

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
        self._lookup.filters.update({'urlencode':jinjafilter.urlencode})

    def add_filter(filters):
        self._lookup.filters.update(filters)

    def assign(self, data):
        self._data.update(data)

    def render(self, tpl, data=None):
        if data is not None:
            self.assign(data)
        return self._lookup.get_template(tpl).render(self._data)

