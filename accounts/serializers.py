from django.contrib.auth import authenticate
from rest_framework import serializers
from accounts.models import User
import django.contrib.auth.password_validation as validators


class CustomEmailSerializerField(serializers.EmailField):

    def to_internal_value(self, value):
        value = super(CustomEmailSerializerField,
                      self).to_internal_value(value)
        return value.lower()


class RegistrationSerializer(serializers.ModelSerializer):
    email = CustomEmailSerializerField(
        allow_null=False,
        required=True
    )
    password = serializers.CharField(
        write_only=True,
        min_length=6,
        style={'input_type': 'password'},
        validators=[validators.validate_password]
    )
    full_name = serializers.CharField(
        required=True,
        allow_null=False
    )

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password')


class LoginSerializer(serializers.Serializer):
    """
       serializer for login view
    """
    email = CustomEmailSerializerField()
    password = serializers.CharField(
        style={'input_type': 'password'},
    )

    default_error_messages = {
        'invalid_credentials': f"Password is invalid.Please try again",
        'invalid_account': f"User does not exist"
    }

    def __init__(self, *args, **kwargs):
        super(LoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError(
                self.error_messages['invalid_account']
            )
        self.user = authenticate(username=attrs.get(User.USERNAME_FIELD),
                                 password=attrs.get('password'))
        if not self.user:
            raise serializers.ValidationError(
                self.error_messages['invalid_credentials'])
        return attrs


class UserGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'full_name', 'email')