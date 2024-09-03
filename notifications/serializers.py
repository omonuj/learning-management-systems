from rest_framework import serializers
from django.apps import apps

class NotificationSerializer(serializers.ModelSerializer):

    class Meta:

        Notification = apps.get_model('notifications', 'Notification')

        fields = '__all__'
        model = Notification