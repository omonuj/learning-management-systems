import math
import os

from distutils.util import strtobool
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from moviepy.video.io.VideoFileClip import VideoFileClip
from rest_framework import generics, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from courses import serializers as courses_serializer
from django.apps import apps


# Create your views here.
class CategoryListView(generics.ListAPIView):
    Category = apps.get_model('courses', 'Category')
    queryset = Category.objects.all()
    serializer_class = courses_serializer.CategorySerializer
    permission_classes = [AllowAny]



class CourseListAPIView(generics.ListAPIView):
    Courses = apps.get_model('courses', 'Courses')
    queryset = Courses.objects.filter(platform_status="Published", teacher_course_status="Published")
    serializer_class = courses_serializer.CourseSerializer
    permission_classes = [AllowAny]



class SearchCourseAPIView(generics.ListAPIView):
    serializer_class = courses_serializer.CourseSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        query = self.request.GET.get('query')
        # learn lms
        Courses = apps.get_model("courses", "Courses")
        return Courses.objects.filter(title__icontains=query, platform_status="Published",
                                                      teacher_course_status="Published")


class StudentNoteCreateAPIView(generics.ListCreateAPIView):
    serializer_class = courses_serializer.NoteSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        enrollment_id = self.kwargs['enrollment_id']

        User = apps.get_model('users', 'User')
        Note = apps.get_model('courses', 'Note')

        user = User.objects.get(id=user_id)
        EnrolledCourse = apps.get_model('courses.EnrolledCourse', 'EnrolledCourse')
        enrolled = EnrolledCourse.objects.get(enrollment_id=enrollment_id)

        return Note.objects.filter(user=user, course=enrolled.course)

    def create(self, request, *args, **kwargs):
        user_id = request.data['user_id']
        enrollment_id = request.data['enrollment_id']
        title = request.data['title']
        note = request.data['note']

        User = apps.get_model('users', 'User')
        Note = apps.get_model('courses', 'Note')

        user = User.objects.get(id=user_id)
        EnrolledCourse = apps.get_model("courses.EnrolledCourse", "EnrolledCourse")
        enrolled = EnrolledCourse.objects.get(enrollment_id=enrollment_id)

        Note.objects.create(user=user, course=enrolled.course, note=note, title=title)

        return Response({"message": "Note created successfully"}, status=status.HTTP_201_CREATED)



class StudentNoteDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = courses_serializer.NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user_id = self.kwargs['user_id']
        enrollment_id = self.kwargs['enrollment_id']
        note_id = self.kwargs['note_id']

        User = apps.get_model('users', 'User')
        Note = apps.get_model('courses', 'Note')

        user = User.objects.get(id=user_id)
        EnrolledCourse = apps.get_model("courses.EnrolledCourse", "EnrolledCourse")
        enrolled = EnrolledCourse.objects.get(enrollment_id=enrollment_id)
        note = Note.objects.get(user=user, course=enrolled.course, id=note_id)
        return note


class StudentRateCourseCreateAPIView(generics.CreateAPIView):
    serializer_class = courses_serializer.ReviewSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        user_id = request.data['user_id']
        course_id = request.data['course_id']
        rating = request.data['rating']
        review = request.data['review']

        User = apps.get_model('users', 'User')
        Courses = apps.get_model('courses', 'Courses')
        Review = apps.get_model('courses', 'Review')

        user = User.objects.get(id=user_id)
        course = Courses.objects.get(id=course_id)

        Review.objects.create(
            user=user,
            course=course,
            review=review,
            rating=rating,
            active=True,
        )

        return Response({"message": "Review created successfully"}, status=status.HTTP_201_CREATED)


class StudentRateCourseUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = courses_serializer.ReviewSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        user_id = self.kwargs['user_id']
        review_id = self.kwargs['review_id']

        User = apps.get_model('users', 'User')
        Review = apps.get_model('courses', 'Review')

        user = User.objects.get(id=user_id)
        return Review.objects.get(id=review_id, user=user)


class StudentWishListListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = courses_serializer.WishListSerializerShallow
    permission_classes = [AllowAny]

    def get_queryset(self):

        User = apps.get_model('users', 'User')
        WishList = apps.get_model('courses', 'WishList')

        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)
        return WishList.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        user_id = request.data['user_id']
        course_id = request.data['course_id']

        User = apps.get_model('users', 'User')
        WishList = apps.get_model('courses', 'WishList')
        Courses = apps.get_model('courses', 'Courses')

        user = User.objects.get(id=user_id)
        course = Courses.objects.get(id=course_id)

        wishlist = WishList.objects.filter(user=user, course=course).first()
        if wishlist:
            wishlist.delete()
            return Response({"message": "Wishlist Deleted"}, status=status.HTTP_200_OK)
        else:
            WishList.objects.create(
                user=user, course=course
            )
            return Response({"message": "Wishlist Created"}, status=status.HTTP_201_CREATED)


class CourseCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        title = request.data.get("title")
        description = request.data.get("description")
        image = request.data.get("image")
        file = request.data.get("file")
        level = request.data.get("level")
        language = request.data.get("language")
        price = request.data.get("price")
        category = request.data.get("category")

        Category = apps.get_model('courses', 'Category')
        Courses = apps.get_model('courses', 'Courses')

        category_obj = Category.objects.filter(id=category).first()
        Teacher = apps.get_model("teachers", "Teacher")
        teacher = Teacher.objects.get(user=request.user)

        course = Courses.objects.create(
            teacher=teacher,
            category=category_obj,
            file=file,
            image=image,
            title=title,
            description=description,
            price=price,
            language=language,
            level=level
        )

        return Response({"message": "Course Created", "course_id": course.course_id}, status=status.HTTP_201_CREATED)


class CourseUpdateAPIView(generics.RetrieveUpdateAPIView):

    Courses = apps.get_model("courses", 'Courses')

    queryset = Courses.objects.all()
    serializer_class = courses_serializer.CourseSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        teacher_id = self.kwargs['teacher_id']
        course_id = self.kwargs['course_id']

        Teacher = apps.get_model("teachers", "Teacher")
        Courses = apps.get_model('courses', 'Courses')

        teacher = Teacher.objects.get(id=teacher_id)
        course = Courses.objects.get(course_id=course_id)

        return course

    def update(self, request, *args, **kwargs):

        Category = apps.get_model('courses', 'Category')

        course = self.get_object()
        serializer = self.get_serializer(course, data=request.data)
        serializer.is_valid(raise_exception=True)

        if "image" in request.data and isinstance(request.data['image'], InMemoryUploadedFile):
            course.image = request.data['image']
        elif 'image' in request.data and str(request.data['image']) == "No File":
            course.image = None

        if 'file' in request.data and not str(request.data['file']).startswith("https://"):
            course.file = request.data['file']

        if 'category' in request.data['category'] and request.data['category'] != 'NaN' and request.data[
            'category'] != "undefined":
            category = Category.objects.get(id=request.data['category'])
            course.category = category

        self.perform_update(serializer)
        self.update_variant(course, request.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update_variant(self, course, request_data):

        VariantItem = apps.get_model("courses", "VariantItem")
        Variant = apps.get_model("courses", "Variant")

        for key, value in request_data.items():
            if key.startswith("variants") and '[variant_title]' in key:

                index = key.split('[')[1].split(']')[0]
                title = value

                id_key = f"variants[{index}][variant_id]"
                variant_id = request_data.get(id_key)

                variant_data = {'title': title}
                item_data_list = []
                current_item = {}

                for item_key, item_value in request_data.items():
                    if f'variants[{index}][items]' in item_key:
                        field_name = item_key.split('[')[-1].split(']')[0]
                        if field_name == "title":
                            if current_item:
                                item_data_list.append(current_item)
                            current_item = {}
                        current_item.update({field_name: item_value})

                if current_item:
                    item_data_list.append(current_item)

                existing_variant = course.variant_set.filter(id=variant_id).first()

                if existing_variant:
                    existing_variant.title = title
                    existing_variant.save()

                    for item_data in item_data_list[1:]:
                        preview_value = item_data.get("preview")
                        preview = bool(strtobool(str(preview_value))) if preview_value is not None else False

                        variant_item = VariantItem.objects.filter(
                            variant_item_id=item_data.get("variant_item_id")).first()

                        if not str(item_data.get("file")).startswith("https://"):
                            if item_data.get("file") != "null":
                                file = item_data.get("file")
                            else:
                                file = None

                            title = item_data.get("title")
                            description = item_data.get("description")

                            if variant_item:
                                variant_item.title = title
                                variant_item.description = description
                                variant_item.file = file
                                variant_item.preview = preview
                            else:
                                variant_item = VariantItem.objects.create(
                                    variant=existing_variant,
                                    title=title,
                                    description=description,
                                    file=file,
                                    preview=preview
                                )

                        else:
                            title = item_data.get("title")
                            description = item_data.get("description")

                            if variant_item:
                                variant_item.title = title
                                variant_item.description = description
                                variant_item.preview = preview
                            else:
                                variant_item = VariantItem.objects.create(
                                    variant=existing_variant,
                                    title=title,
                                    description=description,
                                    preview=preview
                                )

                        variant_item.save()

                else:
                    new_variant = Variant.objects.create(
                        course=course, title=title
                    )

                    for item_data in item_data_list:
                        preview_value = item_data.get("preview")
                        preview = bool(strtobool(str(preview_value))) if preview_value is not None else False

                        VariantItem.objects.create(
                            variant=new_variant,
                            title=item_data.get("title"),
                            description=item_data.get("description"),
                            file=item_data.get("file"),
                            preview=preview,
                        )

    def save_nested_data(self, course_instance, serializer_class, data):
        serializer = serializer_class(data=data, many=True, context={"course_instance": course_instance})
        serializer.is_valid(raise_exception=True)
        serializer.save(course=course_instance)


class CourseDetailAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = courses_serializer.CourseSerializer
    permission_classes = [AllowAny]

    def get_object(self):

        Courses = apps.get_model("courses", "Courses")

        slug = self.kwargs['slug']
        return Courses.objects.get(slug=slug)


class CourseVariantDeleteAPIView(generics.DestroyAPIView):
    serializer_class = courses_serializer.VariantSerializer
    permission_classes = [AllowAny]

    def get_object(self):

        Teacher = apps.get_model("teachers", "Teacher")
        Courses = apps.get_model("courses", "Courses")
        Variant = apps.get_model("courses", "Variant")

        variant_id = self.kwargs['variant_id']
        teacher_id = self.kwargs['teacher_id']
        course_id = self.kwargs['course_id']

        print("variant_id ========", variant_id)

        teacher = Teacher.objects.get(id=teacher_id)
        course = Courses.objects.get(teacher=teacher, course_id=course_id)
        return Variant.objects.get(id=variant_id)


class CourseVariantItemDeleteAPIVIew(generics.DestroyAPIView):
    serializer_class = courses_serializer.VariantItemSerializerShallow
    permission_classes = [IsAuthenticated]

    def get_object(self):

        Teacher = apps.get_model("teachers", "Teacher")
        Courses = apps.get_model("courses", "Courses")
        Variant = apps.get_model("courses", "Variant")
        VariantItem = apps.get_model("courses", "VariantItem")

        variant_id = self.kwargs['variant_id']
        variant_item_id = self.kwargs['variant_item_id']
        teacher_id = self.kwargs['teacher_id']
        course_id = self.kwargs['course_id']

        teacher = Teacher.objects.get(id=teacher_id)
        course = Courses.objects.get(teacher=teacher, course_id=course_id)
        variant = Variant.objects.get(variant_id=variant_id, course=course)
        return VariantItem.objects.get(variant=variant, variant_item_id=variant_item_id)


class FileUploadAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser,)  # Allow file uploads

    @swagger_auto_schema(
        operation_description="Upload a file",
        request_body=courses_serializer.FileUploadSerializer,  # Use the serializer here
        responses={
            200: openapi.Response('File uploaded successfully', openapi.Schema(type=openapi.TYPE_OBJECT)),
            400: openapi.Response('No file provided', openapi.Schema(type=openapi.TYPE_OBJECT)),
        }
    )
    def post(self, request):

        serializer = courses_serializer.FileUploadSerializer(data=request.data)

        if serializer.is_valid():
            file = serializer.validated_data.get("file")

            # Save the file to the media directory
            file_path = default_storage.save(file.name, ContentFile(file.read()))
            file_url = request.build_absolute_uri(default_storage.url(file_path))

            # Check if the file is a video by inspecting its extension
            if file.name.endswith(('.mp4', '.avi', '.mov', '.mkv')):
                # Calculate the video duration
                file_full_path = os.path.join(default_storage.location, file_path)
                clip = VideoFileClip(file_full_path)
                duration_seconds = clip.duration

                # Calculate minutes and seconds
                minutes, remainder = divmod(duration_seconds, 60)
                minutes = math.floor(minutes)
                seconds = math.floor(remainder)

                duration_text = f"{minutes}m {seconds}s"

                print("url ==========", file_url)
                print("duration_seconds ==========", duration_seconds)

                # Return both the file URL and the video duration
                return Response({
                    "url": file_url,
                    "video_duration": duration_text
                })

            # If not a video, just return the file URL
            return Response({
                "url": file_url,
            })

        return Response({"error": "No file provided"}, status=400)


class StudentSummaryAPIView(generics.ListAPIView):
    from courses.serializers import StudentSummarySerializer
    serializer_class = StudentSummarySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        User = apps.get_model("users", "User")
        EnrolledCourse = apps.get_model("certificates", "EnrolledCourse")
        CompletedLessons = apps.get_model("certificates", "CompletedLessons")
        Certificate = apps.get_model("certificates", "Certificate")

        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)
        total_courses = EnrolledCourse.objects.filter(user=user).count()
        completed_lessons = CompletedLessons.objects.filter(user=user).count()
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

    EnrolledCourse = apps.get_model("certificates", "EnrolledCourse")

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
        Courses = apps.get_model("courses", "Courses")
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



class TeacherCourseDetailAPIView(generics.RetrieveAPIView):

    from courses.serializers import CourseSerializer
    Courses = apps.get_model("courses", "Courses")

    serializer_class = CourseSerializer
    permission_classes = [AllowAny]
    queryset = Courses.objects.filter(platform_status="Published", teacher_course_status="Published")

    def get_object(self):

        Courses = apps.get_model("courses", "Courses")

        course_id = self.kwargs['course_id']
        course = Courses.objects.get(course_id=course_id, platform_status="Published",
                                               teacher_course_status="Published")
        return course


class CouponApplyAPIView(generics.CreateAPIView):

    from teachers.serializers import CouponSerializer

    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        CartOrder = apps.get_model("carts", "CartOrder")
        Coupon = apps.get_model("teachers", "Coupon")
        CartOrderItem = apps.get_model("carts", "CartOrderItem")

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

