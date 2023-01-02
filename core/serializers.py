from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError

USER_MODEL = get_user_model()


class CreateUserSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = USER_MODEL
        fields = '__all__'

    def validate(self, attrs: dict):
        password: str = attrs.get("password")
        password_repeat: str = attrs.pop("password_repeat", None)
        if password != password_repeat:
            raise ValidationError("password and password_repeat is not equal")
        return attrs

    def create(self, validated_data):

        hashed_password = make_password(validated_data.get('password'))
        validated_data['password'] = hashed_password
        instance = super().create(validated_data)
        return instance


    # def create(self, validated_data: dict):
    #     password: str = validated_data.get('password')
    #     password_repeat: str = validated_data.pop('password_repeat')
    #
    #     if password != password_repeat:
    #         raise ValidationError('Пароли не совпадают')
    #
    #     hashed_password = make_password(password)
    #     validated_data['password'] = hashed_password
    #     instance = super().create(validated_data)
    #     return instance


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = USER_MODEL
        fields = ['username', 'password']

    def create(self, validated_data):
        user = authenticate(
            username=validated_data['username'],
            password=validated_data['password']
        )
        if not user:
            raise exceptions.AuthenticationFailed
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER_MODEL
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class UpdatePasswordSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        user = attrs['user']
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError('Некорректный старый пароль')
        return attrs

    def update(self, instance, validated_data):
        instance.password = make_password(validated_data['new_password'])
        instance.save()
        return instance
