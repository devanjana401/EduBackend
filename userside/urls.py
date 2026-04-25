from django.urls import path
from .views import BuyCourseView, MyCoursesView, CourseVideosView,PreviewVideosView
from vendorside.views import PublicCoursesView  

urlpatterns = [
    path("public-courses/", PublicCoursesView.as_view()), 

    path("buy/<int:course_id>/", BuyCourseView.as_view()),
    # path("verify-payment/<int:course_id>/", VerifyPaymentView.as_view()),
    path("my-courses/", MyCoursesView.as_view()),
    path("videos/<int:course_id>/", CourseVideosView.as_view()),

    path('preview-videos/<int:course_id>/', PreviewVideosView.as_view()),
]