from django.db import models
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.admin.panels import FieldPanel, InlinePanel, FieldRowPanel, MultiFieldPanel, PageChooserPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from cloudinary.models import CloudinaryField
from authentication.models import User
import datetime
from django.utils.text import slugify
import random
import string
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

class CategoryIndexPage(Page):
    template = 'shop/all_courses.html'

    def get_context(self, request, *args, **kwargs):
        context = super(CategoryIndexPage, self).get_context(request, *args, **kwargs)
        return context

@register_snippet
class Category(models.Model):
    category_name = models.CharField(max_length=500, null=True, blank=True, help_text='Enter a product category', unique=True)
    category_description = RichTextField(null=True, blank=True)
    slug = models.SlugField(null=True,  max_length=500, unique=True)

    panels = [
        FieldPanel('category_name'),
        FieldPanel('category_description'),
    ]

    def __str__(self):
        return self.category_name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name, allow_unicode=True)
        super(Category, self).save(*args, **kwargs)
    
    @staticmethod
    def get_all_categories(): 
        return Category.objects.all()
    
    class Meta:
        verbose_name_plural = "Categories"
    
class ProductIndexPage(Page):
    template = 'shop/all_courses.html'

    def get_context(self, request, *args, **kwargs):
        context = super(ProductIndexPage, self).get_context(request, *args, **kwargs)
        return context
    
def random_alphanumeric_string():
    return ''.join(
        random.choices(
            string.ascii_letters + string.digits,
            k=11
        )
    )
class ProductPage(Page):
    template = 'shop/product_detail.html'
    product_name = models.CharField(max_length=500, null=True, blank=True)
    original_price = models.DecimalField(max_digits=60, decimal_places=2, null=True, blank=True)
    discount_price = models.DecimalField(max_digits=60, decimal_places=2, null=True, blank=True)
    on_sale = models.BooleanField(default=True)
    image1 = CloudinaryField("image", null=True, blank=True, help_text="Enter first product image")
    image2 = CloudinaryField("image", null=True, blank=True, help_text="Enter second product image")
    image3 = CloudinaryField("image", null=True, blank=True, help_text="Enter third product image")
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL, related_name='product_category')
    short_description = models.CharField(max_length=1000, null=True, blank=True)
    full_description = RichTextField(null=True, blank=True)
    additional_information = RichTextField(null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
    # SKU = models.CharField(default=random_alphanumeric_string(), max_length=500, null=False, blank=False)
    # slug = models.SlugField(null=True,  max_length=500, unique=True)

    content_panels = Page.content_panels + [
        FieldPanel('product_name'),
        FieldPanel('original_price'),
        FieldPanel('discount_price'),
        FieldPanel('quantity'),
        # FieldPanel('SKU'),
        FieldPanel('on_sale'),
        FieldPanel('image1'),
        FieldPanel('image2'),
        FieldPanel('image3'),
        FieldPanel('category'),
        FieldPanel('short_description'),
        FieldPanel('full_description'),
        FieldPanel('additional_information'),
    ]

    def __str__(self):
        return self.product_name

    @staticmethod
    def get_products_by_id(ids): 
        return ProductPage.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products(): 
        return ProductPage.objects.all() 
  
    @staticmethod
    def get_all_products_by_categoryid(category_id): 
        if category_id: 
            return ProductPage.objects.filter(category=category_id) 
        else: 
            return ProductPage.get_all_products()
    
    def get_context(self, request, *args, **kwargs):
        context = super(ProductPage, self).get_context(request, *args, **kwargs)
        
        categories = Category.objects.all()
        if request.user.is_authenticated:
            cart = Cart.objects.get_or_create(user=request.user)[0]
            quantity_in_cart = get_object_or_404(CartItem, cart=cart, product=self).quantity
            print(quantity_in_cart)
            cart_items = cart.cartitem_set.all()
            context['cart_items'] = cart_items
            context['cart'] = cart
            context['quantity_in_cart'] = quantity_in_cart
        else:
            cart = None
        context['categories'] = categories
        
        return context
    
    def serve(self, request):

        if request.method == 'POST':
            action = request.POST.get('action')
            cart, _ = Cart.objects.get_or_create(user=request.user)
            
            if action == 'add':
                product_id = int(request.POST.get('cart_product'))
                product = get_object_or_404(ProductPage, pk=product_id)
                cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
                new_quantity = int(request.POST.get('cart_quantity', 0))
                if not created:
                    cart_item.quantity += new_quantity
                    cart_item.save()

            elif action == 'update':
                product_id = int(request.POST.get('cart_product'))
                product = get_object_or_404(ProductPage, pk=product_id)
                cart_item = get_object_or_404(CartItem, cart=cart, product=product)
                new_quantity = int(request.POST.get('cart_quantity', 0))
                if new_quantity <= 0:
                    cart_item.delete()
                else:
                    cart_item.quantity = new_quantity
                    cart_item.save()
                messages.success(request, f"Cart update successful !!")
                return redirect('shop:checkout')
            return HttpResponseRedirect(reverse('shop:checkout'))
        else:
            return render(
            request,
            self.get_template(request),
            self.get_context(request)
        )

@register_snippet
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField('ProductPage', through='CartItem')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel('user'),
        FieldPanel('items'),
    ]

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.user.email} {self.user.first_name}, {self.created_at}'
    
    def is_in_cart(self, product_id):
        """
        Check if a product is in the cart.
        """
        return self.items.filter(id=product_id).exists()
    
    def cart_quantity(self, product_id):
        """
        Get the quantity of a product in the cart.
        """
        if self.is_in_cart(product_id):
            return self.items.get(id=product_id).cartitem.quantity
        return 0
    
    def total_price(self, product_id):
        """
        Get the total price of a product in the cart (price * quantity).
        """
        if self.is_in_cart(product_id):
            product = self.items.get(id=product_id)
            if product.discount_price:
                return product.discount_price * self.cart_quantity(product_id)
            else:
                return product.original_price * self.cart_quantity(product_id)
        return 0
    
    def total_cart_price(self):
        """
        Get the total price of all items in the cart.
        """
        total_price = 0
        for item in self.cartitem_set.all():
            if item.product.discount_price:
                total_price += item.product.discount_price * item.quantity
            else:
                total_price += item.product.original_price * item.quantity
        return total_price
    
    def total_cart_quantity(self):
        """
        Get the total quantity of all items in the cart.
        """
        total_quantity = 0
        for item in self.cartitem_set.all():
            total_quantity += item.quantity
        return total_quantity

@register_snippet
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey('ProductPage', on_delete=models.CASCADE, related_name='cart_product')
    quantity = models.PositiveIntegerField(default=1)

    panels = [
        FieldPanel('cart'),
        FieldPanel('product'),
        FieldPanel('quantity'),
    ]

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.cart}, {self.product}, {self.quantity}'

@register_snippet   
class Order(models.Model): 
    cart_item = models.ForeignKey(CartItem, 
                                on_delete=models.DO_NOTHING, null=True) 
    customer = models.ForeignKey(User, 
                                 on_delete=models.CASCADE, null=True) 
    quantity = models.IntegerField(default=1) 
    price = models.IntegerField() 
    address = models.CharField(max_length=500, default='', blank=True, null=True)
    city = models.CharField(max_length=500, default='', blank=True, null=True)
    country = models.CharField(max_length=500, default='', blank=True, null=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False) 

    panels = [
        FieldPanel('cart_item'),
        FieldPanel('customer'),
        FieldPanel('quantity'),
        FieldPanel('price'),
        FieldPanel('address'),
        FieldPanel('city'),
        FieldPanel('country'),
        FieldPanel('date'),
        FieldPanel('status'),
    ]

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.customer.email} {self.customer.first_name}, {self.cart_item}, {self.quantity}, {self.price}'
  
    def placeOrder(self): 
        self.save() 
  
    @staticmethod
    def get_orders_by_customer(customer_id): 
        return Order.objects.filter(customer=customer_id).order_by('-date')