from django import template


register = template.Library()

qwe = ['UIO', 'f']

@register.filter()
def censor(value):
   postfix = ''
   for i in value.split():
      if i in qwe:
         i = '*'
      postfix += f'{i} '

   return f'{postfix}'