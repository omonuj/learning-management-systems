from django.urls import path
from courses import views


urlpatterns = [

    path("course/catgory/", views.CategoryListView.as_view(), name="category"),
    path("course/course-list/", views.CourseListAPIView.as_view()),
    path("course/search/", views.SearchCourseAPIView.as_view()),
    path("course/course-detail/<slug>/", views.CourseDetailAPIView.as_view()),
   path("student/course-note/<user_id>/<enrollment_id>/", views.StudentNoteCreateAPIView.as_view()),
   path("student/course-note-detail/<user_id>/<enrollment_id>/<note_id>/",
        views.StudentNoteDetailAPIView.as_view()),
   path("student/rate-course/", views.StudentRateCourseCreateAPIView.as_view()),
   path("student/review-detail/<user_id>/<review_id>/", views.StudentRateCourseUpdateAPIView.as_view()),
   path("student/wishlist/<user_id>/", views.StudentWishListListCreateAPIView.as_view()),
   path("teacher/course-create/", views.CourseCreateAPIView.as_view()),
   path("teacher/course-update/<teacher_id>/<course_id>/", views.CourseUpdateAPIView.as_view()),
   path("teacher/course/variant-delete/<variant_id>/<teacher_id>/<course_id>/",
        views.CourseVariantDeleteAPIView.as_view()),
   path("teacher/course/variant-item-delete/<variant_id>/<variant_item_id>/<teacher_id>/<course_id>/",
        views.CourseVariantItemDeleteAPIVIew.as_view()),
   path("file-upload/", views.FileUploadAPIView.as_view()),
    path("order/coupon/", views.CouponApplyAPIView.as_view()),

    path("student/course-note-detail/<user_id>/<enrollment_id>/<note_id>/",
         views.StudentNoteDetailAPIView.as_view()),
    path("student/rate-course/", views.StudentRateCourseCreateAPIView.as_view()),
    path("student/review-detail/<user_id>/<review_id>/", views.StudentRateCourseUpdateAPIView.as_view()),
    path("student/wishlist/<user_id>/", views.StudentWishListListCreateAPIView.as_view()),

    path("teacher/course-create/", views.CourseCreateAPIView.as_view()),
    path("teacher/course-update/<teacher_id>/<course_id>/", views.CourseUpdateAPIView.as_view()),
    path("teacher/course-detail/<course_id>/", views.TeacherCourseDetailAPIView.as_view()),
    path("teacher/course/variant-delete/<variant_id>/<teacher_id>/<course_id>/",
         views.CourseVariantDeleteAPIView.as_view()),
    path("teacher/course/variant-item-delete/<variant_id>/<variant_item_id>/<teacher_id>/<course_id>/",
         views.CourseVariantItemDeleteAPIVIew.as_view()),

    path("file-upload/", views.FileUploadAPIView.as_view())

]