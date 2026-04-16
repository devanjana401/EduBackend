from rest_framework import serializers
from .models import Category, Course, Video

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class CourseSerializer(serializers.ModelSerializer):
    # accept category as ID
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    vendor = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Course
        fields = "__all__"

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"