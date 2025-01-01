from django.urls import path
from teachers import views


urlpatterns = [

    # Teacher Routes
    path("teacher/summary/<teacher_id>/", views.TeacherSummaryAPIView.as_view()),
    path("teacher/course-lists/<teacher_id>/", views.TeacherCourseListAPIView.as_view()),
    path("teacher/review-lists/<teacher_id>/", views.TeacherReviewListAPIView.as_view()),
    path("teacher/review-detail/<teacher_id>/<review_id>/", views.TeacherReviewDetailAPIView.as_view()),
    path("teacher/student-lists/<teacher_id>/", views.TeacherStudentsListAPIVIew.as_view({'get': 'list'})),
    path("teacher/all-months-earning/<teacher_id>/", views.TeacherAllMonthEarningAPIView),
    path("teacher/best-course-earning/<teacher_id>/",
         views.TeacherBestSellingCourseAPIView.as_view({'get': 'list'})),
    path("teacher/course-order-list/<teacher_id>/", views.TeacherCourseOrdersListAPIView.as_view()),
    path("teacher/question-answer-list/<teacher_id>/", views.TeacherQuestionAnswerListAPIView.as_view()),
    path("teacher/coupon-list/<teacher_id>/", views.TeacherCouponListCreateAPIView.as_view()),
    path("teacher/coupon-detail/<teacher_id>/<coupon_id>/", views.TeacherCouponDetailAPIView.as_view()),
    path("teacher/noti-list/<teacher_id>/", views.TeacherNotificationListAPIView.as_view()),
    path("teacher/noti-detail/<teacher_id>/<noti_id>", views.TeacherNotificationDetailAPIView.as_view()),


]