from django.urls import path
from .views import VendorRequestAPI, ApproveVendorRequestAPI, LoginAPI,SignupAPI

urlpatterns = [
    path('vendor-request/', VendorRequestAPI.as_view()),
    path('approve-vendor/<int:pk>/', ApproveVendorRequestAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path("signup/", SignupAPI.as_view(), name="signup"),
]