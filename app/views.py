from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order, Contact
from . serializer import *
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404



from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import exception_handler
import traceback

class OrderCreateView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            order = serializer.save()
            return Response({
                "success": True,
                "message": "Order placed successfully",
                "order_id": order.order_id
            }, status=status.HTTP_201_CREATED)
class MerchantOrderListView(ListAPIView):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderDisplaySerializer


@api_view(['POST'])
def update_order_status(request, order_id):
    try:
        order = Order.objects.get(order_id=order_id)
        new_status = request.data.get('status')

        if not new_status:
            return Response({"error": "Status is required."}, status=status.HTTP_400_BAD_REQUEST)

        order.status = new_status
        order.save()

        return Response({"success": True, "message": "Order status updated."})
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)


class ContactCreateView(CreateAPIView):
    serializer_class = ContactSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            contact = serializer.save()
            return Response({
                "message": "Thank you for contacting us!",
                "name": contact.name,
                "phone": contact.phone
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = ['category', 'top_selling']
    search_fields = ['title', 'short_description']
    

@api_view(['GET'])
def order_status(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = OrderStatusSerializer(order)
    return Response({'success': True, 'order': serializer.data})
            
@api_view(['GET'])
def product_detail_by_uuid(request, uuid):
    product = get_object_or_404(Product, uuid=uuid)
    serializer = ProductSerializer(product)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True, context={'request': request})
    return Response({'success': True, 'categories': serializer.data})

@api_view(['POST'])
def create_user_post(request):
    serializer = UserPostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
