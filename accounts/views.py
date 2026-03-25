from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate

from .models import VendorRequest, CustomUser, Vendor
from .serializers import VendorRequestSerializer


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


# approve vendor request
class ApproveVendorRequestAPI(APIView):

    def post(self, request, pk):

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

        # create user account
        user = CustomUser.objects.create_user(
            email=vendor_request.email,
            password="1234",   # default password
            role=2
        )

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

        return Response({
            "message": "Login successful",
            "email": user.email,
            "role": user.role
        })

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