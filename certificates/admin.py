from django.contrib import admin
from certificates.models import *

# Register your models here.
admin.site.register(Certificate)
admin.site.register(CompletedLessons)
admin.site.register(EnrolledCourse)

