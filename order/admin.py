from django.contrib import admin
from .models import Order, OrderItem

class OrderItemAdmin(admin.TabularInline):
    model = OrderItem

    # Separate the order items' information into columns with names
    fieldset = [
        ('Product', {'fields':['product'],}),
        ('Quantity', {'fields':['quantity'],}),
        ('Price', {'fields':['price'],}),
    ]

    # We don't want to allow the admin to edit fields
    readonly_fields = ['product', 'quantity', 'price']

    # Remove empty rows on the order item section
    max_num = 0

    # Custom admin page (commented the {{ inline_admin_form.original }} line to remove duplicate title)
    template = 'admin/order/tabular.html'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Display these fields on the admin page that lists the orders
    list_display = ['id', 'billingName', 'emailAddress', 'created']

    # Click on these fields to go to order details (not 100% necessary but ok)
    list_display_links = ['id', 'billingName']

    # Search for these fields
    search_fields = ['id', 'billingName', 'emailAddress']

    # We don't want to allow the admin to edit fields
    readonly_fields = ['id', 'token', 'total', 'emailAddress', 'created', 'billingName', 'billingAddress1', 'billingCity', 'billingPostCode', 'billingCountry', 'shippingName', 'shippingAddress1', 'shippingCity', 'shippingPostCode', 'shippingCountry']

    # Separate fields in different categories
    fieldsets = (
        ('ORDER INFORMATION', {
            'fields': ('id', 'token', 'total', 'created', 'emailAddress')
        }),
        ('BILLING INFORMATION', {
            'fields': ('billingName', 'billingAddress1', 'billingCity', 'billingPostCode', 'billingCountry')
        }),
        ('SHIPPING INFORMATION', {
            'fields': ('shippingName', 'shippingAddress1', 'shippingCity', 'shippingPostCode', 'shippingCountry')
        })
    )

    inlines = [
        OrderItemAdmin,
    ]

    # Disable delete functionality
    def has_delete_permission(self, request, obj=None):
        return False

    # Disable add functionality
    def has_add_permission(self, request):
        return False

    list_per_page = 20
