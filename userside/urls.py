from django.urls import path
from .views import BuyCourseView, MyCoursesView, CourseVideosView
from vendorside.views import PublicCoursesView  

urlpatterns = [
    path("public-courses/", PublicCoursesView.as_view()), 

    path("buy/<int:course_id>/", BuyCourseView.as_view()),
    path("my-courses/", MyCoursesView.as_view()),
    path("videos/<int:course_id>/", CourseVideosView.as_view()),
]