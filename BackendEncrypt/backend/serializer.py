from rest_framework import serializers
from .models import User, PasswordEntry


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Agrega info adicional si quieres
        token['username'] = user.username
        return token


# Serializer para el usuario
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


# Serializer para PasswordEntry
# class PasswordEntrySerializer(serializers.ModelSerializer):
#     raw_password = serializers.CharField(write_only=True, required=True)
#     decrypted_password = serializers.CharField(read_only=True, source='get_password')

#     class Meta:
#         model = PasswordEntry
#         fields = [
#             'id', 'title', 'username',
#             'service_url',
#             'created_at', 'updated_at',
#             'raw_password', 'decrypted_password'
#         ]
#         read_only_fields = ['id', 'created_at', 'updated_at', 'decrypted_password']

#     def create(self, validated_data):
#         raw_password = validated_data.pop('raw_password')
#         entry = PasswordEntry(**validated_data)
#         entry.set_password(raw_password)
#         entry.save()
#         return entry

#     def update(self, instance, validated_data):
#         raw_password = validated_data.pop('raw_password', None)
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         if raw_password:
#             instance.set_password(raw_password)
#         instance.save()
#         return instance

class PasswordEntrySerializer(serializers.ModelSerializer):
    raw_password = serializers.CharField(write_only=True, required=True)
    decrypted_password = serializers.CharField(read_only=True, source='get_password')

    class Meta:
        model = PasswordEntry
        fields = [
            'id', 'user', 'title', 'username',
            'service_url', 'created_at', 'updated_at',
            'raw_password', 'decrypted_password'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'decrypted_password', 'user']  # user es solo lectura

    def create(self, validated_data):
        raw_password = validated_data.pop('raw_password')
        entry = PasswordEntry(**validated_data)
        entry.set_password(raw_password)
        entry.save()
        return entry

    def update(self, instance, validated_data):
        raw_password = validated_data.pop('raw_password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if raw_password:
            instance.set_password(raw_password)
        instance.save()
        return instance
