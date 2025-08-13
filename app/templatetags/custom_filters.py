from django import template

register = template.Library()

@register.filter
def get_item(container, key):
    """
    Template filter to get an item from a container (list or dictionary) using an index/key
    Usage: {{ my_dict|get_item:key }} or {{ my_list|get_item:index }}
    """
    if container is None:
        return None
        
    if isinstance(container, dict):
        return container.get(str(key))
    elif isinstance(container, (list, tuple)):
        try:
            return container[int(key)]
        except (IndexError, ValueError):
            return None
    return None

@register.filter
def ordinal(n):
    """Add ordinal suffix to number (1st, 2nd, 3rd, etc.)"""
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}"

@register.simple_tag
def get_grades():
    return ['NSY', 'LKG', 'UKG', '1', '2', '3', '4', '5', '6', '7', '8', '9', '11', '12']