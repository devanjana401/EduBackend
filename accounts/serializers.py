from rest_framework import serializers
from .models import VendorRequest,CustomUser,Vendor

class VendorRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorRequest
        fields = '__all__'
        read_only_fields = ('status', 'admin_remark', 'created_at')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'role']


class VendorSerializer(serializers.ModelSerializer):

    email = serializers.CharField(source="user.email")

    class Meta:
        model = Vendor
        fields = [
            'id',
            'full_name',
            'phone',
            'email',
            'experience_years',
            'specialization',
            'is_verified'
        ]