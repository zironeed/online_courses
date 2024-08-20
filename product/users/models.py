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

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='balance',
        verbose_name='Пользователь'
    )
    balance = models.PositiveIntegerField(
        default=1000,
        verbose_name='Баланс'
    )

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
        "courses.Course",
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Курс'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активная подписка'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-id',)

