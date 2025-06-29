from django.db import models
import uuid
from django.utils.html import mark_safe


class Category(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def img(self):
        return mark_safe(f"<img src='{self.image.url}' alt='' width='100'> ")

    def __str__(self):
        return self.name


class Product(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False)
    title = models.CharField(max_length=255)
    short_description = models.CharField(max_length=300)
    long_description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    img1 = models.ImageField(upload_to='products/')
    img2 = models.ImageField(upload_to='products/', null=True, blank=True)
    img3 = models.ImageField(upload_to='products/', null=True, blank=True)
    additional_info = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE)
    top_selling = models.BooleanField(default=False)

    def ProductImage1(self):
        return mark_safe(f"<img src='{self.img1.url}' alt='' width='250'> ")

    def ProductImage2(self):
        return mark_safe(f"<img src='{self.img2.url}' alt='' width='230'>")

    def ProductImage3(self):
        return mark_safe(f"<img src='{self.img3.url}' alt='' width='230'>")

    def ProductImage(self):
        return mark_safe(f"<img src='{self.img1.url}' alt='' width='100'>")

    def __str__(self):
        return str(self.uuid)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"


ORDER_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('processing', 'Processing'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled'),
]

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.TextField()
    landmark = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    note = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100,)  # ✅ NEW FIELD
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.order_id} – {self.first_name} {self.last_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"


class UserPost(models.Model):
    username = models.CharField(max_length=100)
    user_email = models.EmailField()

    def __str__(self):
        return self.username
