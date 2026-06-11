from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from materials.models import Course, Lesson
from users.models import Payment

User = get_user_model()


class Command(BaseCommand):
    help = "Создаёт тестовые записи платежей (ИСПРАВЛЕНО ПОД ТВОИ МОДЕЛИ)"

    def handle(self, *args, **options):
        # --- 1. Пользователи ---
        user1, _ = User.objects.get_or_create(
            email="ivan@test.com", defaults={"is_active": True}
        )
        if _:
            user1.set_password("123")
            user1.save()

        user2, _ = User.objects.get_or_create(
            email="maria@test.com", defaults={"is_active": True}
        )
        if _:
            user2.set_password("123")
            user2.save()

        # --- 2. Курс ---
        course1, _ = Course.objects.get_or_create(
            course_name="Курс по Python",
            defaults={"description": "Базовый курс по Python"},
        )

        # --- 3. Урок ---
        # ИСПРАВЛЕНИЕ 1: lesson_name вместо title
        # ИСПРАВЛЕНИЕ 2: course_name=course1 (так как в модели FK назван course_name)
        # ИСПРАВЛЕНИЕ 3: description вместо content (в модели нет поля content!)
        lesson1, _ = Lesson.objects.get_or_create(
            lesson_name="Урок 1: Введение в Python",
            course_name=course1,
            defaults={"description": "Привет, мир!"},
        )

        # --- 4. Очистка старых платежей ---
        Payment.objects.filter(
            user__email__in=["ivan@test.com", "maria@test.com"]
        ).delete()

        # --- 5. Создание платежей ---
        Payment.objects.create(
            user=user1,
            paid_course=course1,
            amount=1500.00,
            payment_method="transfer",
        )

        Payment.objects.create(
            user=user2,
            paid_lesson=lesson1,
            amount=500.00,
            payment_method="cash",
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Успешно создано 2 записи платежей (1 за курс, 1 за урок)"
            )
        )
