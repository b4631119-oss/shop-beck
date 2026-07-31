# products/models.py
from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Смартфоны', 'Смартфоны'),
        ('Аксессуары', 'Аксессуары'),
    ]
    
    name = models.CharField('Название', max_length=255)
    category = models.CharField('Категория', max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField('Цена', max_digits=12, decimal_places=2)
    old_price = models.DecimalField('Старая цена', max_digits=12, decimal_places=2, null=True, blank=True)
    in_stock = models.BooleanField('В наличии', default=True)
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

# 🔥 НОВАЯ МОДЕЛЬ ДЛЯ ФОТО
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('Фото', upload_to='products/')
    is_primary = models.BooleanField('Главное фото', default=False)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'Фото товара'
        verbose_name_plural = 'Фото товаров'
        ordering = ['-is_primary', 'created_at']

    def __str__(self):
        return f"{self.product.name} - {self.id}"