import math

from django.db import models
from django.template.defaultfilters import slugify
from moviepy.video.io.VideoFileClip import VideoFileClip
from shortuuid.django_fields import ShortUUIDField


# Create your models here.
LANGUAGE_CHOICES = (
    ("ENGLISH", "English"),
    ("FRENCH", "French"),
    ("SPANISH", "Spanish"),
)

LEVEL = (
    ("BEGINNER", "Beginner"),
    ("INTERMEDIATE", "Intermediate"),
    ("ADVANCED", "Advanced"),
)


TEACHER_STATUS = (
    ("DRAFT", "Draft"),
    ("DISABLED", "Disabled"),
    ("PUBLISHED", "Published"),
)

PLATFORM_STATUS = (
    ("REVIEW", "Review"),
    ("DISABLED", "Disabled"),
    ("REJECTED", "Rejected"),
    ("DRAFT", "Draft"),
    ("PUBLISHED", "Published"),
)




RATING = (
    ("1", "1 Star"),
    ("2", "2 Star"),
    ("3", "3 Star"),
    ("4", "4 Star"),
    ("5", "5 Star"),

)

class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to='categories/', blank=True, null=True, default='default.jpg')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Category"
        ordering = ['title']


    def __str__(self):
        return self.title

    def count(self):
        return Courses.objects.filter(category=self).count()

    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug is None:
            self.slug = slugify(self.title)
        super(Category, self).save()



class Courses(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    teachers = models.ForeignKey("teachers.Teacher", on_delete=models.CASCADE, null=True, blank=True)
    introduction_video_file = models.FileField(upload_to='videos/', null=True, blank=True, default='videos/default.mp4')
    image = models.ImageField(upload_to='images/', null=True, blank=True, default='images/default.jpg')
    title =models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='ENGLISH', max_length=100)
    level = models.CharField(choices=LEVEL, default='BEGINNER', max_length=100)
    platform_status = models.CharField(choices=PLATFORM_STATUS, default='PUBLISHED', max_length=100)
    teacher_course_status = models.CharField(choices=TEACHER_STATUS, default='PUBLISHED', max_length=100)
    featured = models.BooleanField(default=False)
    course_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet='1234567890')
    slug = models.SlugField(unique=True, null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug is None:
            self.slug = slugify(self.title)
        super(Category).save()

    def student(self):
        from certificates.models import EnrolledCourse
        return EnrolledCourse.objects.filter(variant_course=self)

    def curriculum(self):
        return VariantItem.objects.filter(course=self)

    def lecture(self):
        return  VariantItem.objects.filter(course=self)

    def average_ratings(self):
        average_ratings = Review.objects.filter(course=self).aggregate(avg_rating=models.Avg('rating'))
        return average_ratings['rating__avg']

    def rating_count(self):
        return Review.objects.filter(course=self).count()

    def reviews(self):
        return Review.objects.filter(course=self, active=True)



class Variant(models.Model):
    courses = models.ForeignKey(Courses, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    variant_id = ShortUUIDField(unique=True, max_length=20, alphabet='1234567890')
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def variant_items(self):
        return VariantItem.objects.filter(variant=self)


class VariantItem(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    variant_item_id = ShortUUIDField(unique=True, max_length=20, alphabet='1234567890')
    description = models.TextField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    content_duration = models.CharField(null=True, blank=True, max_length=1000)
    preview = models.BooleanField(default=False)
    file = models.FileField(upload_to='files/', null=True, blank=True, default='files/default.jpg')
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.variant.title} - {self.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.file:
            clip = VideoFileClip(self.file.path)
            duration_seconds = clip.duration

            minutes, remainders =  divmod(duration_seconds, 60)
            minutes = math.floor(minutes)
            seconds = math.floor(duration_seconds)

            duration_text = f"{minutes}m {seconds}s"
            self.content_duration = duration_text
            super().save(update_fields=['content_duration'])


class Note(models.Model):
    courses = models.ForeignKey(Courses, on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=1000, null=True, blank=True)
    note = models.TextField()
    note_id = ShortUUIDField(unique=True, max_length=20, alphabet='1234567890')
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class Review(models.Model):
    courses = models.ForeignKey(Courses, on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    review = models.TextField()
    reply = models.CharField(null=True, blank=True, max_length=1000)
    active = models.BooleanField(default=True)
    ratings = models.IntegerField(choices=RATING, default=None)

    def __str__(self):
        return self.courses.title

    def profile(self):
        from users.models import UserProfile
        return UserProfile.objects.get(user=self.user)



class WishList(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True)
    courses = models.ForeignKey(Courses, on_delete=models.CASCADE)

    def __str__(self):
        return self.courses


class Country(models.Model):
    name = models.CharField(max_length=100)
    tax_rate = models.IntegerField(default=5)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name




