from django import template
from pprint import pprint


class StrError(Exception):
    def __str__(self):
        return 'Error'


register = template.Library()

qwe = {'uio': '***',
       'f': '*'}


@register.filter()
def censor(value):
    try:
        if type(value) is not str:
            raise StrError()
    except StrError as e:
        pprint(e)
        return
    else:
        postfix = ''
        for i in value.split():
            if i.lower() in qwe:
                i = qwe[i.lower()]
            postfix += f'{i} '
        return f'{postfix}'
