from rest_framework import serializers
from .models import *


class ProductAddSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "description", "product_image", "price", "stock", "category"]
        
class ProductUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "description","product_image", "price", "stock"]
        
            
    def update(self, instance, validated_data):
        if 'product_image' in validated_data:
            if instance.product_image:
                instance.product_image.delete(save=False)
        return super().update(instance, validated_data)
    
class ProductItemsSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]

class ProductOrderSerializers(serializers.ModelSerializer):
    items = ProductItemsSerializers(many=True)
    total_price = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Order
        fields = ["items", "status", "total_price", "create_at", "update_at"]
        read_only_fields = ["quantity"]

        
    def get_total_price(self, obj):
        return obj.total_price()
    
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(user=self.context['request'].user, **validated_data)
        for item_data in items_data:
            item = OrderItem.objects.create(**item_data)
            order.items.add(item)
        return order
    