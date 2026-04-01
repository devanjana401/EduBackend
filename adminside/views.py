from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Import models and serializers from account app
from accounts.models import CustomUser, VendorRequest, Vendor
from accounts.serializers import UserSerializer, VendorSerializer




# Create your views here.

# approve vendor request(admin only)
class ApproveVendorRequestAPI(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        # # allow only admin
        # if request.user.role != 1:
        #     return Response({"error": "Permission denied"}, status=403)

        try:
            vendor_request = VendorRequest.objects.get(id=pk)
        except VendorRequest.DoesNotExist:
            return Response({"error": "Request not found"}, status=404)

        # check already approved
        if vendor_request.status == 'approved':
            return Response({"message": "Already approved"})

        # change status
        vendor_request.status = 'approved'
        vendor_request.save()

        # create user account if not exists
        user = None

        if not CustomUser.objects.filter(email=vendor_request.email).exists():
            user = CustomUser.objects.create_user(
                email=vendor_request.email,
                password="1234",
                role=2
            )
        else:
            user = CustomUser.objects.get(email=vendor_request.email)

        # create vendor profile
        Vendor.objects.create(
            user=user,
            full_name=vendor_request.full_name,
            phone=vendor_request.phone,
            bio=vendor_request.bio,
            experience_years=vendor_request.experience_years,
            specialization=vendor_request.specialization,
            certificate=vendor_request.certificate,
            id_proof=vendor_request.id_proof
        )

        return Response({
            "message": "Vendor approved and account created"
        })
    

class BlockUserAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            user = CustomUser.objects.get(id=pk)
            user.is_active = False
            user.save()
            return Response({"message": "User blocked successfully"})
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class UnblockUserAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            user = CustomUser.objects.get(id=pk)
            user.is_active = True
            user.save()
            return Response({"message": "User unblocked successfully"})
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        

# users API
class UsersAPI(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)


# Vendors API
class VendorsAPI(APIView):

    def get(self, request):

        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)

        return Response(serializer.data)
