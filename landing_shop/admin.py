from django.contrib import admin
from .models import Landing, TermsOfService, Event, Contact, PrivatePolicy, \
    About, Product, Cart, CartProduct

# Register your models here.


admin.site.register(Landing)

admin.site.register(TermsOfService)

admin.site.register(Event)

admin.site.register(Contact)

admin.site.register(PrivatePolicy)

admin.site.register(About)

admin.site.register(Product)

admin.site.register(Cart)

admin.site.register(CartProduct)
