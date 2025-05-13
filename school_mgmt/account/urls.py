from django.urls import path
from .views import RegisterView, LoginView, ProfileView,LogoutApiView
from rest_framework_simplejwt.views import TokenRefreshView,TokenVerifyView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutApiView.as_view(), name='logout'),  

    # JWT Token Endpoints
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'), 
]
