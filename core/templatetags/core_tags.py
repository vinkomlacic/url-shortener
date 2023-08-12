from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def fullurl(context, url):
    request = context['request']
    return request.build_absolute_uri(url)
