from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .endpoints import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r"authors", AuthorViewSet)
router.register(r"books", BookViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"dashboard", DashboardViewSet,  basename='dashboard')


urlpatterns = [
    path("create_user/", CustomUserViewSet.as_view(), name="create_user"),
    path(
        "activate/<str:uidb64>/<str:token>/",
        ActivateAccount.as_view(),
        name="activate_account",
    ),
    path("", include(router.urls)),
    path("auth/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

# urlpatterns = router.urls
