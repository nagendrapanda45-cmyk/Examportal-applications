
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key))

@register.filter
def zip_lists(a, b):
    return zip(a, b)

# in custom_filters.py
@register.filter
def get_option_text(question, option_letter):
    return getattr(question, f"option_{option_letter.lower()}", "")

