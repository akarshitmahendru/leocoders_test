from django.contrib.auth import authenticate
from rest_framework import serializers
from accounts.models import User, UserAppointmentModel
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


class UserAppointmentPostSerializer(serializers.ModelSerializer):

    start_timestamp = serializers.DateTimeField(
        input_formats=["%Y-%m-%d %H:%M"],
        required=True)
    end_timestamp = serializers.DateTimeField(
        input_formats=["%Y-%m-%d %H:%M"],
        required=True
    )

    def validate(self, attrs):
        start_timestamp = attrs.get('start_timestamp')
        end_timestamp = attrs.get('end_timestamp')
        duration_diff = (end_timestamp - start_timestamp).total_seconds()/60
        if duration_diff > 60:
            raise serializers.ValidationError(
                f"Appointment can't be booked for time slot greater than 1 hour"
            )
        else:
            return attrs

    class Meta:
        model = UserAppointmentModel
        fields = ('start_timestamp', 'end_timestamp')


class UserAppointmentGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAppointmentModel
        fields = "__all__"

