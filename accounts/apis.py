from rest_framework import generics, permissions, response, status
from .models import User, UserAppointmentModel
from .serializers import RegistrationSerializer, LoginSerializer, UserGetSerializer, UserAppointmentPostSerializer, \
    UserAppointmentGetSerializer
from django.contrib.auth import user_logged_in
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
import calendar


class RegistrationAPI(generics.CreateAPIView):
    model = User
    serializer_class = RegistrationSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            User.objects.create_user(**serializer.validated_data)
            return response.Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return response.Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class LoginView(generics.GenericAPIView):
    """ Api for the user login """

    serializer_class = LoginSerializer
    permission_classes = (
        permissions.AllowAny,
    )

    def post(self, request, *args, **kargs):
        """
        login api
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.user  # take the user from serializer objects
            user_logged_in.send(
                sender=user.__class__, request=self.request, user=user)
            response_dict = dict()
            response_dict['user_id'] = user.id
            response_dict['msg'] = f"Login Successful"
            return response.Response(
                data=response_dict,
                status=status.HTTP_200_OK,
            )


class UserDetailsAPI(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = (permissions.IsAuthenticated,)
    model = User
    serializer_class = UserGetSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return self.model.objects.filter(id=user_id)


class UserAppointmentAPI(generics.ListCreateAPIView):
    model = UserAppointmentModel
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserAppointmentPostSerializer
        else:
            return UserAppointmentGetSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return self.model.objects.filter(user_id=user_id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            obj = self.model.objects.create(**serializer.validated_data)
            obj.user = self.request.user
            start_date = obj.start_timestamp.date()
            day_name = calendar.day_name[start_date.weekday()]
            obj.appointment_day = day_name
            obj.save()

            data.update({"user_id": obj.user.id,
                         "appointment_day": obj.appointment_day})
            response_dict = dict()
            response_dict['data'] = data
            return response.Response(
                response_dict,
                status=status.HTTP_201_CREATED
            )
        else:
            return response.Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


