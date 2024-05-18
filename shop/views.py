from django.shortcuts import render, get_object_or_404, redirect
from shop.models import ProductPage, Order, Cart, CartItem
from shop.models import Category
from django.views import View 
from django.views.generic import TemplateView, ListView, DetailView
from authentication.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings # new
from django.http.response import JsonResponse # new
from django.views.decorators.csrf import csrf_exempt # new
import stripe
from home.models import TransactionOption
from guest_user.decorators import allow_guest_user
from django.contrib import messages

# Create your views here.
def get_products_in_cart(cart):
    """
    Get all products in a cart.
    """
    cart_items = cart.cartitem_set.all()
    products = [cart_item.product for cart_item in cart_items]
    return products

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

class ShopView(ListView):
    model = ProductPage
    template_name = 'shop/shop.html'
    context_object_name = 'products'
    paginate_by = 12
	
    # @method_decorator(login_required)
    @method_decorator(allow_guest_user)
    def post(self, request, *args, **kwargs):
        
        action = request.POST.get('action')
        cart, _ = Cart.objects.get_or_create(user=request.user)

        if action == 'update':
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
        
        elif action == 'add':
            product_id = int(request.POST.get('product'))
            product = get_object_or_404(ProductPage, pk=product_id)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += 1
                cart_item.save()

            messages.success(request, f"Product added successfully !!")
            # return redirect('shop:home')
        elif action == 'remove':
            if cart.is_in_cart(product_id):
                cart_item = get_object_or_404(CartItem, cart=cart, product=product)
                cart_item.delete()
            messages.success(request, f"Item removed successfully !!")
        self.object_list = self.get_queryset()
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        products = ProductPage.objects.all().order_by('first_published_at').order_by('-id')
        if self.request.user.is_authenticated:
            cart = Cart.objects.get_or_create(user=self.request.user)[0]
            cart_items = cart.cartitem_set.all()
            context['cart_items'] = cart_items
        else:
            cart = None
        context['categories'] = categories
        context['products'] = products
        context['cart'] = cart
        return render(request, self.template_name, context)  
    
    def get_context_data(self, *args, **kwargs):
        context = super(ShopView, self).get_context_data(**kwargs)
        categories = Category.objects.all()
        products = ProductPage.objects.all().order_by('first_published_at').order_by('-id')

        if self.request.user.is_authenticated:
            cart = Cart.objects.get_or_create(user=self.request.user)[0]
            cart_items = cart.cartitem_set.all()
            context['cart_items'] = cart_items
        else:
            cart = None
        context['categories'] = categories
        context['products'] = products
        context['cart'] = cart
        return context
	

class CategoryProductView(ListView):
    model = Category
    template_name = 'shop/category_product.html'
    context_object_name = 'categories'
    
    # @method_decorator(login_required)
    @method_decorator(allow_guest_user)
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

            messages.success(request, f"Product added successfully !!")
        elif action == 'remove':
            if cart.is_in_cart(product_id):
                cart_item = get_object_or_404(CartItem, cart=cart, product=product)
                cart_item.delete()
            messages.success(request, f"Product removed from cart !!")
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
        
        self.object_list = self.get_queryset()
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        products = ProductPage.objects.all().order_by('first_published_at').order_by('-id')
        if self.request.user.is_authenticated:
            cart = Cart.objects.get_or_create(user=self.request.user)[0]
            cart_items = cart.cartitem_set.all()
            context['cart_items'] = cart_items
        else:
            cart = None
        context['categories'] = categories
        context['products'] = products
        context['cart'] = cart
        return render(request, self.template_name, context)
    
    def get_context_data(self, *args, **kwargs):
        context = super(CategoryProductView, self).get_context_data(**kwargs)
		
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        categories = Category.objects.all()
		
        if category:
            products = ProductPage.objects.filter(category=category).order_by('first_published_at').order_by('-id')

        if self.request.user.is_authenticated:
            cart = Cart.objects.get_or_create(user=self.request.user)[0]
            cart_items = cart.cartitem_set.all()
            context['cart_items'] = cart_items
        else:
            cart = None
        context['cart'] = cart
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
    
    def post(self, request, *args, **kwargs): 
        address = request.POST.get('address') 
        city = request.POST.get('city')
        country = request.POST.get('country')
        email = request.POST.get('email')
        customer = request.user
        cart = Cart.objects.get_or_create(user=request.user)[0]
        cart_items = cart.cartitem_set.all()

        action = request.POST.get('action')
        if action == 'add':
            product_id = int(request.POST.get('product'))
            product = get_object_or_404(ProductPage, pk=product_id)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += 1
                cart_item.save()
            messages.success(request, f"1 product added successfully !!")

        elif action == 'reduce':
            product_id = int(request.POST.get('product'))
            product = get_object_or_404(ProductPage, pk=product_id)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity -= 1
                cart_item.save()

            messages.success(request, f"1 product removed successfully !!")
        elif action == 'remove':
            product_id = int(request.POST.get('product'))
            product = get_object_or_404(ProductPage, pk=product_id)
            if cart.is_in_cart(product_id):
                cart_item = get_object_or_404(CartItem, cart=cart, product=product)
                cart_item.delete()
            messages.success(request, f"Product deleted from cart !!")
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
        elif action == 'checkout':
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

            total_amount = sum(item.product.discount_price * item.quantity for item in cart_items)
            if total_amount:
                total_amount = total_amount
            else:
                total_amount = sum(item.product.original_price * item.quantity for item in cart_items)
            transaction_settings = TransactionOption.for_request(request=request)
            tax = round(total_amount*transaction_settings.tax_rate, 2)
            tax_rate = transaction_settings.tax_rate

            domain_url = settings.WAGTAILADMIN_BASE_URL
            stripe.api_key = settings.STRIPE_SECRET_KEY
            try:
                # Create new Checkout Session for the order
                # Other optional params include:
                # [billing_address_collection] - to display billing address details on the page
                # [customer] - if you have an existing Stripe Customer ID
                # [payment_intent_data] - capture the payment later
                # [customer_email] - prefill the email input in the form
                # For full details see https://stripe.com/docs/api/checkout/sessions/create

                # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
                checkout_session = stripe.checkout.Session.create(
                    success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                    cancel_url=domain_url + 'cancel/',
                    payment_method_types=['card'],
                    mode='payment',
                    currency= "usd",
                    customer_email = email,
                    line_items=[
                        {
                            'quantity': int(item.quantity),
                            'price_data': {
                            'currency': 'usd',
                            'unit_amount': int(item.product.discount_price*100*(1+tax_rate)),
                            'product_data': {
                                'name': str(item.product.product_name),
                                'description': str(item.product.short_description),
                                # 'images': ['https://example.com/t-shirt.png'],
                            },
                            },
                        } if item.product.discount_price else {
                            'quantity': int(item.quantity),
                            'price_data': {
                            'currency': 'usd',
                            'unit_amount': int(item.product.original_price*100*(1+tax_rate)),
                            'product_data': {
                                'name': str(item.product.product_name),
                                'description': str(item.product.short_description),
                                # 'images': ['https://example.com/t-shirt.png'],
                            },
                            },
                        } for item in cart_items
                    ]
                )
                
            except Exception as e:
                return JsonResponse({'error': str(e)})
            return redirect(checkout_session.url, code=303)
        
        # self.object_list = self.get_queryset()
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        products = ProductPage.objects.all().order_by('first_published_at').order_by('-id')
        if self.request.user.is_authenticated:
            cart = Cart.objects.get_or_create(user=self.request.user)[0]
            cart_items = cart.cartitem_set.all()
            total_amount = sum(item.product.discount_price*item.quantity for item in cart_items)
            if total_amount:
                total_amount = total_amount
            else:
                total_amount = sum(item.product.original_price*item.quantity for item in cart_items)
            transaction_settings = TransactionOption.for_request(request=request)
            tax = total_amount*(transaction_settings.tax_rate)
            total = total_amount + tax
            
            context['total'] = round(total, 2)
            context['tax'] = round(tax, 2)
            context['cart_items'] = cart_items
        else:
            cart = None
        context['categories'] = categories
        context['products'] = products
        context['cart'] = cart
        return render(request, self.template_name, context)
    
    def get(self , request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        if request.user.is_authenticated:
            cart = Cart.objects.get_or_create(user=request.user)[0]
            cart_items = cart.cartitem_set.all()
            total_amount = sum(item.product.discount_price*item.quantity for item in cart_items)
            if total_amount:
                total_amount = total_amount
            else:
                total_amount = sum(item.product.original_price*item.quantity for item in cart_items)
            transaction_settings = TransactionOption.for_request(request=request)
            tax = total_amount*(transaction_settings.tax_rate)
            total = total_amount + tax
            context['total'] = round(total, 2)
            context['tax'] = round(tax, 2)
            context['cart_items'] = cart_items
        else:
            cart = None
        context['categories'] = categories
        context['cart'] = cart
        return render(request, self.template_name, context)

class SuccessView(TemplateView):
    template_name = 'shop/success.html'


class CancelledView(TemplateView):
    template_name = 'shop/cancel.html'
class UserAccountView(LoginRequiredMixin, TemplateView):
    template_name = 'home/user-account.html'
    login_url = "authentication:login"
    redirect_field_name = "redirect_to"

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
        if request.user.is_authenticated:
            cart = Cart.objects.get_or_create(user=request.user)[0]
            cart_items = cart.cartitem_set.all()
            context['cart_items'] = cart_items
        else:
            cart = None
        context['categories'] = categories
        context['cart'] = cart
        return render(request, self.template_name, context)
    
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline
class SearchResultsList(ListView):
    model = ProductPage
    context_object_name = "products"
    template_name = "shop/search.html"

    def get_queryset(self):
        query = self.request.GET.get("search")
        search_vector = SearchVector("product_name", "full_description", "category", "original_price", "discount_price")
        search_query = SearchQuery(query)

        search_headline = SearchHeadline("product_name", search_query)
        return ProductPage.objects.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query)
        ).annotate(headline=search_headline).filter(search=search_query).order_by("-rank")
    
    def get_context_data(self, *args, **kwargs):
        context = super(SearchResultsList, self).get_context_data(**kwargs)
        categories = Category.objects.all()
        products = ProductPage.objects.all().order_by('first_published_at').order_by('-id')

        if self.request.user.is_authenticated:
            cart = Cart.objects.get_or_create(user=self.request.user)[0]
            cart_items = cart.cartitem_set.all()
            context['cart_items'] = cart_items
        else:
            cart = None
        context['categories'] = categories
        context['products'] = products
        context['cart'] = cart
        return context
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        
        action = request.POST.get('action')
        cart, _ = Cart.objects.get_or_create(user=request.user)

        if action == 'update':
            product_id = int(request.POST.get('cart_product'))
            product = get_object_or_404(ProductPage, pk=product_id)
            cart_item = get_object_or_404(CartItem, cart=cart, product=product)
            new_quantity = int(request.POST.get('cart_quantity', 0))
            if new_quantity <= 0:
                cart_item.delete()
            else:
                cart_item.quantity = new_quantity
                cart_item.save()
            return redirect('shop:checkout')
        
        elif action == 'add':
            product_id = int(request.POST.get('product'))
            product = get_object_or_404(ProductPage, pk=product_id)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += 1
                cart_item.save()
            # return redirect('shop:home')
        elif action == 'remove':
            if cart.is_in_cart(product_id):
                cart_item = get_object_or_404(CartItem, cart=cart, product=product)
                cart_item.delete()
        self.object_list = self.get_queryset()
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        products = ProductPage.objects.all().order_by('first_published_at').order_by('-id')
        if self.request.user.is_authenticated:
            cart = Cart.objects.get_or_create(user=self.request.user)[0]
            cart_items = cart.cartitem_set.all()
            context['cart_items'] = cart_items
        else:
            cart = None
        context['categories'] = categories
        context['products'] = products
        context['cart'] = cart
        return render(request, self.template_name, context)