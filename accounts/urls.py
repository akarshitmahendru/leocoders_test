from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import apis

router = DefaultRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^registration/$', apis.RegistrationAPI.as_view(), name='register'),
    url(r'^login/$', apis.LoginView.as_view(), name='login'),
    url(r'^user/$', apis.UserDetailsAPI.as_view(), name='users'),

]