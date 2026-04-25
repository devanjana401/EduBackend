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