from django.urls import path
from .views import *

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('contact/', ContactCreateView.as_view(), name='contact'),
    path('order/', OrderCreateView.as_view(), name='order-create'),
    path('merchant/', MerchantOrderListView.as_view(), name='merchant-orders'),
    path('order/status/<int:order_id>/',order_status, name='order-status'),
    path('products/<uuid:uuid>/', product_detail_by_uuid, name='product-by-uuid'),
    path('order/update-status/<int:order_id>/', update_order_status, name='update_order_status'),
    path('categories/', get_categories),
    path('user-post/', create_user_post, name='create_user_post'),
]



