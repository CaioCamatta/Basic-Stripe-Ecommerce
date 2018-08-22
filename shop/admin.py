from django.contrib import admin
from .models import Category, Product

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields = {'slug':('name',)}

class ProductAdmin(admin.ModelAdmin):
    # Display these fields in the products admin page
    list_display = ['name','price', 'stock', 'available', 'created', 'updated']

    # Allow to edit without having to go in the product details page.
    list_editable = ['price', 'stock', 'available']

    # Auto fill slugh with name when creating a new product
    prepopulated_fields = {'slug':('name',)}
    
    list_per_page = 20

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
