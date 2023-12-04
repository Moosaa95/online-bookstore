from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .endpoints import *


urlpatterns = [
    path("create_user/", CustomUserViewSet.as_view(), name="create_user"),
    path(
        "activate/<str:uidb64>/<str:token>/",
        ActivateAccount.as_view(),
        name="activate_account",
    ),
]
