from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Category, Course, Video
from .serializers import CategorySerializer, CourseSerializer, VideoSerializer

# ----------- Vendor Side ---------------

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


class CreateCourseView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(vendor=request.user, publishvendor=True)
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

    def get(self, request):
        # Get all videos for courses of the logged-in vendor
        videos = Video.objects.filter(course__vendor=request.user)
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)

# ----------- Admin Side ---------------

class CreateCategoryView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class PendingCoursesView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        courses = Course.objects.filter(publishvendor=True, publishadmin=False)
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


# ----------- Public Side for Students ---------------

class PublicCoursesView(APIView):
    def get(self, request):
        courses = Course.objects.filter(publishvendor=True, publishadmin=True)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)