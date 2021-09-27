from django import template
from django.shortcuts import get_object_or_404
#
# from applications.recipes.models import PurchaseList
# from applications.users.models import User

register = template.Library()


# @register.simple_tag(takes_context=True)
# def is_favorite(context):
#     return context['user'].favorites.filter(recipe=context['recipe']).exists()
#

@register.filter()
def addclass(field, arg):
    return field.as_widget(attrs={'class': arg})

#
# @register.simple_tag(takes_context=True)
# def is_author_id(context):
#     username = context['request']
#     return get_object_or_404(
#         User, username=username.resolver_match.kwargs['username']).pk
#
#
# @register.simple_tag(takes_context=True)
# def is_followed(context):
#     followed = is_author_id(context)
#     return context['user'].follower.filter(author=followed).exists()
#
#
# @register.simple_tag(takes_context=True)
# def is_in_purchaselist(context):
#     return context['user'].purchasing.filter(
#         recipe=context['recipe']).exists()
#
#
# @register.filter()
# def last_three_recipes(recipes):
#     return recipes[:3]
#
#
# @register.simple_tag(takes_context=True)
# def amount_of_purchase(context):
#     return PurchaseList.objects.filter(user=context['user']).count()
#
#
# @register.simple_tag(takes_context=True)
# def manage_tags(context, **kwargs):
#     tag = kwargs['tag']
#     query_string = context['request'].GET.copy()
#     tags = query_string.getlist('tags')
#     if tag in tags:
#         tags.remove(tag)
#     else:
#         tags.append(tag)
#     query_string.setlist('tags', tags)
#
#     if 'page' in query_string:
#         query_string.pop('page')
#
#     return query_string.urlencode()
#
#
# @register.simple_tag(takes_context=True)
# def param_replace(context, **kwargs):
#     query_string = context['request'].GET.copy()
#     if 'page' in kwargs:
#         query_string['page'] = kwargs.get('page')
#
#     return query_string.urlencode()
