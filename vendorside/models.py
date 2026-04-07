from django.db import models
from django.utils.text import slugify
from django.conf import settings

class Category(models.Model):
    categoryname = models.CharField(max_length=250, unique=True)
    description = models.CharField(max_length=255)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    image = models.ImageField(upload_to="categoryimage", blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.categoryname)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.categoryname


class Course(models.Model):
    vendor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    coursename = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    description = models.TextField()
    about = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    coverphoto = models.ImageField(upload_to="coursecover", blank=True)
    publishvendor = models.BooleanField(default=False)
    publishadmin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.coursename


class Video(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="videos")
    title = models.CharField(max_length=250)
    video = models.FileField(upload_to="coursevideos")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title