import stripe
from django.conf import settings

from materials.models import Course

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product_and_price(course: Course) -> dict:
    """Создает продукт и цену в Stripe, если их еще нет."""
    if not course.stripe_product_id:
        stripe_product = stripe.Product.create(
            name=course.course_name,
            description=course.description or "",
        )
        course.stripe_product_id = stripe_product.id

    if not course.stripe_price_id:
        unit_amount = int(course.price * 100)  # Конвертируем в копейки
        stripe_price = stripe.Price.create(
            product=course.stripe_product_id,
            unit_amount=unit_amount,
            currency=course.currency.lower(),
        )
        course.stripe_price_id = stripe_price.id

    course.save()
    return {"product_id": course.stripe_product_id, "price_id": course.stripe_price_id}


def create_checkout_session(course: Course) -> dict:
    """Создает сессию оплаты и возвращает ссылку."""
    create_stripe_product_and_price(course)

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": course.stripe_price_id,
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url="http://127.0.0.1:8000/",
        metadata={
            "course_id": str(course.id),
        },
    )
    return {
        "url": session.url,
        "session_id": session.id,
    }
