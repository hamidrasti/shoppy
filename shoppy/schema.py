import graphene
from graphene_django.debug import DjangoDebug

from accounts.schema import Query as AccountsQuery
from shop.schema import Query as ShopQuery


class Query(
    AccountsQuery,
    ShopQuery,
    graphene.ObjectType,
):
    debug = graphene.Field(DjangoDebug, name='_debug')


# noinspection PyTypeChecker
schema = graphene.Schema(query=Query)
