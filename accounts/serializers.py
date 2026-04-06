from rest_framework import serializers
from .models import VendorRequest,CustomUser,Vendor

class VendorRequestSerializer(serializers.ModelSerializer):
    certificate_url = serializers.SerializerMethodField()
    id_proof_url = serializers.SerializerMethodField()

    class Meta:
        model = VendorRequest
        fields = '__all__'  # now includes certificate_url and id_proof_url
        read_only_fields = ('admin_remark', 'created_at')

    def get_certificate_url(self, obj):
        if obj.certificate:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.certificate.url)
            return obj.certificate.url
        return None

    def get_id_proof_url(self, obj):
        if obj.id_proof:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.id_proof.url)
            return obj.id_proof.url
        return None

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'role','is_active']


class VendorSerializer(serializers.ModelSerializer):

    email = serializers.CharField(source="user.email")
    certificate_url = serializers.SerializerMethodField()
    id_proof_url = serializers.SerializerMethodField()

    class Meta:
        model = Vendor
        fields = [
            'id',
            'full_name',
            'phone',
            'email',
            'experience_years',
            'specialization',
            'is_verified',
            'bio',
            'certificate_url',
            'id_proof_url'
        ]

    def get_certificate_url(self, obj):
        if obj.certificate:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.certificate.url)
            return obj.certificate.url
        return None

    def get_id_proof_url(self, obj):
        if obj.id_proof:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.id_proof.url)
            return obj.id_proof.url
        return None