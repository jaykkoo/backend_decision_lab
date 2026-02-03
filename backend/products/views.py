from django.shortcuts import render
from .serializers import ProductSerializer, ProductViewSerializer

class ProductCreateView(APIView):
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        return Response(ProductSerializer(product).data, status=201)

class ProductActionView(APIView):
    def post(self, request):
        serializer = ProductViewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_view = serializer.save()
        return Response(ProductViewSerializer(product_view).data, status=201)