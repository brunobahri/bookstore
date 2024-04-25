from rest_framework import serializers
from django.contrib.auth.models import User
from product.models.product import Product
from product.serializers.product_serializer import ProductSerializer
from order.models.order import Order


class OrderSerializer(serializers.ModelSerializer):
    products_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", many=True, write_only=True
    )
    product = ProductSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )
    total = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = ["id", "product", "total", "user", "products_id"]
        extra_kwargs = {"user": {"write_only": True}}

    def get_total(self, order):
        return sum(product.price for product in order.product.all())

    def create(self, validated_data):
        products_data = validated_data.pop("product", [])
        user = validated_data.pop("user")
        order = Order.objects.create(user=user)
        order.product.set(products_data)
        return order
