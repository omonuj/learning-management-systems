from django.urls import path
from question_answer import views


urlpatterns = [

    path("student/question-answer-list-create/<course_id>/", views.QuestionAnswerListCreateAPIView.as_view()),
    path("student/question-answer-message-create/", views.QuestionAnswerMessageSendAPIView.as_view()),


]