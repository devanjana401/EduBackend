from django.urls import path
from .views import (
    ApproveVendorRequestAPI,
    BlockUserAPI,
    UnblockUserAPI,
    UsersAPI,
    VendorsAPI,
    UserViewAPI,
    UserUpdateAPI,
    UserDeleteAPI,
    VendorViewAPI,
    VendorUpdateAPI,
    VendorDeleteAPI,
    VendorRequestViewAPI,
    VendorRequestUpdateAPI,
    VendorRequestDeleteAPI,
)

urlpatterns = [
    path('approve-vendor/<int:pk>/', ApproveVendorRequestAPI.as_view(), name='approve-vendor'),
    path('block-user/<int:pk>/', BlockUserAPI.as_view(), name='block-user'),
    path('unblock-user/<int:pk>/', UnblockUserAPI.as_view(), name='unblock-user'),
    path('users/', UsersAPI.as_view(), name='users-list'),
    path('vendors/', VendorsAPI.as_view(), name='vendors-list'),

    
    # user actions
    path('user/<int:pk>/', UserViewAPI.as_view(), name='user-view'),
    path('user-update/<int:pk>/', UserUpdateAPI.as_view(), name='user-update'),
    path('user-delete/<int:pk>/', UserDeleteAPI.as_view(), name='user-delete'),

    # vendor actions
    path('vendor/<int:pk>/', VendorViewAPI.as_view(), name='vendor-view'),
    path('vendor-update/<int:pk>/', VendorUpdateAPI.as_view(), name='vendor-update'),
    path('vendor-delete/<int:pk>/', VendorDeleteAPI.as_view(), name='vendor-delete'),

    # vendor - request actions
    path("vendor-request/<int:pk>/", VendorRequestViewAPI.as_view(), name="vendor-request-view"),
    path("vendor-request-update/<int:pk>/", VendorRequestUpdateAPI.as_view(), name="vendor-request-update"),
    path("vendor-request-delete/<int:pk>/", VendorRequestDeleteAPI.as_view(), name="vendor-request-delete"),
]