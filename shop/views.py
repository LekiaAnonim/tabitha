from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.shortcuts import render, redirect, HttpResponseRedirect 
from shop.models import ProductPage, Order, Cart, CartItem
from shop.models import Category
from django.views import View 
from django.views.generic import TemplateView, ListView, DetailView
from authentication.models import User

# Create your views here.
def get_products_in_cart(cart):
    """
    Get all products in a cart.
    """
    cart_items = cart.cartitem_set.all()
    products = [cart_item.product for cart_item in cart_items]
    return products

class ShopView(ListView):
    model = ProductPage
    template_name = 'shop/shop.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_context_data(self, *args, **kwargs):
        context = super(ShopView, self).get_context_data(**kwargs)
        categories = Category.objects.all()
        products = ProductPage.objects.all().order_by('first_published_at').order_by('-id')
        context['categories'] = categories
        context['products'] = products
        return context
	
    def post(self, request, *args, **kwargs):
        
        action = request.POST.get('action')
        cart, _ = Cart.objects.get_or_create(user=request.user)
        
        if action == 'add':
            product_id = int(request.POST.get('product'))
            product = get_object_or_404(ProductPage, pk=product_id)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += 1
                cart_item.save()
        elif action == 'remove':
            if cart.is_in_cart(product_id):
                cart_item = get_object_or_404(CartItem, cart=cart, product=product)
                cart_item.delete()
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
        return redirect('shop:home')
    
    def get(self , request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        products = ProductPage.objects.all().order_by('first_published_at').order_by('-id')

        cart = Cart.objects.get_or_create(user=request.user)[0]
        cart_items = cart.cartitem_set.all()
        cart_products = get_products_in_cart(cart)
        
        context['cart_products'] = cart_products
        context['cart_items'] = cart_items
        context['categories'] = categories
        context['products'] = products
        context['cart'] = cart
        return render(request, self.template_name, context)
	

class CategoryProductView(ListView):
    model = Category
    template_name = 'shop/category_product.html'
    context_object_name = 'categories'
    paginate_by = 12
	
    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return ProductPage.objects.filter(category=category).order_by('first_published_at').order_by('-id')
    
    def get_context_data(self, *args, **kwargs):
        context = super(CategoryProductView, self).get_context_data(**kwargs)
		
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        categories = Category.objects.all()
		
        if category:
            products = ProductPage.objects.filter(category=category).order_by('first_published_at').order_by('-id')
        
        context['category'] = category
        context['categories'] = categories
        context['products'] = products
        return context
	

class CheckOut(TemplateView):
    template_name = 'shop/checkout.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CheckOut, self).get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = categories
        return context
    
    def post(self, request): 
        address = request.POST.get('address') 
        city = request.POST.get('city')
        country = request.POST.get('country')
        customer = request.user
        cart = Cart.objects.get_or_create(user=request.user)[0]
        cart_items = cart.cartitem_set.all()
        # products = get_products_in_cart(cart)
        # products = ProductPage.get_products_by_id(list(cart.keys())) 
        # print(address, city, customer, cart, products) 
  
        for item in cart_items: 
            if item.product.discount_price:
                price = item.product.discount_price
            else:
                price = item.product.original_price
            order = Order(customer=customer, 
                          cart_item=item, 
                          price=price, 
                          address=address, 
                          city=city,
                          country=country,  
                          quantity=item.quantity) 
            order.save()
        return redirect('shop:checkout')
    
    def get(self , request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        cart = Cart.objects.get_or_create(user=request.user)[0]
        cart_items = cart.cartitem_set.all()
        cart_products = get_products_in_cart(cart)
        
        context['cart_products'] = cart_products
        context['cart_items'] = cart_items
        context['categories'] = categories
        context['cart'] = cart
        return render(request, self.template_name, context)
    
class UserAccountView(TemplateView):
    template_name = 'home/user-account.html'

    def get_context_data(self, *args, **kwargs):
        context = super(UserAccountView, self).get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = categories
        return context
    
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.user.id)
        # Get Post information from tempate
        first_name =  request.POST.get('first_name')
        last_name =  request.POST.get('last_name')
        region =  request.POST.get('region')
        country =  request.POST.get('country')
        address =  request.POST.get('address')
        phone =  request.POST.get('phone')
        # Update User Model
        user.first_name = first_name
        user.last_name = last_name
        user.region = region
        user.country = country
        user.residential_address = address
        user.phone_number = phone
        user.save()
        return redirect('shop:account')
    
    def get(self , request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        cart = Cart.objects.get_or_create(user=request.user)[0]
        cart_items = cart.cartitem_set.all()

        context['cart_items'] = cart_items
        context['categories'] = categories
        context['cart'] = cart
        return render(request, self.template_name, context)