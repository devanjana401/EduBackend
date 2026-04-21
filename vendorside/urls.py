from django.urls import path
from .views import *

urlpatterns = [
    # vendor
    path("categories/", CategoryListView.as_view()),
    path("vendor-courses/", VendorCoursesView.as_view()),
    path("create-course/", CreateCourseView.as_view()),
    path("upload-video/", UploadVideoView.as_view()),
    path("vendor-videos/<int:course_id>/", VendorVideosView.as_view()),


    path('course/request/<int:pk>/', RequestCourseApprovalView.as_view()),

    # admin
    path("create-category/", CreateCategoryView.as_view()),
    path("pending-courses/", PendingCoursesView.as_view()),
    path("approve-course/<int:pk>/", ApproveCourseView.as_view()),

    # for admin
    path("approved-courses/", ApprovedCoursesView.as_view()),
    path("course/<int:pk>/", CourseDetailView.as_view()),
    path("course/update/<int:pk>/", UpdateCourseView.as_view()),
    path("course/delete/<int:pk>/", DeleteCourseView.as_view()),

    # for vendor
    path('course/<int:pk>/', VendorCourseDetailView.as_view()),
    path('course-update/<int:pk>/', VendorUpdateCourseView.as_view()),
    path('course-delete/<int:pk>/', VendorDeleteCourseView.as_view()),

    path('recent-videos/', RecentVideosView.as_view()),

    path('video/<int:pk>/', VideoDetailView.as_view()),
    path('video-update/<int:pk>/', UpdateVideoView.as_view()),
    path('video-delete/<int:pk>/', DeleteVideoView.as_view()),

    # public
    path("public-courses/", PublicCoursesView.as_view()),

    # purchased users
    path("vendor/purchases/", VendorPurchasesView.as_view()),

    # for self profile editing of vendor
    path("profile/", VendorProfileAPI.as_view()),
    path("profile/update/", VendorProfileUpdateAPI.as_view()),

]