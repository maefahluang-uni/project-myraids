# matching/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def get_value(dictionary, key):
    """Returns the value of a key in a dictionary, or an empty string if key doesn't exist."""
    return dictionary.get(key, "")
