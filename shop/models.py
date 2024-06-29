from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models import Sum


# Create your models here.
def generate_slug(name):
    return slugify(name)


class ProdCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_visible = models.BooleanField(default=True)
    sort = models.PositiveSmallIntegerField()
    slug = models.SlugField(max_length=255, default='', blank=True)

    # Override save method to generate slug automatically
    def save(self, *args, **kwargs):
        # If slug is not provided, generate it from name
        if not self.slug:
            self.slug = generate_slug(self.name)
        super().save(*args, **kwargs)

    def __iter__(self):
        for prod in self.prods.filter(is_visible=True):
            yield prod

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product category'
        verbose_name_plural = 'Product categories'
        ordering = ['sort']


class Prod(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_visible = models.BooleanField(default=True)
    category = models.ForeignKey(ProdCategory, on_delete=models.CASCADE, related_name='prods')
    sort = models.PositiveSmallIntegerField()

    photo = models.ImageField(upload_to='prods/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['sort']


class Contacts(models.Model):
    address = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    opening_days = models.CharField(max_length=255, blank=True, null=True)
    working_hours = models.TextField(blank=True, null=True)
    closed_days = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'


class Staff(models.Model):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='staff_photo/', blank=True, null=True)
    bio = models.TextField(max_length=255)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Store employees'
        verbose_name_plural = 'Store employees'


class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    photo = models.ImageField(upload_to='news_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.items.aggregate(Sum('total_price'))['total_price__sum'] or 0

    def __str__(self):
        return f'User Cart {self.user.username}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Prod, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'