from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        model = User

    def create(self, validated_data):
        password = validated_data.get('password')
        user = User.objects.create(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
        )
        user.set_password(raw_password=password)
        user.save()
        return {
            'id': user.id,
            'username': user.username,
            'password': user.password,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }

    def check_value(self, key):
        if key in self.validated_data:
            return True
        return False

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        try:
            if validated_data['password']:
                instance.set_password(validated_data['password'])
        except:
            pass
        instance.save()
        return instance


def jwt_response_payload_handler(token, user=None, request=None):
    return dict(token=token, userid=user.id)
