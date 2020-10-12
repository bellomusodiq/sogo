from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Landing, PrivatePolicy, TermsOfService, \
    Event, Contact, About, Product, Cart, CartProduct, Order, OrderProduct, Faq
from .serializers import LandingSerializer, PrivatePolicySerializer, TermsOfServiceSerializer, \
    EventSerializer, ContactSerializer, AboutSerializer, ProductSerializer, CartProductSerializer, \
    CartSerializer, FaqSerializer
from rest_framework.views import APIView
import requests
from django.conf import settings


# Create your views here.


class LandingView(APIView):

    def get(self, request):

        landing = Landing.objects.first()
        if not landing:
            return Response({'message': 'landing page data not found'}, 404)
        events = Event.objects.all()
        event_response = [EventSerializer(event).data for event in events]
        response = {
            'landing': LandingSerializer(landing).data,
            'events': event_response
        }
        return Response(response)


class FooterView(APIView):

    def get(self, request):

        landing = Landing.objects.first()
        if not landing:
            return Response({'message': 'landing page data not found'}, 404)
        response = {
            'twitter_url': landing.twitter_url,
            'facebook_url': landing.facebook_url,
            'instagram_url': landing.instagram_url,
            'linkedin_url': landing.linkedin_url,
            'location': landing.location,
            'info_email': landing.info_email,
            'support_email': landing.support_email,
            'phone': landing.phone,
        }
        return Response(response)


class TermsOfServiceView(APIView):

    def get(self, request):
        tos = TermsOfService.objects.first()
        if not tos:
            return Response({'message': 'terms of service was not found'}, 404)
        return Response(TermsOfServiceSerializer(tos).data)


class PrivatePolicyView(APIView):

    def get(self, request):
        tos = PrivatePolicy.objects.first()
        if not tos:
            return Response({'message': 'privacy policy was not found'}, 404)
        return Response(PrivatePolicySerializer(tos).data)


class AboutView(APIView):

    def get(self, request):
        tos = About.objects.first()
        if not tos:
            return Response({'message': 'about was not found'}, 404)
        return Response(AboutSerializer(tos).data)


class ContactViewSet(ModelViewSet):

    serializer_class = ContactSerializer
    queryset = Contact.objects.all()


class ProductViewSet(ModelViewSet):

    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class CartViewSet(ModelViewSet):

    serializer_class = CartSerializer
    queryset = Cart.objects.all()


class FaqViewSet(ModelViewSet):

    serializer_class = FaqSerializer
    queryset = Faq.objects.all()


class CartProductViewSet(ModelViewSet):

    serializer_class = CartProductSerializer

    def get_queryset(self):
        queryset = CartProduct.objects.all()
        cart = self.request.GET.get('cart')
        if cart:
            if cart != 'null':
                queryset = queryset.filter(cart__id=cart)
            else:
                queryset = []
        return queryset


class VerifyPayment(APIView):

    def post(self, request):
        url = 'https://api.paystack.co/transaction/verify/' + request.data.get('ref')

        cart_id = request.data.get('cart_id')
        try:
            cart = Cart.objects.get(id=cart_id)
            amount = 0
            for product in cart.cartproduct_set.all():
                amount += (product.product.price * product.quantity)
            amount = int(amount * 100)
            headers = {
                'Authorization': 'Bearer {}'.format(settings.PAYSTACK_SECRET_KEY)
            }
            x = requests.get(url, headers=headers)
            res = x.json()
            if (res['status'] and (amount == res['data']['amount'])):
                order = Order.objects.create(
                    amount=amount/100,
                    email=request.data.get('email'),
                    ref=request.data.get('ref'),
                    name=request.data.get('name'),
                    street_name=request.data.get('street_name'),
                    city=request.data.get('city'),
                    country=request.data.get('country'),
                    zip_code=request.data.get('zip_code'),
                )
                for product in cart.cartproduct_set.all():
                    OrderProduct.objects.create(
                        order=order,
                        product=product.product,
                        quantity=product.quantity
                    )
                return Response({'message': 'payment was successful'})
            return Response({'message': 'payment was not successful'}, 400)
        except Cart.DoesNotExist:
            return Response({'message': 'cart id does not exist'}, 400)


