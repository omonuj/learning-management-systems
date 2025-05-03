from django.urls import path
from carts import views

urlpatterns = [

    path("course/cart/", views.CartAPIView.as_view()),
    path("course/cart-list/<cart_id>/", views.CartListAPIView.as_view()),
    path("cart/stats/<cart_id>/", views.CartStatsAPIView.as_view()),
    path("course/cart-item-delete/<cart_id>/<item_id>/", views.CartItemDeleteAPIView.as_view()),
    path("order/create-order/", views.CreateOrderAPIView.as_view()),
    path("order/checkout/<oid>/", views.CheckoutAPIView.as_view()),
]