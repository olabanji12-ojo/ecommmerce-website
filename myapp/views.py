from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import RegisterCreationForm, ProductForm
from .models import *
from django.core.paginator import Paginator
import json
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages





@login_required(login_url='login_page')
def home_page(request):
    customer = request.user.customer  # Assuming user is a Customer; adjust if needed.
    order, created = Order.objects.get_or_create(customer=customer)
    products = Product.objects.all()
    # Use filter instead of get
    items = Orderitem.objects.filter(order=order)  # Get all items related to the order
    
    context = {'products': products, 'items': items, 'order': order}
    return render(request, 'home_page.html', context)



# @login_required(login_url='login_page')
def login_page(request):
    if request.user.is_authenticated:
        return redirect('home_page')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login Successful!')
            return redirect('home_page')
        else:
            messages.error(request, 'Username or Password is Incorrect!')

            
    context = {}
    return render(request, 'login_page.html', context)


def logout_page(request):
    
    logout(request)
    messages.success(request, 'You have successfully logged out!')
    return redirect('login_page')


def register_page(request):
    form = RegisterCreationForm()
    if request.method == 'POST':
        form = RegisterCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home_page')
    
    context = {'form' : form}
    return render(request, 'register_page.html', context)


@login_required(login_url='login_page')
def cart(request):
    
    
    products = Product.objects.all()

    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer)
    items = Orderitem.objects.filter(order=order) 

    context = {'items': items, 'order': order}
    
    return render(request, 'cart.html', context)



def checkout(request):
    products = Product.objects.all()

    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer)
    items = Orderitem.objects.filter(order=order) 

    context = {'items': items, 'order': order}

    return render(request, 'checkout.html', context)


def update_cart(request):
    data = json.loads(request.body)
    
    product_id = data.get('product_id')
    action = data.get('action')
    product = Product.objects.get(id=product_id)
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer)
    items, created = Orderitem.objects.get_or_create(product=product, order=order)
    
    if action == 'add':
        items.quantity += 1
        messages.info(request, 'product added')
        
    elif action == 'remove':
        items.quantity -= 1
        messages.info(request, 'product removed')
        
    items.save()
    
    if items.quantity <= 0:
        items.delete()
        # items.save()
        
    return JsonResponse('item was added', safe=False)


def shipping_info(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # product = Product.objects.get(id=product_id)
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer)
        name = data.get('name')
        email = data.get('email')
        
        
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data.get('name'),
            city = data.get('city'),
            state = data.get('state'),
            zipcode = data.get('zipcode')
            
        )
        order_items = Orderitem.objects.filter(order=order)
        order_items.delete()
        messages.success(request, 'Your Payment was successful!')
        # order_items.save()

    return JsonResponse('payment button was clicked', safe=False)

def superuser_required(view_func):
    """
    Custom decorator to allow only superusers.
    """
    decorated_view_func = user_passes_test(
        lambda user: user.is_superuser,
        login_url='/'  # Redirects to login page if not a superuser
    )(view_func)
    return decorated_view_func


@superuser_required
def create_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home_page')
    
    context = {'form':form}
    return render(request, 'create_product.html', context)
    
# Create your views here.
