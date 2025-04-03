from django.contrib import admin
from question_answer.models import *

# Register your models here.
admin.site.register(QuestionAnswer)
admin.site.register(QuestionAnswerMessage)