from rest_framework import serializers
from .models import Purchase, ChatMessage
from vendorside.models import Video

class PurchaseSerializer(serializers.ModelSerializer):
    # extract the IDs specifically for your React URL params
    user_id = serializers.ReadOnlyField(source='user.id')
    course_id = serializers.ReadOnlyField(source='course.id')
    
    # provide the human-readable names for your table
    user = serializers.CharField(source='user.username', read_only=True)
    course = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Purchase
        # updated 'date' to 'purchased_at' to match your model
        fields = ['id', 'user_id', 'course_id', 'user', 'course', 'purchased_at']

class PreviewVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'description']


class ChatMessageSerializer(serializers.ModelSerializer):
    sender_id = serializers.ReadOnlyField(source='sender.id')

    class Meta:
        model = ChatMessage
        fields = ['id', 'user', 'course', 'sender_id', 'message', 'timestamp']