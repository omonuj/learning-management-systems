from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.apps import apps



# Create your models here.
class QuestionAnswer(models.Model):
    courses = models.ForeignKey("courses.Courses", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=100,null=True, blank=True)
    qa_id = ShortUUIDField(unique=True, max_length=20, alphabet='1234567890')
    datetime = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        return f"{self.user.username} - {self.courses.title}"

    class Meta:
        ordering = ['-datetime']

    def messages(self):
        return QuestionAnswerMessage.objects.filter(question=self)

    def profile(self):
        UserProfile = apps.get_model('users', 'UserProfile')
        return UserProfile.objects.get(user=self)


class QuestionAnswerMessage(models.Model):
    courses = models.ForeignKey("courses.Courses", on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionAnswer, on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    gam_id = ShortUUIDField(unique=True, max_length=20, alphabet='1234567890')
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.courses.title}"

    class Meta:
        ordering = ['datetime']
