from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser

# import models and serializers from account app
from accounts.models import CustomUser, VendorRequest, Vendor
from accounts.serializers import UserSerializer, VendorSerializer,VendorRequestSerializer
from vendorside.serializers import CategorySerializer

from userside.models import Purchase

from vendorside.models import Category, Course

from django.contrib.auth import get_user_model

# for password mail generate
from django.core.mail import send_mail
from django.conf import settings
import random
import string

# Create your views here.

# password generate 
def generate_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

# approve vendor request(admin only)
class ApproveVendorRequestAPI(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        try:
            vendor_request = VendorRequest.objects.get(id=pk)
        except VendorRequest.DoesNotExist:
            return Response({"error": "Request not found"}, status=404)

        # already approved check
        if vendor_request.status == 'approved':
            return Response({"message": "Already approved"})

        # update status
        vendor_request.status = 'approved'
        vendor_request.save()

        # create user
        if not CustomUser.objects.filter(email=vendor_request.email).exists():

            password = generate_password()

            user = CustomUser.objects.create_user(
                email=vendor_request.email,
                password=password,
                role=2
            )

            # send email here
            try:
                send_mail(
                    "Test Mail",
                    "Email working or not",
                    settings.EMAIL_HOST_USER,
                    ["yourgmail@gmail.com"],  # put your email
                    fail_silently=False,
                )
                print("✅ Email sent")

            except Exception as e:
                print("❌ Email error:", e)

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
            "message": "Vendor approved, account created & email sent"
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



# vendor actions api
class VendorViewAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        vendor = get_object_or_404(Vendor, id=pk)

        serializer = VendorSerializer(
            vendor,
            context={"request": request}
        )

        return Response(serializer.data)


class VendorUpdateAPI(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, pk):

        vendor = get_object_or_404(Vendor, id=pk)

        serializer = VendorSerializer(
            vendor,
            data=request.data,
            partial=True,
            context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)


class VendorDeleteAPI(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        vendor = get_object_or_404(Vendor, id=pk)

        vendor.delete()

        return Response({
            "message": "Vendor deleted successfully"
        })
    

# vendor-request actions api
class VendorRequestViewAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """View a single vendor request"""
        try:
            request_obj = VendorRequest.objects.get(id=pk)
            serializer = VendorRequestSerializer(request_obj,context={"request":request})
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
                        defaults={"role": 2}
                        )
                    if created:
                        password = generate_password()  
                        user.set_password(password)
                        user.save()
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
                    try:
                        send_mail(
                            subject="🎉 Your Vendor Account Has Been Approved",
                            message=f"""
                                Hello {vendor_request.full_name},

                                We are pleased to inform you that your vendor request has been successfully approved.

                                You can now log in and start using your vendor dashboard.

                                Login Details:
                                Email: {vendor_request.email}
                                {f"Password: {password}" if password else ""}

                                For security reasons, we strongly recommend that you change your password after your first login.

                                If you have any questions or need assistance, feel free to contact our support team.

                                Welcome aboard!

                                Best regards,  
                                Team EduPlatform
                                """,
                            from_email=settings.EMAIL_HOST_USER,
                            recipient_list=[vendor_request.email],
                            fail_silently=False,
                        )

                        print("✅ Approval email sent")

                    except Exception as e:
                        print("❌ Email error:", e)

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
        

# for categories to upload video by vendor
class CreateCategoryView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)
    

# api for see the users who purchased the course
class AdminPurchasesView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        purchases = Purchase.objects.filter(is_paid=True).select_related('user', 'course')

        data = []
        for p in purchases:
            data.append({
                "user": p.user.email,
                "course": p.course.coursename,
                "vendor": p.course.vendor.email,
                "date": p.purchased_at
            })

        return Response(data)
    

User = get_user_model()
class AdminDashboardCountsAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):

        data = {
            "users": User.objects.filter(is_staff=False).count(),
            "vendors": Vendor.objects.count(),
            "categories": Category.objects.count(),
            "courses": Course.objects.count(),
        }

        return Response(data)