from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from vendorside.models import Course, Video
from .models import Purchase
from .serializers import PreviewVideoSerializer


# Create your views here.

class BuyCourseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        user = request.user

        if Purchase.objects.filter(user=user, course_id=course_id).exists():
            return Response({"message": "Already purchased"})

        Purchase.objects.create(user=user, course_id=course_id, is_paid=True)

        return Response({"message": "Course purchased successfully"})
    
    
class MyCoursesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        purchases = Purchase.objects.filter(user=request.user, is_paid=True)
        courses = [p.course for p in purchases]

        from vendorside.serializers import CourseSerializer
        serializer = CourseSerializer(courses, many=True)

        return Response(serializer.data)
    
class CourseVideosView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):

        user = request.user

        if not Purchase.objects.filter(user=user, course_id=course_id, is_paid=True).exists():
            return Response({"error": "You need to purchase this course"}, status=403)

        videos = Video.objects.filter(course_id=course_id)

        from vendorside.serializers import VideoSerializer
        serializer = VideoSerializer(videos, many=True)

        return Response(serializer.data)
    

# api for preview of videos befor buying
class PreviewVideosView(APIView):

    def get(self, request, course_id):
        videos = Video.objects.filter(course_id=course_id)

        serializer = PreviewVideoSerializer(videos, many=True)
        return Response(serializer.data)
    


# razorpay integration
# import razorpay
# from django.conf import settings

# class BuyCourseView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, course_id):
#         user = request.user

#         if Purchase.objects.filter(user=user, course_id=course_id).exists():
#             return Response({"message": "Already purchased"})

#         course = Course.objects.get(id=course_id)

#         client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

#         order = client.order.create({
#             "amount": int(course.price * 100),
#             "currency": "INR",
#             "payment_capture": "1"
#         })

#         return Response({
#             "order_id": order["id"],
#             "amount": order["amount"],
#             "key": settings.RAZORPAY_KEY_ID
#         })



# class VerifyPaymentView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, course_id):

#         client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

#         data = {
#             "razorpay_order_id": request.data.get("razorpay_order_id"),
#             "razorpay_payment_id": request.data.get("razorpay_payment_id"),
#             "razorpay_signature": request.data.get("razorpay_signature"),
#         }

#         try:
#             client.utility.verify_payment_signature(data)

#             Purchase.objects.create(
#                 user=request.user,
#                 course_id=course_id,
#                 is_paid=True,
#                 razorpay_order_id=data["razorpay_order_id"],
#                 razorpay_payment_id=data["razorpay_payment_id"]
#             )

#             return Response({"message": "Payment successful"})

#         except:
#             return Response({"error": "Payment failed"}, status=400)