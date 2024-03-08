from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson
from django.utils.translation import gettext_lazy as _

NULLABLE = {
    'null': True,
    'blank': True,
}

PAYMENT_CHOICES = (
    ('card', 'карта'),
    ('cash', 'наличные'),
)


class UserRoles(models.TextChoices):
    MEMBER = 'member', _('member')
    MODERATOR = 'moderator', _('moderator')


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    phone = models.CharField(max_length=50, verbose_name='номер телефона', **NULLABLE)
    city = models.CharField(max_length=100, verbose_name='город', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    role = models.CharField(max_length=20, choices=UserRoles.choices, default=UserRoles.MEMBER, verbose_name='роль')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('pk',)


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)
    payment_date = models.DateField(auto_now_add=True, verbose_name='дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='урок', **NULLABLE)
    amount = models.PositiveIntegerField(verbose_name='стоимость', **NULLABLE)
    payment_method = models.CharField(max_length=50, verbose_name='метод оплаты', choices=PAYMENT_CHOICES,
                                      default='card')

    def __str__(self):
        return f'{self.course if self.course else self.lesson} - {self.payment_date}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
        ordering = ('-payment_date',)

