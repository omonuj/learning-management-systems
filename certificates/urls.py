from django.urls import path
from certificates import views

urlpatterns = [


    # Student API Endpoints
    path("student/summary/<user_id>/", views.StudentSummaryAPIView.as_view()),
    path("student/course-list/<user_id>/", views.StudentCourseListAPIView.as_view()),
    path("student/course-detail/<user_id>/<enrollment_id>/", views.StudentCourseDetailAPIView.as_view()),
    path("student/course-completed/", views.StudentCourseCompletedCreateAPIView.as_view()),
    path("student/course-note/<user_id>/<enrollment_id>/", views.StudentNoteCreateAPIView.as_view()),

]