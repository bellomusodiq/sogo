from rest_framework import serializers
from .models import Landing, PrivatePolicy, TermsOfService, \
    Event, Contact, UserComment, About, Product, CartProduct, \
    Cart


class LandingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Landing
        fields = '__all__'


class PrivatePolicySerializer(serializers.ModelSerializer):

    class Meta:
        model = PrivatePolicy
        fields = '__all__'


class AboutSerializer(serializers.ModelSerializer):

    class Meta:
        model = About
        fields = '__all__'


class TermsOfServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = TermsOfService
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = '__all__'


class UserCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserComment
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Cart
        fields = '__all__'


class CartProductSerializer(serializers.ModelSerializer):

    product_obj = serializers.SerializerMethodField()
    
    class Meta:
        model = CartProduct
        fields = '__all__'

    def get_product_obj(self, obj):
        return ProductSerializer(obj.product).data
