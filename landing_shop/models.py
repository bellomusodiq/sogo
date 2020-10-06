from django.db import models

# Create your models here.


class Landing(models.Model):
    header_title = models.CharField(max_length=400)
    header_text = models.CharField(max_length=400)
    header_image = models.ImageField(upload_to='landing/images')
    available_date = models.DateField(blank=True, null=True)
    features_header1 = models.CharField(max_length=400)
    smartphone_text = models.CharField(max_length=400)
    seamless_text = models.CharField(max_length=400)
    high_resolution_text = models.CharField(max_length=400)
    all_vr_text = models.CharField(max_length=400)
    features_image1 = models.ImageField(upload_to='landing/images')
    features_header2 = models.CharField(max_length=400)
    features_image2 = models.ImageField(upload_to='landing/images')
    features_text2 = models.CharField(max_length=400)
    features_video = models.FileField(upload_to='landing/videos', blank=True, null=True)
    dark_banner_heading = models.CharField(max_length=400)
    dark_banner_text = models.CharField(max_length=400)
    dark_banner_image = models.ImageField(upload_to='landing/images')
    event_text = models.CharField(max_length=400)
    subscription_image = models.ImageField(upload_to='landing/images')
    contact_us_image = models.ImageField(upload_to='landing/images')

    twitter_url = models.URLField()
    facebook_url = models.URLField()
    instagram_url = models.URLField()
    linkedin_url = models.URLField()
    location = models.CharField(max_length=400)
    info_email = models.EmailField(max_length=225)
    support_email = models.EmailField(max_length=225)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return str(self.pk)


class UserComment(models.Model):
    image = models.ImageField(upload_to='coments/images')
    comment = models.CharField(max_length=400)

    def __str__(self):
        return self.comment[:100]


class PrivatePolicy(models.Model):
    private_policy = models.TextField()

    def __str__(self):
        return str(self.pk)


class TermsOfService(models.Model):
    terms_of_service = models.TextField()

    def __str__(self):
        return str(self.pk)


class About(models.Model):
    about = models.TextField()

    def __str__(self):
        return str(self.pk)


class Event(models.Model):
    title = models.CharField(max_length=400)
    image = models.ImageField(upload_to='landing/images')

    def __str__(self):
        return self.title


class Contact(models.Model):
    service_type = models.CharField(max_length=100, choices=(
        ('customer', 'customer'),
        ('support', 'support')
    ))
    email = models.EmailField(max_length=225)
    message = models.TextField()

    def __str__(self):
        return self.email


class Product(models.Model):

    title = models.CharField(max_length=500)
    image = models.ImageField(upload_to='shop/products')
    price = models.FloatField()

    def __str__(self):
        return self.title[:100]


class Cart(models.Model):

    def __str__(self):
        return str(self.id)


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return 'cart {} '.format(self.cart.pk) + self.product.title[:100]
