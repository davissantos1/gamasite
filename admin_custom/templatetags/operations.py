# myapp/templatetags/operations.py
from django import template

register = template.Library()

@register.filter
def divide_half(value):
    """Divide o valor por 2 e retorna o resultado."""
    try:
        return value // 2
    except (TypeError, ValueError):
        return 0
