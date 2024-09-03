from django.db import models

# Create your models here.


NOTI_TYPE = (
    ("New Order", "New Order"),
    ("New Review", "New Review"),
    ("New Course Question", "New Course Question"),
    ("Draft", "Draft"),
    ("Course Published", "Course Published"),
)

class Notification(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey("teachers.Teacher", on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey("carts.CartOrder", on_delete=models.SET_NULL, null=True, blank=True)
    order_item = models.ForeignKey("carts.CartOrderItem", on_delete=models.SET_NULL, null=True, blank=True)
    review = models.ForeignKey("courses.Review", on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=1000, choices=NOTI_TYPE, default=None)
    seen = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.type
