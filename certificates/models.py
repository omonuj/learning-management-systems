from django.db import models
from shortuuid.django_fields import ShortUUIDField


# Create your models here.
class Certificate(models.Model):
    courses = models.ForeignKey("courses.Courses", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True)
    certificate_id = ShortUUIDField(unique=True, max_length=20, alphabet='1234567890')
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.courses.title


class CompletedLessons(models.Model):
    courses = models.ForeignKey("courses.Courses", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True)
    variant_item = models.ForeignKey("courses.VariantItem", on_delete=models.CASCADE,blank=True)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.courses.title


class EnrolledCourse(models.Model):
    courses = models.ForeignKey("courses.Courses", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey("teachers.Teacher", on_delete=models.SET_NULL, null=True, blank=True)
    order_item = models.ForeignKey("carts.CartOrderItem", on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    enrollment_id = ShortUUIDField(unique=True, max_length=20, alphabet='1234567890')

    def __str__(self):
        return self.courses.title

    def lectures(self):
        from courses.models import VariantItem
        return VariantItem.objects.filter(variant__courses=self.courses)

    def completed_lessons(self):
        return CompletedLessons.objects.filter(courses=self.courses, user=self.user)

    def curriculum(self):
        from courses.models import Variant
        return Variant.objects.filter(courses=self.courses)

    def note(self):
        from courses.models import Note
        return Note.objects.filter(courses=self.courses, user=self.user)

    def question_answer(self):
        from question_answer.models import QuestionAnswer
        return QuestionAnswer.objects.filter(courses=self.courses)

    def review(self):
        from courses.models import Review
        return Review.objects.filter(courses=self.courses, user=self.user).first()
