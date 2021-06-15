from rest_framework import generics, permissions, response, status
from .models import User
from .serializers import RegistrationSerializer, LoginSerializer, UserGetSerializer
from django.contrib.auth import user_logged_in
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


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




