from django.test import TestCase
from django.urls import reverse
from shop.models import ProdCategory, Prod, Staff, News, Contacts
from django.contrib.auth.models import User
from django.test import RequestFactory


class ShopViewTest(TestCase):

    def setUp(self):
        self.category1 = ProdCategory.objects.create(name="Smartphones", is_visible=True, sort=1)
        self.category2 = ProdCategory.objects.create(name="Laptops", is_visible=True, sort=2)
        self.product1 = Prod.objects.create(name="iPhone", category=self.category1, price=999, is_visible=True, sort=1)
        self.product2 = Prod.objects.create(name="MacBook", category=self.category2, price=1999, is_visible=True, sort=2)
        self.staff = Staff.objects.create(name="John Doe", position="Manager", is_visible=True)
        self.news = News.objects.create(title="Big Sale", content="Huge discounts on all products!")
        self.contacts = Contacts.objects.create(phone="123-456-7890", email="info@example.com")

    def test_shop_view(self):
        response = self.client.get(reverse('shop:shop'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/shop.html')
        self.assertContains(response, "Smartphones")
        self.assertContains(response, "Laptops")
        self.assertContains(response, "iPhone")
        self.assertContains(response, "MacBook")
        self.assertContains(response, "John Doe")
        self.assertContains(response, "Big Sale")


class ProductDetailViewTest(TestCase):

    def setUp(self):
        self.category = ProdCategory.objects.create(name="Smartphones", is_visible=True, sort=1)
        self.product = Prod.objects.create(name="iPhone", category=self.category, price=999, is_visible=True, sort=1)

    def test_product_detail_view(self):
        response = self.client.get(reverse('shop:product_detail', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "iPhone")
        self.assertTemplateUsed(response, 'shop/product_detail.html')


class AddToCartTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.category = ProdCategory.objects.create(name="Smartphones", is_visible=True, sort=1)
        self.product = Prod.objects.create(name="iPhone", category=self.category, price=999, is_visible=True, sort=1)

    def test_add_to_cart(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('shop:add_to_cart', args=[self.product.pk]), {'quantity': 1})
        self.assertRedirects(response, reverse('shop:product_detail', args=[self.product.pk]))

        session = self.client.session
        self.assertIn(str(self.product.pk), session['cart'])
        self.assertEqual(session['cart'][str(self.product.pk)], 1)


class ViewCartTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.category = ProdCategory.objects.create(name="Smartphones", is_visible=True, sort=1)
        self.product = Prod.objects.create(name="iPhone", category=self.category, price=999, is_visible=True, sort=1)

    def test_view_cart(self):
        session = self.client.session
        session['cart'] = {str(self.product.pk): 2}
        session.save()

        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('shop:view_cart'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "iPhone")
        self.assertContains(response, "1998.00 USD")  # 2 x 999


class CheckoutTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.category = ProdCategory.objects.create(name="Smartphones", is_visible=True, sort=1)
        self.product = Prod.objects.create(name="iPhone", category=self.category, price=999, is_visible=True, sort=1)

    def test_checkout(self):
        session = self.client.session
        session['cart'] = {str(self.product.pk): 2}
        session.save()

        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('shop:checkout'))
        self.assertRedirects(response, reverse('shop:view_cart'))

        session = self.client.session
        self.assertNotIn(str(self.product.pk), session['cart'])
