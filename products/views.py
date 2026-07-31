# products/views.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related('images').all()
    serializer_class = ProductSerializer
    
    def get_permissions(self):
        # Для публичных чтения запросов (включая кастомные GET-экшены) разрешаем всем
        if self.action in ['list', 'retrieve', 'categories', 'in_stock'] or self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        # Для POST, PUT, PATCH, DELETE нужен админ
        return [permissions.IsAdminUser()]
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Возвращает список всех категорий"""
        categories = Product.objects.values_list('category', flat=True).distinct()
        return Response(list(categories))
    
    @action(detail=False, methods=['get'])
    def in_stock(self, request):
        """Возвращает только товары в наличии"""
        products = self.get_queryset().filter(in_stock=True)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)