from rest_framework import serializers
from django.apps import apps


class TeacherSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()
    students = serializers.SerializerMethodField()
    courses = serializers.SerializerMethodField()

    class Meta:

        Teacher = apps.get_model('teachers', 'Teacher')

        fields = ["user", "image", "full_name", "bio",
                  "facebook", "twitter", "linkedin", "about",
                  "country", "students", "courses", "reviews"]
        model = Teacher

    def get_reviews(self, obj):
        return obj.reiew()

    def get_students(self, obj):
        return obj.students.count()

    def get_courses(self, obj):
        return obj.courses.count()


class TeacherSummarySerializer(serializers.Serializer):
    total_courses = serializers.IntegerField()
    total_students = serializers.IntegerField()
    total_revenue = serializers.IntegerField()
    monthly_revenue = serializers.IntegerField()

    class Meta:

        fields = ['total_courses', 'total_revenue', 'monthly_revenue',

                  ]


class CouponSerializer(serializers.ModelSerializer):
    class Meta:

        Coupon = apps.get_model('teachers', 'Coupon')

        fields = '__all__'
        model = Coupon
