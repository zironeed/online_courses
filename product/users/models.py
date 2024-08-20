from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """Кастомная модель пользователя - студента."""

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=250,
        unique=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.get_full_name()

    def has_access_to_course(self, course):
        return self.subscriptions.filter(course=course, active=True).exists()


class Balance(models.Model):
    """Модель баланса пользователя."""


    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
        ordering = ('-id',)


class Subscription(models.Model):
    """Модель подписки пользователя на курс."""

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Пользователь'
    )
    course = models.ForeignKey(
        "Course",
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Курс'
    )
    start_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата начала подписки'
    )
    end_date = models.DateTimeField(
        verbose_name='Дата окончания подписки'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активная подписка'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-id',)

