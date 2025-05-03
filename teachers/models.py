from django.db import models
from django.apps import apps

# Create your models here.
class Teacher(models.Model):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE)
    image = models.FileField(upload_to='teachers/', blank=True, null=True, default='default.jpg')
    full_name = models.CharField(max_length=100)
    bio = models.TextField()
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    about = models.TextField()
    country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.full_name

    def students(self):
        CartOrderItem = apps.get_model("carts", "CartOrderItem")
        return CartOrderItem.objects.filter(teacher=self)

    def courses(self):
        Courses = apps.get_model('courses', 'Courses')
        return Courses.objects.filter(teacher=self)

    def reviews(self):
        Courses = apps.get_model("courses", "Courses")
        return Courses.objects.filter(teacher=self).count()


class Coupon(models.Model):
    teacher = models.ForeignKey("teachers.Teacher", on_delete=models.SET_NULL, null=True, blank=True)
    used_by = models.ManyToManyField("users.User", blank=True)
    code = models.CharField(max_length=50)
    discount = models.DecimalField(default=0.00, decimal_places=2, max_digits=6)
    active = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

