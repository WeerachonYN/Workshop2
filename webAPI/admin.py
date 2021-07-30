from django.contrib import admin
from django.db import models
from webAPI.models.product import Product
from webAPI.models.productImage import ProductImage
from webAPI.models.category import Category
from webAPI.models.cart import Cart
from webAPI.models.Invoice import invoice
from webAPI.models.Invoice_item import invoice_item
from webAPI.models.Comment import Comment
from webAPI.models.ImageUser import ImageUser
from rest_framework.authtoken.admin import TokenAdmin
# Register your models here.
class ImageProductAdmins(admin.StackedInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    class Meta:
        model = Product
    inlines = [ ImageProductAdmins]
    list_display = (
        'id',
        'category',
        'name',
        'price',
         'detail',
         'image',
        'is_enabled',
        'created_datetime'
    )
    list_editable = (
        'is_enabled',
        'detail',
        'price',
    )
    list_filter = (
        'category',
       'is_enabled',
       'recommend',
    )
    search_fields = (
        'name',
    )
    list_per_page=6

admin.site.register(Product,ProductAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'product',
        'user',
        'quantity',
        'total',
    )
    list_editable = (
        'quantity',
        'total',
    )
    list_filter = (
        'product',
        'user'
    )
    list_per_page=10
admin.site.register(Cart,CartAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
   
        'name',
        'image',
        'detail',
        'is_enabled',
    )
    list_editable = (
        'is_enabled',
        'detail',
        'image'
    )
    list_filter = (
        'name',
        'is_enabled'
    )
    search_fields=[
        'name'
    ]
   
admin.site.register(Category,CategoryAdmin)

class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'created_datetime',
        'updated_datetime',
        'total',
        'status'
    )
    list_editable = (
        'status',
        'updated_datetime',
        'total',
    )
    list_filter = (
        'user',
    )
    search_fields=[
        'user'
    ]
admin.site.register(invoice,InvoiceAdmin)

class InvoiceITEMAdmin(admin.ModelAdmin):
    
    class Meta:
        model = Product
    list_display = (
        'id',
        'product',
        'invoice',
        'created_datetime',
        'quantity',
        'total'
    )
admin.site.register(invoice_item,InvoiceITEMAdmin)


TokenAdmin.raw_id_fields = ['user']
class CommentAdmin(admin.ModelAdmin):
    class Meta:
        model = Comment
    list_display=(
        'id',
        
        'message',
        'product',
        'user',
        'datetime',
        'is_activate'
    )
admin.site.register(Comment,CommentAdmin)
class ImageUserAdmin(admin.ModelAdmin):
    class Meta:
        model = ImageUser
    list_display=(
        'id',
        'user',
        'image',
    )
admin.site.register(ImageUser,ImageUserAdmin)
