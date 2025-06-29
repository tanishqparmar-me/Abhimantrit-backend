from rest_framework import serializers
from .models import *


# ✅ Used when placing an order
class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.UUIDField()  # Expect product UUID in request

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


# ✅ Used when displaying order details to merchant
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.UUIDField()  # Accept UUID as raw string

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'order_id', 'first_name', 'last_name', 'address', 'landmark',
            'city', 'state', 'pincode', 'phone', 'email', 'note',
            'amount', 'status', 'transaction_id',  # ✅ NEW FIELD
            'items'
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        transaction_id = validated_data.pop('transaction_id', None)  # ✅ extract payment id

        order = Order.objects.create(transaction_id=transaction_id, **validated_data)

        for item_data in items_data:
            product_uuid = item_data.get('product')
            try:
                product = Product.objects.get(uuid=product_uuid)
            except Product.DoesNotExist:
                raise serializers.ValidationError(
                    f"Product with UUID {product_uuid} does not exist."
                )
            OrderItem.objects.create(
                order=order, product=product, quantity=item_data['quantity'])

        return order



# ✅ Used for GET /merchant/orders/
class OrderDisplaySerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'order_id',
            'first_name', 'last_name', 'address', 'landmark',
            'city', 'state', 'pincode', 'phone', 'email', 'note',
            'amount', 'status', 'created_at', 'items'
        ]


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'phone', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']


class OrderDisplaySerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'order_id', 'first_name', 'last_name', 'address', 'landmark',
            'city', 'state', 'pincode', 'phone', 'email', 'note',
            'amount', 'status', 'created_at', 'items'
        ]



class OrderStatusSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    created_at = serializers.DateTimeField(format="%d %B %Y, %I:%M %p")  # 👈 optional formatting

    class Meta:
        model = Order
        fields = [
            'order_id', 'first_name', 'last_name', 'address', 'landmark',
            'city', 'state', 'pincode', 'phone', 'email', 'note',
            'amount', 'status', 'created_at',
            'items'
        ]


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['name', 'image']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None
    

class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPost
        fields = '__all__'
