from django.urls import path
from .views import VendorRequestAPI, LoginAPI,SignupAPI,LogoutAPI,ResetPasswordAPI

urlpatterns = [
    
    # vendor request
    path('vendor-request/', VendorRequestAPI.as_view()),

    # authentication
    path('login/', LoginAPI.as_view()),
    path("logout/", LogoutAPI.as_view()),
    path("signup/", SignupAPI.as_view(), name="signup"),
    path("reset-password/", ResetPasswordAPI.as_view(), name="reset-password"),
]