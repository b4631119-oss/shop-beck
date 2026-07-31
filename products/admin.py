# products/admin.py
from typing import ClassVar

from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display

from .models import Product, ProductImage


class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 1
    fields: ClassVar[list[str]] = ['image', 'image_preview', 'is_primary']
    readonly_fields: ClassVar[list[str]] = ['image_preview']
    max_num = 10
    
    @display(description='Превью')
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 50px; border-radius: 6px; object-fit: cover;" />', obj.image.url)
        return "—"

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display: ClassVar[list[str]] = ['display_image', 'name', 'category', 'display_price', 'display_stock', 'created_at']
    list_filter: ClassVar[list[str]] = ['category', 'in_stock']
    list_filter_submit = True
    search_fields: ClassVar[list[str]] = ['name', 'description']
    list_per_page = 20
    inlines: ClassVar[list[type[ProductImageInline]]] = [ProductImageInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'category', 'description')
        }),
        ('Цена и наличие', {
            'fields': (('price', 'old_price'), 'in_stock')
        }),
    )

    @display(description='Фото')
    def display_image(self, obj):
        first_image = obj.images.first()
        if first_image and first_image.image:
            return format_html(
                '<img src="{}" style="width: 44px; height: 44px; border-radius: 8px; object-fit: cover;" />',
                first_image.image.url
            )
        return format_html(
            '<div style="width: 44px; height: 44px; border-radius: 8px; background: #374151; display: flex; align-items: center; justify-content: center; font-size: 10px; color: #9ca3af;">Нет фото</div>'
        )

    @display(description='Цена', ordering='price')
    def display_price(self, obj):
        if obj.old_price:
            return format_html(
                '<span style="font-weight: 600; color: #10b981;">{} сом</span> <span style="text-decoration: line-through; color: #9ca3af; font-size: 0.85em; margin-left: 4px;">{}</span>',
                obj.price,
                obj.old_price
            )
        return format_html('<span style="font-weight: 600;">{} сом</span>', obj.price)

    @display(description='Статус', label=True)
    def display_stock(self, obj):
        if obj.in_stock:
            return "В наличии", "success"
        return "Нет на складе", "danger"

@admin.register(ProductImage)
class ProductImageAdmin(ModelAdmin):
    list_display: ClassVar[list[str]] = ['image_preview', 'product', 'is_primary', 'created_at']
    list_filter: ClassVar[list[str]] = ['is_primary']
    readonly_fields: ClassVar[list[str]] = ['image_preview']

    @display(description='Превью')
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 60px; border-radius: 8px; object-fit: cover;" />', obj.image.url)
        return "—"