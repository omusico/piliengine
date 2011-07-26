# -*- coding: utf-8 -*-
import re
import types
import inspect

from pili.ext import webapp2

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

        if len(args) < _min or len(args) > _max:
            return self.response.set_status(400)

        if _max == 0:
            output = method()
        else:
            output = apply(method, args)

        if output is None:
            output = ''

        self.response.write(output)

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

    #def render(self, name, data={}):
    #    data.update({"ctx":web.ctx})
    #    return self._render.__getattr__(name)(data)

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

route = webapp2.Route

create_app = webapp2.WSGIApplication

def pilirun(prefix_url, handler):
    app = create_app([(r"%s/%s" % (prefix_url, "([^/]+)?/?"*10), handler)])
    app.run()
    
