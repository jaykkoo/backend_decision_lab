
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["product", "user"]

class ProductViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductView
        fields = '__all__'
