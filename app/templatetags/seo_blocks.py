from django import template

register = template.Library()

@register.simple_tag
def get_meta_image(request, image_url):
    """Convert relative image URL to absolute URL"""
    if not image_url:
        return ''
    if image_url.startswith('http'):
        return image_url
    return request.build_absolute_uri(image_url)