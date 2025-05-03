from django.db import models
from django.db.models.functions import ExtractMonth
from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.apps import apps
from rest_framework.response import Response
from datetime import datetime, timedelta


# Create your views here.
class TeacherCourseDetailAPIView(generics.RetrieveAPIView):

    from courses.serializers import CourseSerializer
    Courses = apps.get_model('courses', 'Courses')

    serializer_class = CourseSerializer
    permission_classes = [AllowAny]
    queryset = Courses.objects.filter(platform_status="Published", teacher_course_status="Published")

    def get_object(self):

        Courses = apps.get_model('courses', 'Courses')

        course_id = self.kwargs['course_id']
        course = Courses.objects.get(course_id=course_id, platform_status="Published",
                                               teacher_course_status="Published")
        return course


class CouponApplyAPIView(generics.CreateAPIView):

    from teachers.serializers import CouponSerializer

    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        CartOrder = apps.get_model('carts', 'CartOrder')
        Coupon = apps.get_model("teachers", "Coupon")
        CartOrderItem = apps.get_model('carts', 'CartOrderItem')

        order_oid = request.data['order_oid']
        coupon_code = request.data['coupon_code']

        order = CartOrder.objects.get(oid=order_oid)
        coupon = Coupon.objects.filter(code=coupon_code).first()

        if coupon:
            order_items = CartOrderItem.objects.filter(order=order, teacher=coupon.teacher)
            for i in order_items:
                if not coupon in i.coupons.all():
                    discount = i.total * coupon.discount / 100

                    i.total -= discount
                    i.price -= discount
                    i.saved += discount
                    i.applied_coupon = True
                    i.coupons.add(coupon)

                    order.coupons.add(coupon)
                    order.total -= discount
                    order.sub_total -= discount
                    order.saved += discount

                    i.save()
                    order.save()
                    coupon.used_by.add(order.student)
                    return Response({"message": "Coupon Found and Activated", "icon": "success"},
                                    status=status.HTTP_201_CREATED)
                else:
                    return Response({"message": "Coupon Already Applied", "icon": "warning"}, status=status.HTTP_200_OK)
        else:

            return Response({"message": "Coupon Not Found", "icon": "error"}, status=status.HTTP_404_NOT_FOUND)



class TeacherSummaryAPIView(generics.ListAPIView):

    from teachers.serializers import TeacherSummarySerializer

    serializer_class =TeacherSummarySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        Teacher = apps.get_model('teachers', 'Teacher')
        Courses = apps.get_model('courses', 'Courses')
        CartOrderItem = apps.get_model('carts', 'CartOrderItem')
        EnrolledCourse = apps.get_model("certificates", "EnrolledCourse")
        User = apps.get_model('users', 'User')

        teacher_id = self.kwargs['teacher_id']
        teacher = Teacher.objects.get(id=teacher_id)

        one_month_ago = datetime.today() - timedelta(days=28)

        total_courses = Courses.objects.filter(teacher=teacher).count()
        total_revenue = \
        CartOrderItem.objects.filter(teacher=teacher, order__payment_status="Paid").aggregate(
            total_revenue=models.Sum("price"))['total_revenue'] or 0
        monthly_revenue = CartOrderItem.objects.filter(teacher=teacher, order__payment_status="Paid",
                                                                  date__gte=one_month_ago).aggregate(
            total_revenue=models.Sum("price"))['total_revenue'] or 0

        enrolled_courses = EnrolledCourse.objects.filter(teacher=teacher)
        unique_student_ids = set()
        students = []

        for course in enrolled_courses:
            if course.user_id not in unique_student_ids:
                user = User.objects.get(id=course.user_id)
                student = {
                    "full_name": user.profile.full_name,
                    "image": user.profile.image.url,
                    "country": user.profile.country,
                    "date": course.date
                }

                students.append(student)
                unique_student_ids.add(course.user_id)

        return [{
            "total_courses": total_courses,
            "total_revenue": total_revenue,
            "monthly_revenue": monthly_revenue,
            "total_students": len(students),
        }]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TeacherCourseListAPIView(generics.ListAPIView):

    from courses.serializers import CourseSerializer

    serializer_class = CourseSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        Teacher = apps.get_model('teachers', 'Teacher')
        Courses = apps.get_model('courses', 'Courses')

        teacher_id = self.kwargs['teacher_id']
        teacher = Teacher.objects.get(id=teacher_id)
        return Courses.objects.filter(teacher=teacher)


class TeacherReviewListAPIView(generics.ListAPIView):

    from courses.serializers import ReviewSerializer

    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        Teacher = apps.get_model("teachers", "Teacher")
        Review = apps.get_model('courses', 'Review')

        teacher_id = self.kwargs['teacher_id']
        teacher = Teacher.objects.get(id=teacher_id)
        return Review.objects.filter(course__teacher=teacher)


class TeacherReviewDetailAPIView(generics.RetrieveUpdateAPIView):

    from courses.serializers import ReviewSerializer

    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    def get_object(self):

        Teacher = apps.get_model('teachers', 'Teacher')
        Review = apps.get_model("courses", "Review")

        teacher_id = self.kwargs['teacher_id']
        review_id = self.kwargs['review_id']
        teacher = Teacher.objects.get(id=teacher_id)
        return Review.objects.get(course__teacher=teacher, id=review_id)


class TeacherStudentsListAPIVIew(viewsets.ViewSet):

    def list(self, request, teacher_id=None):

        Teacher = apps.get_model("teachers", "Teacher")
        EnrolledCourse = apps.get_model("certificates", "EnrolledCourse")
        User = apps.get_model('users', 'User')

        teacher = Teacher.objects.get(id=teacher_id)

        enrolled_courses = EnrolledCourse.objects.filter(teacher=teacher)
        unique_student_ids = set()
        students = []

        for course in enrolled_courses:
            if course.user_id not in unique_student_ids:
                user = User.objects.get(id=course.user_id)
                student = {
                    "full_name": user.profile.full_name,
                    "image": user.profile.image.url,
                    "country": user.profile.country,
                    "date": course.date
                }

                students.append(student)
                unique_student_ids.add(course.user_id)

        return Response(students)


@api_view(("GET",))
def TeacherAllMonthEarningAPIView(request, teacher_id):

    Teacher = apps.get_model("teachers", "Teacher")
    CartOrderItem = apps.get_model("carts", "CartOrderItem")

    teacher = Teacher.objects.get(id=teacher_id)
    monthly_earning_tracker = (
        CartOrderItem.objects
        .filter(teacher=teacher, order__payment_status="Paid")
        .annotate(
            month=ExtractMonth("date")
        )
        .values("month")
        .annotate(
            total_earning=models.Sum("price")
        )
        .order_by("month")
    )

    return Response(monthly_earning_tracker)


class TeacherBestSellingCourseAPIView(viewsets.ViewSet):

    def list(self, request, teacher_id=None):

        Teacher = apps.get_model("teachers", "Teacher")
        Courses = apps.get_model("courses", "Courses")

        teacher = Teacher.objects.get(id=teacher_id)
        courses_with_total_price = []
        courses = Courses.objects.filter(teacher=teacher)

        for course in courses:
            revenue = course.enrolledcourse_set.aggregate(total_price=models.Sum('order_item__price'))[
                          'total_price'] or 0
            sales = course.enrolledcourse_set.count()

            courses_with_total_price.append({
                'course_image': course.image.url,
                'course_title': course.title,
                'revenue': revenue,
                'sales': sales,
            })

        return Response(courses_with_total_price)


class TeacherCourseOrdersListAPIView(generics.ListAPIView):

    from carts.serializers import CartOrderItemSerializer

    serializer_class = CartOrderItemSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        Teacher = apps.get_model("teachers", "Teacher")
        CartOrderItem = apps.get_model("carts", "CartOrderItem")

        teacher_id = self.kwargs['teacher_id']
        teacher = Teacher.objects.get(id=teacher_id)

        return CartOrderItem.objects.filter(teacher=teacher)


class TeacherQuestionAnswerListAPIView(generics.ListAPIView):

    from question_answer.serializers import QuestionAnswerSerializer

    serializer_class = QuestionAnswerSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        Teacher = apps.get_model("teachers", "Teacher")
        QuestionAnswer = apps.get_model("question_answer", "QuestionAnswer")

        teacher_id = self.kwargs['teacher_id']
        teacher = Teacher.objects.get(id=teacher_id)
        return QuestionAnswer.objects.filter(course__teacher=teacher)


class TeacherCouponListCreateAPIView(generics.ListCreateAPIView):

    from teachers.serializers import CouponSerializer

    serializer_class = CouponSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        Teacher = apps.get_model("teachers", "Teacher")
        Coupon = apps.get_model("teachers", "Coupon")

        teacher_id = self.kwargs['teacher_id']
        teacher = Teacher.objects.get(id=teacher_id)
        return Coupon.objects.filter(teacher=teacher)


class TeacherCouponDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    from teachers.serializers import CouponSerializer

    serializer_class = CouponSerializer
    permission_classes = [AllowAny]

    def get_object(self):

        Teacher = apps.get_model("teachers", "Teacher")
        Coupon = apps.get_model("teachers", "Coupon")

        teacher_id = self.kwargs['teacher_id']
        coupon_id = self.kwargs['coupon_id']
        teacher = Teacher.objects.get(id=teacher_id)
        return Coupon.objects.get(teacher=teacher, id=coupon_id)


class TeacherNotificationListAPIView(generics.ListAPIView):

    from notifications.serializers import NotificationSerializer

    serializer_class = NotificationSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        Teacher = apps.get_model("teachers", "Teacher")
        Notification = apps.get_model("notifications", "Notification")

        teacher_id = self.kwargs['teacher_id']
        teacher = Teacher.objects.get(id=teacher_id)
        return Notification.objects.filter(teacher=teacher, seen=False)


class TeacherNotificationDetailAPIView(generics.RetrieveUpdateAPIView):

    from notifications.serializers import NotificationSerializer

    serializer_class = NotificationSerializer
    permission_classes = [AllowAny]

    def get_object(self):

        Teacher = apps.get_model("teachers", "Teacher")
        Notification = apps.get_model("notifications", "Notification")

        teacher_id = self.kwargs['teacher_id']
        noti_id = self.kwargs['noti_id']
        teacher = Teacher.objects.get(id=teacher_id)
        return Notification.objects.get(teacher=teacher, id=noti_id)

