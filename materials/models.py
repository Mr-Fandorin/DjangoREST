from django.db import models

from users.models import User


class Course(models.Model):
    course_name = models.CharField(max_length=200, verbose_name="Название курса")
    photo = models.ImageField(
        upload_to="course/photo", null=True, blank=True, verbose_name="Изображение"
    )
    description = models.TextField(null=True, blank=True, verbose_name="Описание курса")

    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец",
        help_text="Укажите владельца курса",
    )

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    lesson_name = models.CharField(max_length=150, verbose_name="Название урока")
    description = models.TextField(null=True, blank=True, verbose_name="Описание урока")
    photo = models.ImageField(
        upload_to="lesson/photo", null=True, blank=True, verbose_name="Изображение"
    )
    video_url = models.URLField(
        max_length=500, null=True, blank=True, verbose_name="Ссылка на видео"
    )

    course_name = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Название курса",
        related_name="lesson_name",
        null=True,
        blank=True,
    )

    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец",
        help_text="Укажите владельца урока",
    )

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"

class CourseSubscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='course_subscriptions',
        verbose_name="Пользователь"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name="Курс"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подписки")

    class Meta:
        verbose_name = "подписка на курс"
        verbose_name_plural = "подписки на курсы"
        unique_together = ('user', 'course')




