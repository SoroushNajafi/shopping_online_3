from django.contrib import admin

from jalali_date.admin import ModelAdminJalaliMixin
from .models import Product, Comment, Category, ProductImage


class CommentsInLine(admin.TabularInline):
    model = Comment
    fields = ['author', 'body', 'stars', 'active', ]
    extra = 1


class ProductImagesInLine(admin.TabularInline):
    model = ProductImage
    fields = ['product', 'product_image']
    extra = 1


@admin.register(Product)
class ProductAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'active']
    inlines = [CommentsInLine, ProductImagesInLine]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'author', 'stars', 'active']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['en_title', 'fa_title', 'datetime_created']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass


