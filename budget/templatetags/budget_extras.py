from django import template

register = template.Library()


@register.filter
def dict_get(d, key):
    """Retrieve a value from a dictionary using the given key."""
    if isinstance(d, dict):
        return d.get(key)
    return None