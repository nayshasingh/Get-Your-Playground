from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(list, index):
    try:
        return list[index]
    except IndexError:
        return None
