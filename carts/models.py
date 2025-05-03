from django.db import models
from django.db.models import SET_NULL
from shortuuid.django_fields import ShortUUIDField

# Create your models here.
PAYMENT_STATUS = (
    ("PAID", "paid"),
    ("PROCESSING", "processing"),
    ("FAILED", "failed"),

)

class Cart(models.Model):
    courses = models.ForeignKey("courses.Courses", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tax_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    cart_id = ShortUUIDField(unique=True, max_length=20, alphabet='1234567890')
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.courses.title


class CartOrder(models.Model):
    student = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True)
    teachers = models.ManyToManyField("teachers.Teacher", blank=True)
    sub_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tax_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    payment_status = models.CharField(choices=PAYMENT_STATUS, default='PROCESSING', max_length=100)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    coupons = models.ManyToManyField("teachers.Coupon", blank=True)
    stripe_session_id = models.CharField(max_length=100, null=True, blank=True)
    oid = ShortUUIDField(unique=True, max_length=20, alphabet='1234567890')
    datetime = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-datetime']

    def order_items(self):
        return CartOrderItem.objects.filter(oder=self)

    def __str__(self):
        return self.oid


class CartOrderItem(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE, related_name='order_item')
    courses = models.ForeignKey("courses.Courses", on_delete=models.CASCADE, related_name='order_item')
    teacher = models.ForeignKey("teachers.Teacher", on_delete=models.CASCADE)
    tax_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    initial_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    saved = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    coupons = models.ForeignKey("teachers.Coupon", on_delete=SET_NULL, blank=True, null=True)
    applied_coupon = models.BooleanField(default=False)
    oid = ShortUUIDField(unique=True, max_length=20, alphabet='1234567890')
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-datetime']

    def order_id(self):
        return f'Order ID #{self.order.oid}'


    def payment_status(self):
        return f'{self.order.payment_status}'

    def __str__(self):
        return self.oid

