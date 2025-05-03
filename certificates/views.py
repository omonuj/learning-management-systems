from rest_framework import generics, status
from django.apps import apps
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


# Create your views here.
class StudentSummaryAPIView(generics.ListAPIView):

    from courses.serializers import StudentSummarySerializer

    serializer_class = StudentSummarySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        User = apps.get_model("users", "User")
        EnrolledCourses = apps.get_model("courses", "EnrolledCourse")
        CompletedLesson = apps.get_model("certificates", "CompletedLesson")
        Certificate = apps.get_model("certificates", "Certificate")

        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)

        total_courses = EnrolledCourses.objects.filter(user=user).count()
        completed_lessons = CompletedLesson.objects.filter(user=user).count()
        achieved_certificates = Certificate.objects.filter(user=user).count()

        return [{
            "total_courses": total_courses,
            "completed_lessons": completed_lessons,
            "achieved_certificates": achieved_certificates,
        }]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class StudentCourseListAPIView(generics.ListAPIView):

    from certificates.serializers import EnrolledCourseSerializer

    serializer_class = EnrolledCourseSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        User = apps.get_model("users", "User")
        EnrolledCourse = apps.get_model("certificates", "EnrolledCourse")

        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)
        return EnrolledCourse.objects.filter(user=user)


class StudentCourseDetailAPIView(generics.RetrieveAPIView):

    from certificates.serializers import EnrolledCourseSerializer

    serializer_class = EnrolledCourseSerializer
    permission_classes = [AllowAny]
    lookup_field = 'enrollment_id'

    def get_object(self):

        User = apps.get_model("users", "User")
        EnrolledCourse = apps.get_model("certificates", "EnrolledCourse")

        user_id = self.kwargs['user_id']
        enrollment_id = self.kwargs['enrollment_id']

        user = User.objects.get(id=user_id)
        return EnrolledCourse.objects.get(user=user, enrollment_id=enrollment_id)


class StudentCourseCompletedCreateAPIView(generics.CreateAPIView):

    from certificates.serializers import CompletedLessonSerializerShallow

    serializer_class = CompletedLessonSerializerShallow
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):

        User = apps.get_model("users", "User")
        Courses = apps.get_model("courses", "Course")
        VariantItem = apps.get_model("courses", "VariantItem")
        CompletedLesson = apps.get_model("certificates", "CompletedLesson")

        user_id = request.data['user_id']
        course_id = request.data['course_id']
        variant_item_id = request.data['variant_item_id']

        user = User.objects.get(id=user_id)
        course = Courses.objects.get(id=course_id)
        variant_item = VariantItem.objects.get(variant_item_id=variant_item_id)

        completed_lessons = CompletedLesson.objects.filter(user=user, course=course,
                                                                      variant_item=variant_item).first()

        if completed_lessons:
            completed_lessons.delete()
            return Response({"message": "Course marked as not completed"})

        else:
            CompletedLesson.objects.create(user=user, course=course, variant_item=variant_item)
            return Response({"message": "Course marked as completed"})


class StudentNoteCreateAPIView(generics.ListCreateAPIView):

    from courses.serializers import NoteSerializer

    serializer_class = NoteSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        User = apps.get_model("users", "User")
        EnrolledCourse = apps.get_model("certificates", "EnrolledCourse")
        Note = apps.get_model("courses", "Note")

        user_id = self.kwargs['user_id']
        enrollment_id = self.kwargs['enrollment_id']

        user = User.objects.get(id=user_id)
        enrolled = EnrolledCourse.objects.get(enrollment_id=enrollment_id)

        return Note.objects.filter(user=user, course=enrolled.course)

    def create(self, request, *args, **kwargs):

        User = apps.get_model("users", "User")
        EnrolledCourse = apps.get_model("certificates", "EnrolledCourse")
        Note = apps.get_model("courses", "Note")

        user_id = request.data['user_id']
        enrollment_id = request.data['enrollment_id']
        title = request.data['title']
        note = request.data['note']

        user = User.objects.get(id=user_id)
        enrolled = EnrolledCourse.objects.get(enrollment_id=enrollment_id)

        Note.objects.create(user=user, course=enrolled.course, note=note, title=title)

        return Response({"message": "Note created successfully"}, status=status.HTTP_201_CREATED)


