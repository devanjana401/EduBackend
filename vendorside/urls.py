from django.urls import path
from .views import *

urlpatterns = [
    # Vendor
    path("categories/", CategoryListView.as_view()),
    path("vendor-courses/", VendorCoursesView.as_view()),
    path("create-course/", CreateCourseView.as_view()),
    path("upload-video/", UploadVideoView.as_view()),
    path("vendor-videos/<int:course_id>/", VendorVideosView.as_view()),

    # Admin
    path("create-category/", CreateCategoryView.as_view()),
    path("pending-courses/", PendingCoursesView.as_view()),
    path("approve-course/<int:pk>/", ApproveCourseView.as_view()),

    # Public
    path("public-courses/", PublicCoursesView.as_view()),
]