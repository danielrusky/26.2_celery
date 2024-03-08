from django.db import models
from django.conf import settings

NULLABLE = {
    'null': True,
    'blank': True,
}

PAYMENT_CHOICES = (
    ('card', 'карта'),
    ('cash', 'наличные'),
)


class Course(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)
    title = models.CharField(max_length=200, verbose_name='название')
    image = models.ImageField(upload_to='materials/course/', verbose_name='картинка', **NULLABLE)
    description = models.TextField(verbose_name='описание', **NULLABLE)
    price = models.PositiveIntegerField(verbose_name='стоимость', **NULLABLE)
    last_update = models.DateTimeField(verbose_name='последнее обновление', auto_now=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    title = models.CharField(max_length=200, verbose_name='название')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    image = models.ImageField(upload_to='materials/lesson/', verbose_name='картинка', **NULLABLE)
    url_video = models.URLField(verbose_name='ссылка на видео', **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions',
                              verbose_name='владелец', **NULLABLE)

    def __str__(self):
        return f'{self.user} - {self.course}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
