from django.contrib.auth import get_user_model
from graphene import Node
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

User = get_user_model()


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (Node,)
        # fields = '__all__'
        exclude = ('password',)
        filter_fields = ['username', 'first_name', 'last_name']


class Query(object):
    user = Node.Field(UserNode)
    users = DjangoFilterConnectionField(UserNode)
