from django.db import models
from django.conf import settings
from vendorside.models import Course

# Create your models here.

class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    purchased_at = models.DateTimeField(auto_now_add=True)

    # razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    # razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.course}"
    


from django.contrib.auth import get_user_model

User = get_user_model()

class ChatMessage(models.Model):
    # 'user' is the student, 'course' is the context
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student_messages")
    course = models.ForeignKey('vendorside.Course', on_delete=models.CASCADE)
    
    # Who actually sent this specific text?
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.email}: {self.message[:20]}"