from django.urls import path
from .views import (
    ApproveVendorRequestAPI,
    BlockUserAPI,
    UnblockUserAPI,
    UsersAPI,
    VendorsAPI,
    ProfileViewAPI,
    ProfileUpdateAPI,
    ProfileDeleteAPI
)

urlpatterns = [
    path('approve-vendor/<int:pk>/', ApproveVendorRequestAPI.as_view(), name='approve-vendor'),
    path('block-user/<int:pk>/', BlockUserAPI.as_view(), name='block-user'),
    path('unblock-user/<int:pk>/', UnblockUserAPI.as_view(), name='unblock-user'),
    path('users/', UsersAPI.as_view(), name='users-list'),
    path('vendors/', VendorsAPI.as_view(), name='vendors-list'),

    
    path("profile/<str:role>/<int:pk>/", ProfileViewAPI.as_view()),
    path("profile-update/<str:role>/<int:pk>/", ProfileUpdateAPI.as_view()),
    path("profile-delete/<str:role>/<int:pk>/", ProfileDeleteAPI.as_view()),
]