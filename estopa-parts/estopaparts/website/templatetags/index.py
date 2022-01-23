from django import template
register = template.Library()

@register.filter
def index(indexable, i):
    for x in indexable:
        if x[0]==i:
            return x[1]