from rest_framework import serializers
from product.models.product import Product, Category
from .category_serializer import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    categories_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(),
                                                       many=True,
                                                       write_only=True,
                                                       required=False)
    categories_detail = CategorySerializer(source='category', many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["id", "title", "description", "price", "active", "categories_id", "categories_detail"]

    def create(self, validated_data):
        category_data = validated_data.pop('categories_id', [])
        product = Product.objects.create(**validated_data)
        if category_data:
            product.category.set(category_data)
        return product
