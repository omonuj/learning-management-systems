from rest_framework import serializers
from django.apps import apps


class CertificateSerializerShallow(serializers.ModelSerializer):
    class Meta:
        Certificate = apps.get_model('certificates', 'Certificate')

        fields = '__all__'
        model = Certificate
        depth = 0


class CertificateSerializerDeep(serializers.ModelSerializer):
    class Meta:

        Certificate = apps.get_model('certificates', 'Certificate')

        fields = '__all__'
        model = Certificate
        depth = 3


class CompletedLessonSerializerShallow(serializers.ModelSerializer):
    class Meta:

        CompletedLesson = apps.get_model('certificates', 'CompletedLessons')

        fields = '__all__'
        model = CompletedLesson
        depth = 0


class CompletedLessonSerializerDeep(serializers.ModelSerializer):
    class Meta:

        CompletedLesson = apps.get_model('certificates', 'CompletedLessons')

        fields = '__all__'
        model = CompletedLesson
        depth = 3


class EnrolledCourseSerializer(serializers.ModelSerializer):
    lectures = serializers.SerializerMethodField()
    completed_lesson = serializers.SerializerMethodField()
    curriculum =  serializers.SerializerMethodField()
    note = serializers.SerializerMethodField()
    question_answer = serializers.SerializerMethodField()
    review = serializers.SerializerMethodField()


    class Meta:

        EnrolledCourse = apps.get_model('certificates', 'EnrolledCourse')

        fields = (
            "courses", "user", "teacher", "order_item", "datetime",
            "enrollment_id", "lectures", "completed_lesson", "curriculum",
            "note", "question_answer", "review"
        )
        model = EnrolledCourse


    def get_lectures(self, obj):
        return [
            {
                "title": lecture.title,
                "description": lecture.description,
                "video_url": lecture.video.url if lecture.video else None,
            }
            for lecture in obj.lectures()
        ]

    def get_completed_lesson(self, obj):
        return obj.completed_lessons().count()

    def get_curriculum(self, obj):
        return [
            {
                "title": curriculum.title,
                "description": curriculum.description,
            }
            for curriculum in obj.curriculum()
        ]

    def get_note(self, obj):
        return [
            {
                "title": note.title,
                "note": note.note,
                "datetime": note.datetime,
            }
            for note in obj.note()
        ]

    def get_question_answer(self, obj):
        return [
            {
                "question": qa.question,
                "answer": qa.answer,
                "datetime": qa.datetime,
            }
            for qa in obj.question_answer()
        ]

    def get_review(self, obj):
        review = obj.review()
        if review:
            return {
                "review": review.review,
                "rating": review.ratings,
                "reply": review.reply,
                "datetime": review.datetime,
            }
        return None











