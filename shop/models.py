from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.utils.text import slugify


# Function to generate a slug from a name
def generate_slug(name):
    return slugify(name)


class ProdCategory(models.Model):
    """
    Model representing a product category.

    Fields:
        name (CharField): The name of the product category.
        is_visible (BooleanField): Whether the category is visible.
        sort (PositiveSmallIntegerField): Sort order of the category.
        slug (SlugField): URL-friendly version of the category name.
    """

    name = models.CharField(max_length=255, unique=True)
    is_visible = models.BooleanField(default=True)
    sort = models.PositiveSmallIntegerField()
    slug = models.SlugField(max_length=255, default="", blank=True)

    def save(self, *args, **kwargs):
        """
        Override the save method to generate a slug automatically if it is not provided.
        """
        if not self.slug:
            self.slug = generate_slug(self.name)
        super().save(*args, **kwargs)

    def __iter__(self):
        """
        Iterate over all visible products in the category.
        """
        for prod in self.prods.filter(is_visible=True):
            yield prod

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product category"
        verbose_name_plural = "Product categories"
        ordering = ["sort"]


class Prod(models.Model):
    """
    Model representing a product.

    Fields:
        name (CharField): The name of the product.
        description (TextField): The description of the product.
        price (DecimalField): The price of the product.
        is_visible (BooleanField): Whether the product is visible.
        category (ForeignKey): The category the product belongs to.
        sort (PositiveSmallIntegerField): Sort order of the product.
        photo (ImageField): The image of the product.
    """

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_visible = models.BooleanField(default=True)
    category = models.ForeignKey(
        ProdCategory, on_delete=models.CASCADE, related_name="prods"
    )
    sort = models.PositiveSmallIntegerField()
    photo = models.ImageField(upload_to="prods/", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["sort"]


class Contacts(models.Model):
    """
    Model representing contact information.

    Fields:
        address (CharField): The address of the contact.
        email (EmailField): The email address of the contact.
        phone (CharField): The phone number of the contact.
        opening_days (CharField): The days the business is open.
        working_hours (TextField): The working hours of the business.
        closed_days (CharField): The days the business is closed.
    """

    address = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    opening_days = models.CharField(max_length=255, blank=True, null=True)
    working_hours = models.TextField(blank=True, null=True)
    closed_days = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"


class Staff(models.Model):
    """
    Model representing a staff member.

    Fields:
        name (CharField): The name of the staff member.
        position (CharField): The position of the staff member.
        photo (ImageField): The photo of the staff member.
        bio (TextField): The biography of the staff member.
        is_visible (BooleanField): Whether the staff member is visible.
    """

    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="staff_photo/", blank=True, null=True)
    bio = models.TextField(max_length=255)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Store employees"
        verbose_name_plural = "Store employees"


class News(models.Model):
    """
    Model representing a news item.

    Fields:
        title (CharField): The title of the news item.
        content (TextField): The content of the news item.
        photo (ImageField): The photo associated with the news item.
        created_at (DateTimeField): The date and time when the news item was created.
    """

    title = models.CharField(max_length=255)
    content = models.TextField()
    photo = models.ImageField(upload_to="news_photos/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Cart(models.Model):
    """
    Model representing a shopping cart.

    Fields:
        user (OneToOneField): The user associated with the cart.
        created_at (DateTimeField): The date and time when the cart was created.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        """
        Calculate the total price of all items in the cart.
        """
        return self.items.aggregate(Sum("total_price"))["total_price__sum"] or 0

    def __str__(self):
        return f"User Cart {self.user.username}"


class CartItem(models.Model):
    """
    Model representing an item in a shopping cart.

    Fields:
        cart (ForeignKey): The cart the item belongs to.
        product (ForeignKey): The product associated with the item.
        quantity (PositiveIntegerField): The quantity of the product.
        total_price (DecimalField): The total price for the quantity of the product.
    """

    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Prod, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        """
        Override the save method to calculate the total price of the item based on the quantity.
        """
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
