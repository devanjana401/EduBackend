from django.urls import path
from .views import VendorRequestAPI, ApproveVendorRequestAPI, LoginAPI,SignupAPI,UsersAPI,VendorsAPI,LogoutAPI

urlpatterns = [
    # vendor request
    path('vendor-request/', VendorRequestAPI.as_view()),
    path('approve-vendor/<int:pk>/', ApproveVendorRequestAPI.as_view()),

    # authentication
    path('login/', LoginAPI.as_view()),
    path("logout/", LogoutAPI.as_view()),
    path("signup/", SignupAPI.as_view(), name="signup"),

    # admin dashboard APIs
    path("users/", UsersAPI.as_view()),
    path("vendors/", VendorsAPI.as_view()),
]