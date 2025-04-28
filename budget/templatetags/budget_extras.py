from django import template
from django.utils.html import escape

register = template.Library()


@register.filter
def dict_get(d, key):
    """Retrieve a value from a dictionary using the given key."""
    if isinstance(d, dict):
        return d.get(key)
    return None

@register.filter(name='add_class')
def add_class(field, css_class):
    """
       Appends the specified class to the form field widget's class attribute.
       """
    return field.as_widget(attrs={'class': css_class})
