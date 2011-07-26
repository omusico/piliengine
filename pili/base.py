# -*- coding: utf-8 -*-
import re
import types
import inspect

from pili.ext import webapp2
#from pili import lite

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

        from jinja2 import Environment,FileSystemLoader
        from pily.python_loader import PythonLoader
        self._lookup = Environment(loader=PythonLoader(*a, **kwargs), extensions=extensions)
        self._lookup.globals.update(globals)

        #now is not available to use byteccode cache
        #from jinja2.bccache import MemcachedBytecodeCache
        #from google.appengine.api import memcache
        #self._render._lookup.bytecode_cache = MemcachedBytecodeCache(memcache, self.config.CACHE_KEY_PREFIX)

        #add useful filters
        from pily import jinjafilter
        self._lookup.filters.update({'urlencode':jinjafilter.urlencode})

    def add_filter(filters):
        self._lookup.filters.update(filters)

    def assign(self, data):
        self._data.update(data)

    def render(self, tpl, data=None, ctx=False):
        if data is not None:
            self.assign(data)
        if ctx:
            self.assign({'ctx':web.ctx})
        return self._lookup.get_template(tpl).render(self._data)

"""
    def __getattr__(self, name):
        # Assuming all templates end with .html
        path = name + '.html'
        t = self._lookup.get_template(path)
        return t.render
"""

"""

    def _initial_renderer(self):
        self._render=render_jinja(self.tpl)

    def render(self, name, data={}):
        data.update({"ctx":web.ctx})
        return self._render.__getattr__(name)(data)

"""

class Base(webapp2.RequestHandler):
    _method = ''
    
    def __init__(self, request, response):
        super(Base,self).__init__(request, response)
        self._init()

    def _init(self):
        pass

    def create_renderer(self, tpl_path=None):
        return create_jinja(tpl_path)

    """
    def _add_filter
        #add filters
        from pily import jinjafilter
        self._render._lookup.filters.update({
            "hl_url":jinjafilter.hl_url,
            "linebreaks": jinjafilter.linebreaks,
            "urlencode": jinjafilter.urlencode, 
            'pathname2url': jinjafilter.pathname2url,
            })
    """

    def post(self, *args):
        self._method = 'post'
        self._request(*args)

    def get(self, *args):
        self._method = 'get'
        self._request(*args)

    def _index(self, *args):
        pass

    def _default(self, *args):
        return self.response.set_status(400)

    def _request(self, *args):

        func_list = self._pili_get_func_list()

        if '_all' in func_list:
            target_method = '_all'
        elif args[0] is None:
            target_method = '_index'
        else:
            target_method = self._pili_get_target(args[0], func_list)

        # now we have _all, _index, _default or custom
        
        if target_method == '_all':
            args = self._pili_strip_none_args(list(args))
        elif target_method == '_index':
            args = list()
        elif target_method == '_default':
            args = self._pili_strip_none_args(list(args)[1:])
        else:
            args = self._pili_strip_none_args(list(args)[1:])

        method = getattr(self, target_method)
        spec = inspect.getargspec(method)
        
        if spec[3] is None:
            default_num = 0
        else:
            default_num = len(spec[3])
        _min = len(spec[0]) - default_num - 1

        if spec[1] is not None:
            _max = 999
        else:
            _max = len(spec[0]) - 1

        #return str(len(args)) + "@" + str(_min) + "#" + str(_max)
     
        if len(args) < _min or len(args) > _max:
            return self.response.set_status(400)

        if _max == 0:
            output = method()
        else:
            output = apply(method, args)

        if output is None:
            output = ''

        self.response.write(output)

        #from types import StringType
        #if type(output) is StringType:
        #    output = output.encode('utf-8')

        #return self._html + str(output)

        
        # profiler
        """
        profiler=web.input(profiler='').profiler
        if not profiler:
            return self._request()
        else:
            from google.appengine.api import users
            user=users.get_current_user()
            if not user:
                return web.webapi.TempRedirect(users.create_login_url(web.ctx.path + web.ctx.query))
            if not users.is_current_user_admin():
                return self.webapi.Unauthorized()

            import cProfile, pstats, StringIO
            prof = cProfile.Profile()
            self.html=""
            prof = prof.runctx("self.html=self._request()", globals(), locals())
            stream = StringIO.StringIO()
            stats = pstats.Stats(prof, stream=stream)
            stats.sort_stats(web.input(sort_stats="cumulative").sort_stats) # or time
            stats.print_stats(int(web.input(print_stats="300").print_stats))
            return self.html + "<pre>" + stream.getvalue() + "</pre>"
        """

    def echo(self, text):
        self.response.write(text)
        #self._html += str(text)

    def render(self, name, data={}):
        data.update({"ctx":web.ctx})
        return self._render.__getattr__(name)(data)

    def _pili_get_target(self, func, func_list):
        if func == '_all':
            return func
        func = func.lower()
        pattern = re.compile( "\-([a-z])" , re.I|re.M|re.S)
        match = re.findall(pattern, func)
        for i in match:
            func = func.replace('-' + i, i.upper())

        if not re.match(r"^[a-z]\w*$", func) or func not in func_list:
            return '_default'
        return func

    # get function list which does not belong to Base class
    def _pili_get_func_list(self):
        target_funcs = []
        for func in self.__class__.__dict__:
            if type(self.__class__.__dict__[func]) is not types.FunctionType:
                continue
            method = getattr(self, func)
            if self.__class__.__name__ == method.im_class.__name__:
                target_funcs.append(func)
        return target_funcs

    # we got so many None in args, need to strip it
    def _pili_strip_none_args(self, args):
        while(args[-1] is None):
            args.pop()
            if len(args) == 0:
                break
        return args

def simplerun(prefix_url, handler):
    app = webapp2.WSGIApplication([
        (r"%s/%s" % (prefix_url, "([^/]+)?/?"*10), handler)
        #webapp2.Route(r"%s/(.*)" % prefix_url, handler=handler, handler_method='_request'),
        ])
    app.run()
    
