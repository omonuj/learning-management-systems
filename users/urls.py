from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (HomeView, RegisterView, UserProfileView,
                    UpdateUserProfileView, ChangePasswordView, LogoutView, CustomTokenObtainPairView)

urlpatterns = [

    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),

    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/update/', UpdateUserProfileView.as_view(), name='update-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # JWT Token Endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]