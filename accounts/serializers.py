from rest_framework import serializers
from .models import VendorRequest

class VendorRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorRequest
        fields = '__all__'
        read_only_fields = ('status', 'admin_remark', 'created_at')