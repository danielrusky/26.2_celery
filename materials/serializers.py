from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from materials.validators import YoutubeUrlValidator

from materials.models import Course, Lesson, Subscription


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [
            YoutubeUrlValidator(field='url_video'),
            serializers.UniqueTogetherValidator(
                queryset=Lesson.objects.all(),
                fields=('title', 'description'),
            ),
        ]


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)
    is_subscribed = SerializerMethodField()

    def get_count_lessons(self, obj):
        return Lesson.objects.filter(course=obj).count()

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        is_subscribed = Subscription.objects.filter(user=user, course=obj).exists()
        return is_subscribed

    class Meta:
        model = Course
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
