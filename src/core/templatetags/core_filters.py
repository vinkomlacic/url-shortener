from django import template

register = template.Library()


# This filter is necessary because it's impossible to pass an argument to a
# function in Django templates
@register.filter
def elided_page_range(paginator, number):
    return paginator.get_elided_page_range(number)
