import re

try:
    # Jinja 3.1+
    from jinja2 import pass_eval_context as eval_context_decorator
    from markupsafe import Markup, escape
except ImportError:
    # Jinja < 3.1
    from jinja2 import evalcontextfilter as eval_context_decorator
    from jinja2 import Markup, escape

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

@eval_context_decorator
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', Markup('<br>\n'))
                          for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result

