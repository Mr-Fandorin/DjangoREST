from celery import shared_task
from django.core.mail import send_mail
from materials.models import CourseSubscription

from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta


@shared_task
def send_course_update_email(course_id, course_name):
    """
    Отправляет письмо всем подписчикам курса об обновлении.
    """
    subscribers = CourseSubscription.objects.filter(course_id=course_id).select_related('user')

    subject = f"Обновление курса: {course_name}"
    message = f"Курс '{course_name}' был обновлен! Проверьте новые материалы."
    from_email = "no-reply@yourdomain.com"  # Или из настроек

    recipients = []
    for sub in subscribers:
        if sub.user.email:
            recipients.append(sub.user.email)

    if recipients:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipients,
            fail_silently=False,
        )
    return f"Отправлено писем: {len(recipients)}"


User = get_user_model()


@shared_task
def deactivate_inactive_users():
    """
    Блокирует пользователей, которые не заходили более 30 дней.
    """
    cutoff_date = timezone.now() - timedelta(days=30)

    inactive_users = User.objects.filter(
        is_active=True,
        last_login__lt=cutoff_date
    )

    count = inactive_users.update(is_active=False)

    return f"Заблокировано пользователей: {count}"