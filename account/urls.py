from django.urls import path
from .views import *
from rest_framework_simplejwt.views import ( # type: ignore
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/register/', UserCreateView.as_view(), name='user-register'),
    path('api/token/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/profile/<int:id>/', UserProfileView.as_view(), name='user-profile'),
    path("api/update/<int:id>/", UserUpdateView.as_view(), name="user-update"),
    path("api/delete/<int:id>/", UserDeleteView.as_view(), name="user-delete"),
    path("api/all/", GetAllUsersView.as_view(), name="get-all-users"),
]
