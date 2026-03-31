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