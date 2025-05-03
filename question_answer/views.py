from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from django.apps import apps
from rest_framework.response import Response


# Create your views here.
class QuestionAnswerListCreateAPIView(generics.ListCreateAPIView):

    from question_answer.serializers import QuestionAnswerSerializer

    serializer_class = QuestionAnswerSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        Courses = apps.get_model('question_answer', 'Course')
        QuestionAnswer = apps.get_model('question_answer', 'QuestionAnswer')

        course_id = self.kwargs['course_id']
        course = Courses.objects.get(id=course_id)
        return QuestionAnswer.objects.filter(course=course)

    def create(self, request, *args, **kwargs):

        QuestionAnswerMessage = apps.get_model("question_answer", "QuestionAnswerMessage")
        QuestionAnswer = apps.get_model('question_answer', 'QuestionAnswer')

        User = apps.get_model('users', 'User')
        Courses = apps.get_model('courses', 'Courses')

        course_id = request.data['course_id']
        user_id = request.data['user_id']
        title = request.data['title']
        message = request.data['message']

        user = User.objects.get(id=user_id)
        course = Courses.objects.get(id=course_id)

        question = QuestionAnswer.objects.create(
            course=course,
            user=user,
            title=title
        )

        QuestionAnswerMessage.objects.create(
            course=course,
            user=user,
            message=message,
            question=question
        )

        return Response({"message": "Group conversation Started"}, status=status.HTTP_201_CREATED)


class QuestionAnswerMessageSendAPIView(generics.CreateAPIView):

    from question_answer.serializers import QuestionAnswerMessageSerializerShallow

    serializer_class = QuestionAnswerMessageSerializerShallow
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):

        User = apps.get_model("users", "User")
        Courses = apps.get_model('courses', 'Courses')
        QuestionAnswer = apps.get_model('question_answer', 'QuestionAnswer')
        QuestionAnswerMessage = apps.get_model("question_answer", "QuestionAnswerMessage")
        from question_answer.serializers import QuestionAnswerSerializer

        course_id = request.data['course_id']
        qa_id = request.data['qa_id']
        user_id = request.data['user_id']
        message = request.data['message']

        user = User.objects.get(id=user_id)
        course = Courses.objects.get(id=course_id)
        question = QuestionAnswer.objects.get(qa_id=qa_id)
        QuestionAnswerMessage.objects.create(
            course=course,
            user=user,
            message=message,
            question=question
        )

        question_serializer = QuestionAnswerSerializer(question)
        return Response({"message": "Message Sent", "question": question_serializer.data})


