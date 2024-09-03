from rest_framework import serializers
from django.apps import apps



class CategorySerializer(serializers.ModelSerializer):
    course_count = serializers.SerializerMethodField()

    class Meta:
        Category = apps.get_model('courses', 'Category')
        fields = ['id', 'title', 'image', 'slug', 'course_count']
        model = Category

    def get_course_count(self, obj):
        return obj.courses.count()


class VariantItemSerializerShallow(serializers.ModelSerializer):
    class Meta:
        VariantItem = apps.get_model('courses', 'VariantItem')
        fields = '__all__'
        model = VariantItem


class VariantItemSerializerDeep(serializers.ModelSerializer):
    class Meta:
        VariantItem = apps.get_model('courses', 'VariantItem')
        fields = '__all__'
        model = VariantItem
        depth = 3


class VariantSerializer(serializers.ModelSerializer):
    variant_items = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    class Meta:
        Variant = apps.get_model('courses', 'Variant')
        fields = (
            "courses", "title", "variant_id", "datetime", "variant_items", "items"
        )
        model = Variant

    def get_variant_items(self, obj):
        return obj.variant_items.count()

    def get_items(self, obj):
        return VariantItemSerializerDeep(obj.variant_items.all(), many=True).data


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        Note = apps.get_model('courses', 'Note')
        fields = '__all__'
        model = Note


class ReviewSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        Review = apps.get_model('courses', 'Review')
        fields = (
            "profile", "courses", "user", "datetime", "review",
            "reply", "active", "ratings"
        )
        model = Review

    def get_profile(self, obj):
        if obj.profile:
            return {
                "id": obj.profile.id,
                "full_name": obj.profile.full_name,
                "image": obj.profile.image.url if obj.profile.image else None,
            }
        return None

class WishListSerializerShallow(serializers.ModelSerializer):
    class Meta:
        WishList = apps.get_model('courses', 'WishList')
        fields = '__all__'
        model = WishList
        depth = 0


class WishListSerializerDeep(serializers.ModelSerializer):
    class Meta:
        WishList = apps.get_model('courses', 'WishList')
        fields = '__all__'
        model = WishList
        depth = 3


class CountrySerializerShallow(serializers.ModelSerializer):
    class Meta:
        Country = apps.get_model('courses', 'Country')
        fields = '__all__'
        model = Country
        depth = 0


class CountrySerializerDeep(serializers.ModelSerializer):
    class Meta:
        Country = apps.get_model('courses', 'Country')
        fields = '__all__'
        model = Country
        deep = 3


class CourseSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    curriculum = serializers.SerializerMethodField()
    lecture = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    average_ratings = serializers.SerializerMethodField()

    class Meta:
        Courses = apps.get_model('courses', 'Courses')
        fields = ("category", "teachers", "image", "title", "description",
                  "price", "language", "level","platform_status",
                  "teacher_course_status", "featured", "course_id",
                  "slug", "datetime", "student", "curriculum",
                 "lecture", "average_ratings", "rating_count", "reviews",
                  "introduction_video_file", "student", "rating_count",
                  "average_ratings",
                  )
        model = Courses

    def get_student(self, obj):
        return obj.student().count()

    def get_curriculum(self, obj):
        items = obj.curriculum()
        return [{"title": i.title, "description": i.description} for i in items]

    def get_lecture(self, obj):
        items = obj.lecture()
        return [{"title": i.title, "video": i.video.url if i.video else None} for i in items]

    def get_reviews(self, obj):
        reviews = obj.reviews()
        return ReviewSerializer(reviews, many=True).data

    def get_rating_count(self, obj):
        return obj.rating_count()

    def get_average_ratings(self, obj):
        avg = obj.average_ratings()
        return round(avg, 1) if avg else 0


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class StudentSummarySerializer(serializers.Serializer):
    total_courses = serializers.IntegerField()
    completed_lessons = serializers.IntegerField()
    achieved_certificates = serializers.IntegerField()

