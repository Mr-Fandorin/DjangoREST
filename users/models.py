from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson

from django.conf import settings
from django.core.exceptions import ValidationError


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Email", help_text="Введите email"
    )
    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Введите номер телефона",
    )
    city = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Укажите ваш город",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/", blank=True, null=True, verbose_name="Аватар"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    # def __str__(self):
    #     return self.email





class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счёт'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Пользователь'
    )

    paid_course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='course_payments',
        verbose_name='Оплаченный курс'
    )

    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lesson_payments',
        verbose_name='Оплаченный урок'
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма оплаты'
    )

    payment_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата оплаты'
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='transfer',
        verbose_name='Способ оплаты'
    )

    def clean(self):
        if self.paid_course and self.paid_lesson:
            raise ValidationError("Можно указать либо курс, либо урок, но не оба одновременно.")
        if not self.paid_course and not self.paid_lesson:
            raise ValidationError("Необходимо указать либо курс, либо урок.")

    def __str__(self):
        return f"{self.user.email} — {self.amount} руб. ({self.get_payment_method_display()})"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
