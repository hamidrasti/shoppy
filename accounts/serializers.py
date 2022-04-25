from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name', 'codename',)


class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'permissions',)


class CreateGroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)
    permission_ids = serializers.PrimaryKeyRelatedField(many=True, write_only=True, queryset=Permission.objects.all())

    class Meta:
        model = Group
        fields = ('id', 'name', 'permissions', 'permission_ids',)

    def create(self, validated_data):
        permission_ids = validated_data.pop('permission_ids')
        group = Group.objects.create(**validated_data)
        group.permissions.set(permission_ids)
        return group


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email',)


# noinspection PyAbstractClass
class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        data['user'] = UserSerializer(self.user).data
        # data['groups'] = self.user.groups.values_list('name', flat=True)

        return data
