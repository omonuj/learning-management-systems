from django.shortcuts import redirect
from rest_framework import generics, status
from django.apps import apps
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from decimal import Decimal
import stripe
import requests

from learning import settings

stripe.api_key = settings.STRIPE_SECRET_KEY
STRIPE_PUBLISHABLE_KEY = settings.STRIPE_PUBLISHABLE_KEY
PAYPAL_CLIENT_ID = settings.PAYPAL_CLIENT_ID
PAYPAL_SECRET_ID = settings.PAYPAL_SECRET_ID



# Create your views here.
class CartAPIView(generics.CreateAPIView):

    Cart = apps.get_model('carts', 'Cart')
    from carts.serializers import CartSerializerShallow

    queryset = Cart.objects.all()
    serializer_class = CartSerializerShallow
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):

        Courses = apps.get_model("courses", "Courses")
        User = apps.get_model("users", "User")
        Country = apps.get_model("courses", "Country")
        Cart = apps.get_model("carts", "Cart")

        course_id = request.data['course_id']
        user_id = request.data['user_id']
        price = request.data['price']
        country_name = request.data['country_name']
        cart_id = request.data['cart_id']

        print("course_id ==========", course_id)

        course = Courses.objects.filter(id=course_id).first()

        if user_id != "undefined":
            user = User.objects.filter(id=user_id).first()
        else:
            user = None

        try:
            country_object = Country.objects.filter(name=country_name).first()
            country = country_object.name
        except:
            country_object = None
            country = "United States"

        if country_object:
            tax_rate = country_object.tax_rate / 100
        else:
            tax_rate = 0

        cart = Cart.objects.filter(cart_id=cart_id, course=course).first()

        if cart:
            cart.course = course
            cart.user = user
            cart.price = price
            cart.tax_fee = Decimal(price) * Decimal(tax_rate)
            cart.country = country
            cart.cart_id = cart_id
            cart.total = Decimal(cart.price) + Decimal(cart.tax_fee)
            cart.save()

            return Response({"message": "Cart Updated Successfully"}, status=status.HTTP_200_OK)

        else:
            cart = Cart()

            cart.course = course
            cart.user = user
            cart.price = price
            cart.tax_fee = Decimal(price) * Decimal(tax_rate)
            cart.country = country
            cart.cart_id = cart_id
            cart.total = Decimal(cart.price) + Decimal(cart.tax_fee)
            cart.save()

            return Response({"message": "Cart Created Successfully"}, status=status.HTTP_201_CREATED)


class CartListAPIView(generics.ListAPIView):

    from carts.serializers import CartSerializerDeep

    serializer_class = CartSerializerDeep
    permission_classes = [AllowAny]

    def get_queryset(self):

        Cart = apps.get_model('carts', 'Cart')

        cart_id = self.kwargs['cart_id']
        queryset = Cart.objects.filter(cart_id=cart_id)
        return queryset


class CartItemDeleteAPIView(generics.DestroyAPIView):

    from carts.serializers import CartSerializerShallow

    serializer_class = CartSerializerShallow
    permission_classes = [AllowAny]

    def get_object(self):

        Cart = apps.get_model('carts', 'Cart')

        cart_id = self.kwargs['cart_id']
        item_id = self.kwargs['item_id']

        return Cart.objects.filter(cart_id=cart_id, id=item_id).first()


class CartStatsAPIView(generics.RetrieveAPIView):

    from carts.serializers import CartSerializerShallow

    serializer_class = CartSerializerShallow
    permission_classes = [AllowAny]
    lookup_field = 'cart_id'

    def get_queryset(self):

        Cart = apps.get_model('carts', 'Cart')

        cart_id = self.kwargs['cart_id']
        queryset = Cart.objects.filter(cart_id=cart_id)
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        total_price = 0.00
        total_tax = 0.00
        total_total = 0.00

        for cart_item in queryset:
            total_price += float(self.calculate_price(cart_item))
            total_tax += float(self.calculate_tax(cart_item))
            total_total += round(float(self.calculate_total(cart_item)), 2)

        data = {
            "price": total_price,
            "tax": total_tax,
            "total": total_total,
        }

        return Response(data)

    def calculate_price(self, cart_item):
        return cart_item.price

    def calculate_tax(self, cart_item):
        return cart_item.tax_fee

    def calculate_total(self, cart_item):
        return cart_item.total


class CreateOrderAPIView(generics.CreateAPIView):

    from carts.serializers import CartOrderSerializer

    serializer_class = CartOrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        User = apps.get_model("users", "User")
        Cart = apps.get_model('carts', 'Cart')
        CartOrder = apps.get_model("carts", "CartOrder")
        CartOrderItem = apps.get_model("carts", "CartOrderItem")

        print(request.headers.get('Authorization'))
        full_name = request.data['full_name']
        email = request.data['email']
        country = request.data['country']
        cart_id = request.data['cart_id']
        user_id = request.user.id

        if user_id != 0:
            user = User.objects.get(id=user_id)
        else:
            user = None

        cart_items = Cart.objects.filter(cart_id=cart_id)

        total_price = Decimal(0.00)
        total_tax = Decimal(0.00)
        total_initial_total = Decimal(0.00)
        total_total = Decimal(0.00)

        order = CartOrder.objects.create(
            full_name=full_name,
            email=email,
            country=country,
            student=user
        )

        for c in cart_items:
            CartOrderItem.objects.create(
                order=order,
                course=c.course,
                price=c.price,
                tax_fee=c.tax_fee,
                total=c.total,
                initial_total=c.total,
                teacher=c.course.teacher
            )

            total_price += Decimal(c.price)
            total_tax += Decimal(c.tax_fee)
            total_initial_total += Decimal(c.total)
            total_total += Decimal(c.total)

            order.teachers.add(c.course.teacher)

        order.sub_total = total_price
        order.tax_fee = total_tax
        order.initial_total = total_initial_total
        order.total = total_total
        order.save()

        return Response({"message": "Order Created Successfully", "order_oid": order.oid},
                        status=status.HTTP_201_CREATED)


class CheckoutAPIView(generics.RetrieveAPIView):

    from carts.serializers import CartOrderSerializer
    CartOrder = apps.get_model("carts", "CartOrder")

    serializer_class = CartOrderSerializer
    permission_classes = [IsAuthenticated]
    queryset = CartOrder.objects.all()
    lookup_field = 'oid'

# Payment
class StripeCheckoutAPIView(generics.CreateAPIView):

    from carts.serializers import CartOrderSerializer

    serializer_class = CartOrderSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):

        CartOrder = apps.get_model("carts", "CartOrder")

        order_oid = self.kwargs['order_oid']
        order = CartOrder.objects.get(oid=order_oid)

        if not order:
            return Response({"message": "Order Not Found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            checkout_session = stripe.checkout.Session.create(
                customer_email=order.email,
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': order.full_name,
                            },
                            'unit_amount': int(order.total * 100)
                        },
                        'quantity': 1
                    }
                ],
                mode='payment',
                success_url=settings.FRONTEND_SITE_URL + '/payment-success/' + order.oid + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.FRONTEND_SITE_URL + '/payment-failed/'
            )
            print("checkout_session ====", checkout_session)
            order.stripe_session_id = checkout_session.id

            return redirect(checkout_session.url)
        except stripe.error.StripeError as e:
            return Response({"message": f"Something went wrong when trying to make payment. Error: {str(e)}"})


def get_access_token(client_id, secret_key):
    token_url = "https://api.sandbox.paypal.com/v1/oauth2/token"
    data = {'grant_type': 'client_credentials'}
    auth = (client_id, secret_key)
    response = requests.post(token_url, data=data, auth=auth)

    if response.status_code == 200:
        print("Access TOken ====", response.json()['access_token'])
        return response.json()['access_token']
    else:
        raise Exception(f"Failed to get access token from paypal {response.status_code}")


class PaymentSuccessAPIView(generics.CreateAPIView):

    from carts.serializers import CartOrderSerializer
    CartOrder = apps.get_model("carts", "CartOrder")

    serializer_class = CartOrderSerializer
    queryset = CartOrder.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        CartOrder = apps.get_model("carts", "CartOrder")
        CartOrderItem = apps.get_model("carts", "CartOrderItem")
        Notification = apps.get_model("notifications", "Notification")
        EnrolledCourse = apps.get_model("certificates", "EnrolledCourse")

        order_oid = request.data['order_oid']
        session_id = request.data['session_id']
        paypal_order_id = request.data['paypal_order_id']

        print("order_oid ====", order_oid)
        print("session_id ====", session_id)
        print("paypal_order_id ====", paypal_order_id)

        order = CartOrder.objects.get(oid=order_oid)
        order_items = CartOrderItem.objects.filter(order=order)

        # Paypal payment success
        if paypal_order_id != "null":
            paypal_api_url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{paypal_order_id}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f"Bearer {get_access_token(PAYPAL_CLIENT_ID, PAYPAL_SECRET_ID)}"
            }
            response = requests.get(paypal_api_url, headers=headers)
            if response.status_code == 200:
                paypal_order_data = response.json()
                paypal_payment_status = paypal_order_data['status']
                if paypal_payment_status == "COMPLETED":
                    if order.payment_status == "Processing":
                        order.payment_status = "Paid"
                        order.save()
                        Notification.objects.create(user=order.student, order=order,
                                                               type="Course Enrollment Completed")
                        for o in order_items:
                            Notification.objects.create(teacher=o.teacher, order=order, order_item=o,
                                                                   type="New Order")
                            EnrolledCourse.objects.create(course=o.course, user=order.student,
                                                                     teacher=o.teacher, order_item=o)

                        return Response({"message": "Payment Successful"})
                    else:
                        return Response({"message": "Already Paid"})
                else:
                    return Response({"message": "Payment Failed"})
            else:
                return Response({"message": "PayPal Error Occurred"})

        # Stripe payment success
        if session_id != 'null':
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status == "paid":
                if order.payment_status == "Processing":
                    order.payment_status = "Paid"
                    order.save()

                    Notification.objects.create(user=order.student, order=order,
                                                           type="Course Enrollment Completed")
                    for o in order_items:
                        Notification.objects.create(teacher=o.teacher, order=order, order_item=o,
                                                               type="New Order")
                        EnrolledCourse.objects.create(course=o.course, user=order.student, teacher=o.teacher,
                                                                 order_item=o)

                    return Response({"message": "Payment Successful"})
                else:
                    return Response({"message": "Already Paid"})
            else:
                return Response({"message": "Payment Failed"})

