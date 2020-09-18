from django import template
register = template.Library()

@register.filter
def sort_by(queryset, order):
    return queryset.order_by(order)

@register.filter
def count_comments(queryset, id):
    return queryset.filter(post_id=id).count()