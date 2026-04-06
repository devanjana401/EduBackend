from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# import models and serializers from account app
from accounts.models import CustomUser, VendorRequest, Vendor
from accounts.serializers import UserSerializer, VendorSerializer,VendorRequestSerializer


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
    

# user block api
class BlockUserAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            user = CustomUser.objects.get(id=pk)

            # Prevent blocking admin
            if user.is_staff:
                return Response(
                    {"error": "Admin users cannot be blocked"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.is_active = False
            user.save()

            return Response({"message": "User blocked successfully"})

        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
# unblock user api
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


# user actions api
class UserViewAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = get_object_or_404(CustomUser, id=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class UserUpdateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        user = get_object_or_404(CustomUser, id=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class UserDeleteAPI(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        user = get_object_or_404(CustomUser, id=pk)
        user.delete()
        return Response({"message": "User deleted successfully"})


# vendor actions api
class VendorViewAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        vendor = get_object_or_404(Vendor, id=pk)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

class VendorUpdateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        vendor = get_object_or_404(Vendor, id=pk)
        serializer = VendorSerializer(vendor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class VendorDeleteAPI(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        vendor = get_object_or_404(Vendor, id=pk)
        vendor.delete()
        return Response({"message": "Vendor deleted successfully"})
    

# vendor-request actions api
# class VendorRequestListAPI(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         """Get all vendor requests"""
#         requests = VendorRequest.objects.all()
#         serializer = VendorRequestSerializer(requests, many=True)
#         return Response(serializer.data)

class VendorRequestViewAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """View a single vendor request"""
        try:
            request_obj = VendorRequest.objects.get(id=pk)
            serializer = VendorRequestSerializer(request_obj)
            return Response(serializer.data)
        except VendorRequest.DoesNotExist:
            return Response({"error": "Request not found"}, status=404)

class VendorRequestUpdateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            vendor_request = VendorRequest.objects.get(id=pk)
        except VendorRequest.DoesNotExist:
            return Response({"error": "Request not found"}, status=404)

        old_status = vendor_request.status
        serializer = VendorRequestSerializer(vendor_request, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            new_status = serializer.data.get("status")

            # Remove vendor if request changed from approved → pending/rejected
            if old_status == "approved" and new_status != "approved":
                try:
                    vendor = Vendor.objects.get(user__email=vendor_request.email)
                    vendor.delete()
                except Vendor.DoesNotExist:
                    pass

            # Create vendor if request changed to approved and vendor doesn't exist
            if new_status == "approved" and old_status != "approved":
                if not Vendor.objects.filter(user__email=vendor_request.email).exists():
                    user, created = CustomUser.objects.get_or_create(
                        email=vendor_request.email,
                        defaults={"role": 2, "password": "1234"}
                    )
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

            return Response(serializer.data)

        return Response(serializer.errors, status=400)


class VendorRequestDeleteAPI(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        """Delete a vendor request"""
        try:
            request_obj = VendorRequest.objects.get(id=pk)
            request_obj.delete()
            return Response({"message": "Vendor request deleted"})
        except VendorRequest.DoesNotExist:
            return Response({"error": "Request not found"}, status=404)