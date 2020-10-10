from django.contrib import admin
from django.db import models
from .models import Landing, TermsOfService, Event, Contact, PrivatePolicy, \
    About, Product, Cart, CartProduct, Order, OrderProduct
from quilljs.widgets import QuillEditorWidget
from quilljs.admin import QuillAdmin


class TermsOfServiceAdmin(QuillAdmin):
    formfield_overrides = {
        models.TextField: {'widget': QuillEditorWidget},
    }


class PrivatePolicyAdmin(QuillAdmin):
    formfield_overrides = {
        models.TextField: {'widget': QuillEditorWidget},
    }


class AboutAdmin(QuillAdmin):
    formfield_overrides = {
        models.TextField: {'widget': QuillEditorWidget},
    }

# Register your models here.


admin.site.register(Landing)

admin.site.register(TermsOfService, TermsOfServiceAdmin)

admin.site.register(Event)

admin.site.register(Contact)

admin.site.register(PrivatePolicy, PrivatePolicyAdmin)

admin.site.register(About, AboutAdmin)

admin.site.register(Product)

admin.site.register(Cart)

admin.site.register(CartProduct)

admin.site.register(Order)

admin.site.register(OrderProduct)
