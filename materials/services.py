import stripe
from config import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_course_payment(course, price):
    product_stripe = stripe.Product.create(name=course)

    price_stripe = stripe.Price.create(
        currency="usd",
        unit_amount=price,
        recurring={"interval": "month"},
        product_data={"name": product_stripe},
    )

    session_stripe = stripe.checkout.Session.create(
        mode="subscription",
        success_url="https://example.com/success",
        line_items=[
            {
                "price": price_stripe.id,
                "quantity": 1,
            }
        ]
    )

    return session_stripe


course = 'test course 1'
price = 3500

result = create_course_payment(course, price)
print(result)