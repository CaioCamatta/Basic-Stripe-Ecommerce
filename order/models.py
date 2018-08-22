from django.db import models

# Order model. We'll fill most of these fields with data from the stripe form.
class Order(models.Model):
    # Basic Info
    token = models.CharField(max_length=250, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="USD Order Total")
    emailAddress = models.EmailField(max_length=250, blank=True, verbose_name="Email Address")
    created = models.DateTimeField(auto_now_add=True)

    # Billing
    billingName = models.CharField(max_length=250, blank=True)
    billingAddress1 = models.CharField(max_length=250, blank=True)
    billingCity = models.CharField(max_length=250, blank=True)
    billingPostCode = models.CharField(max_length=10, blank=True)
    billingCountry = models.CharField(max_length=150, blank=True)

    # Shipping
    shippingName = models.CharField(max_length=250, blank=True)
    shippingAddress1 = models.CharField(max_length=250, blank=True)
    shippingCity = models.CharField(max_length=250, blank=True)
    shippingPostCode = models.CharField(max_length=10, blank=True)
    shippingCountry = models.CharField(max_length=150, blank=True)

    class Meta:
        db_table = 'Order'
        ordering = ['-created']

    # The order objects will be its id
    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.CharField(max_length=250)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="USD Price")
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        db_table = 'OrderItem'

    def sub_total(self):
        return self.quantity * self.price

    def __str__(self):
        return self.product
