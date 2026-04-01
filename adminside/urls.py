from django.urls import path
from .views import (
    ApproveVendorRequestAPI,
    BlockUserAPI,
    UnblockUserAPI,
    UsersAPI,
    VendorsAPI
)

urlpatterns = [
    path('approve-vendor/<int:pk>/', ApproveVendorRequestAPI.as_view(), name='approve-vendor'),
    path('block-user/<int:pk>/', BlockUserAPI.as_view(), name='block-user'),
    path('unblock-user/<int:pk>/', UnblockUserAPI.as_view(), name='unblock-user'),
    path('users/', UsersAPI.as_view(), name='users-list'),
    path('vendors/', VendorsAPI.as_view(), name='vendors-list'),
]