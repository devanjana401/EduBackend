from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken

from .models import VendorRequest, CustomUser, Vendor
from .serializers import VendorRequestSerializer,UserSerializer,VendorSerializer



# function to generate JWT tokens
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


# vendor request api
class VendorRequestAPI(APIView):

    # GET all vendor requests
    def get(self, request):
        requests = VendorRequest.objects.all()
        serializer = VendorRequestSerializer(requests, many=True)
        return Response(serializer.data)

    # create new vendor request
    def post(self, request):

        serializer = VendorRequestSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Request submitted successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# login API
class LoginAPI(APIView):

    def post(self, request):

        email = request.data.get("email")
        password = request.data.get("password")

        # authenticate user
        user = authenticate(request, username=email, password=password)

        if user is None:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # generate JWT tokens
        tokens = get_tokens_for_user(user)

        return Response({
            "message": "Login successful",
            "email": user.email,
            "role": user.role,
            "access": tokens["access"],
            "refresh": tokens["refresh"]
        })


# logout API        
class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Logged out successfully"})

        except Exception:
            return Response({"error": "Invalid token"}, status=400)


# signup API
class SignupAPI(APIView):

    def post(self, request):

        email = request.data.get("email")
        password = request.data.get("password")
        role = request.data.get("role")

        if CustomUser.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=400)

        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            role=role
        )

        return Response({"message": "User created successfully"})


# reset password
class ResetPasswordAPI(APIView):

    def post(self, request):
        email = request.data.get("email")
        new_password = request.data.get("new_password")

        if not email or not new_password:
            return Response({"error": "Email and new password are required"}, status=400)

        try:
            user = CustomUser.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password reset successfully"})
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=404)


from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PasswordResetOTP, CustomUser
from django.core.mail import send_mail
import random
class RequestOTPAPI(APIView):
    def post(self, request):
        email = request.data.get("email")
        if not CustomUser.objects.filter(email=email).exists():
            return Response({"error": "User with this email does not exist"}, status=404)

        # Generate 6-digit OTP
        otp = str(random.randint(100000, 999999))
        PasswordResetOTP.objects.filter(email=email).delete() # Clear old OTPs
        PasswordResetOTP.objects.create(email=email, otp=otp)

        # Send Email (Configure your settings.py for this to work)
        send_mail(
            "Your Password Reset OTP",
            f"Your OTP for password reset is: {otp}",
            "noreply@yourapp.com",
            [email],
        )
        return Response({"message": "OTP sent to your email"})

class ResetPasswordVerifyAPI(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")
        new_password = request.data.get("new_password")

        try:
            otp_record = PasswordResetOTP.objects.get(email=email, otp=otp)
            if not otp_record.is_valid():
                return Response({"error": "OTP has expired"}, status=400)
            
            user = CustomUser.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            
            otp_record.delete() # Clean up
            return Response({"message": "Password reset successfully"})
        except PasswordResetOTP.DoesNotExist:
            return Response({"error": "Invalid OTP"}, status=400)
