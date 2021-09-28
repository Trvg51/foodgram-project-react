from django.contrib.auth import get_user_model
from djoser.conf import settings
# from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

# class SubscribeField(serializers.Field):

#     def to_representation(self, value):
#         user_id = self.context.get('request').user.id
#         if value.filter(subscriber=user_id):
#             return True
#         return False


# class CustomUserSerializer(UserSerializer):
#     is_subscribed = SubscribeField(source='subscribed_to')

#     class Meta:
#         model = User
#         fields = tuple(User.REQUIRED_FIELDS) + (
#             settings.USER_ID_FIELD,
#             settings.LOGIN_FIELD,
#             'first_name',
#             'last_name',
#             'is_subscribed',
#         )
#         read_only_fields = (settings.LOGIN_FIELD)


# class CustomUserCreateSerializer(UserCreateSerializer):

#     class Meta:
#         model = User
#         fields = tuple(User.REQUIRED_FIELDS) + (
#             settings.USER_ID_FIELD,
#             settings.LOGIN_FIELD,
#             'first_name',
#             'last_name',
#             "password",
#         )
