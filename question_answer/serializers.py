from rest_framework import serializers
from django.apps import apps


class QuestionAnswerMessageSerializerShallow(serializers.ModelSerializer):

    class Meta:

        QuestionAnswerMessage = apps.get_model('question_answer', 'QuestionAnswerMessage')

        fields = '__all__'
        model = QuestionAnswerMessage
        depth = 0


class QuestionAnswerMessageSerializerDeep(serializers.ModelSerializer):
    class Meta:

        QuestionAnswerMessage = apps.get_model('question_answer', 'QuestionAnswerMessage')


        fields = '__all__'
        model = QuestionAnswerMessage
        depth = 3


class QuestionAnswerSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()
    profile = serializers.SerializerMethodField()

    class Meta:

        QuestionAnswer = apps.get_model('question_answer', 'QuestionAnswer')

        fields = ("courses", "messages", "profile", "user", "title",
                  "qa_id", "datetime"
        )
        model = QuestionAnswer

    def get_profile(self, obj):
        if obj.profile:
            return {
                "id": obj.profile.id,
                "full_name": obj.profile.full_name,
                "image": obj.profile.image.url if obj.profile.image else None,
            }
        return None

    def get_messages(self, obj):
        return obj.messages.count()