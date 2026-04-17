from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import status

from .models import Category, Course, Video
from .serializers import CategorySerializer, CourseSerializer, VideoSerializer


# ----------- vendor side ---------------

class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class VendorCoursesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        courses = Course.objects.filter(vendor=request.user)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)


# no auto publish
class CreateCourseView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                vendor=request.user,
                publishvendor=False,   # ❌ not published
                publishadmin=False
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class UploadVideoView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class VendorVideosView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        videos = Video.objects.filter(
            course__id=course_id,
            course__vendor=request.user
        )
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)


# request course approval
class RequestCourseApprovalView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            course = Course.objects.get(id=pk, vendor=request.user)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=404)

        videos = Video.objects.filter(course=course)

        #  must upload videos
        if videos.count() == 0:
            return Response(
                {"error": "Upload at least one video before requesting approval"},
                status=400
            )

        # optional minimum videos
        # if videos.count() < 3:
        #     return Response({"error": "Minimum 3 videos required"}, status=400)

        course.publishvendor = True
        course.is_requested = True
        course.save()

        return Response({"message": "Request sent to admin"})


# ----------- admin side ---------------

class CreateCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


#  show only requested courses
class PendingCoursesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        courses = Course.objects.filter(
            is_requested=True,
            publishvendor=True,
            publishadmin=False
        )
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)


class ApproveCourseView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            course = Course.objects.get(id=pk)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=404)

        course.publishadmin = True
        course.save()

        return Response({"message": "Course approved"})


class ApprovedCoursesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        courses = Course.objects.filter(
            publishvendor=True,
            publishadmin=True
        )
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)


# ----------- course actions ---------------

class CourseDetailView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class UpdateCourseView(UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class DeleteCourseView(DestroyAPIView):
    queryset = Course.objects.all()


# ----------- public side (students) ---------------

class PublicCoursesView(APIView):
    def get(self, request):
        courses = Course.objects.filter(
            publishvendor=True,
            publishadmin=True
        )
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)