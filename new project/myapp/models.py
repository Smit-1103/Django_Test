from django.db import models
from django.contrib.auth.models import User

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=200)
    warehouse = models.CharField(max_length=100, default='Unknown')

    def __str__(self):
        return self.name

# Product Model
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=100)
    available = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    interested = models.PositiveIntegerField(default=0)

    def refill(self):
        """Adds 100 units to the current stock."""
        self.stock += 100
        self.save()

    def __str__(self):
        return self.name

# Client Model
class Client(User):
    PROVINCE_CHOICES = [
        ('AB', 'Alberta'),
        ('MB', 'Manitoba'),
        ('ON', 'Ontario'),
        ('QC', 'Quebec'),
    ]
    company = models.CharField(max_length=50,null=True, blank=True)
    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=20,default='Windsor')
    province = models.CharField(max_length=2, choices=PROVINCE_CHOICES, default='ON')
    interested_in = models.ManyToManyField(Category)

    def __str__(self):
        return self.username


# Order Model
class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        (0, 'Order Cancelled'),
        (1, 'Order Placed'),
        (2, 'Order Shipped'),
        (3, 'Order Delivered'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    num_units = models.PositiveIntegerField()
    order_status = models.IntegerField(choices=ORDER_STATUS_CHOICES, default=1)
    status_date = models.DateField(auto_now=True)  # Auto-updates

    def total_cost(self):
        return self.num_units * self.product.price  # Computes order cost

    def __str__(self):
        return f"Order {self.id} - {self.product.name} x{self.num_units}"