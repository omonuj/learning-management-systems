from rest_framework import serializers
from django.apps import apps


class CartSerializerShallow(serializers.ModelSerializer):

    class Meta:
        Cart = apps.get_model('carts', 'Cart')
        fields = "__all__"
        model = Cart
        depth = 0

class CartSerializerDeep(serializers.ModelSerializer):
    class Meta:
        Cart = apps.get_model('carts', 'Cart')
        fields = "__all__"
        model = Cart
        depth = 3


class CartOrderSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()
    class Meta:
        CartOrder = apps.get_model('carts', 'CartOrder')
        fields = (
            "student", "teachers", "sub_total", "order_items", "tax_fee",
            "total", "payment_status", "full_name", "email", "coupons",
            "stripe_session_id", "oid", "datetime",
        )
        model = CartOrder

    def get_order_items(self, obj):
        return CartOrderItemSerializer(obj.order_items(), many=True).data


class CartOrderItemSerializer(serializers.ModelSerializer):
    order_id = serializers.SerializerMethodField()
    payment_status = serializers.SerializerMethodField()

    class Meta:
        CartOrderItem = apps.get_model('carts', 'CartOrderItem')
        fields = (
            "order_id", "payment_status", "order", "courses", "teacher",
            "tax_fee", "total", "initial_total", "saved", "coupons",
            "applied_coupon", "oid", "datetime",
        )
        model = CartOrderItem

    def get_order_id(self, obj):
        return obj.order_id()  # Call the method, with ()

    def get_payment_status(self, obj):
        return obj.payment_status()
