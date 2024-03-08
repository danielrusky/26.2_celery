from rest_framework.serializers import ValidationError
from rest_framework_simplejwt import serializers


class YoutubeUrlValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, attrs):
        url = attrs.get(self.field)
        if url and not url.startswith('https://www.youtube.com/watch?v='):
            raise serializers.ValidationError('Недопустимая ссылка на видео')