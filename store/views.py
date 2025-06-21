from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django import forms
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth import logout  # ✅ import at the top
from django.db import models
from .models import Product 
from .models import Order  # adjust model import if needed
from django.utils import timezone
from django.http import HttpResponse


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'store/my_orders.html', {'orders': orders})


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        help_texts = {
            'username': '',
            'password1': '',
            'password2': '',
        }
def clean_password1(self):
        password = self.cleaned_data.get('password1')
        import re
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters.")
        if not re.search(r"[A-Z]", password):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", password):
            raise forms.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", password):
            raise forms.ValidationError("Password must contain at least one number.")
        if not re.search(r"[!@#$%^&*()_+{}:\"<>?|\\[\];',./`~]", password):
            raise forms.ValidationError("Password must contain at least one special character.")
        return password

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def home_view(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})
# Product detail page
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

# Add to cart
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1
    request.session['cart'] = cart
    return redirect('cart')

# View cart
def cart_view(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []
    total_price = 0

    for product in products:
        quantity = cart[str(product.id)]
        total = product.price * quantity
        total_price += total
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total': total
        })

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

# ✅ Checkout view
@login_required
def checkout_view(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']
        

        total_price = 0
        for product in products:
            quantity = cart[str(product.id)]
            total_price += product.price * quantity

        order = Order.objects.create(
    customer_name=request.POST['name'],
    customer_email=request.POST['email'],
    product=product,
    quantity=1,
    address=request.POST['address'],
    total_price=product.price,
)

        for product in products:
            quantity = cart[str(product.id)]
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                item_price=product.price
            )

        request.session['cart'] = {}  # Clear cart after order
        return redirect('home')
    

    return render(request, 'store/checkout.html')
def thank_you(request):
    return render(request, 'store/thankyou.html')

@login_required
def my_orders_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/my_orders.html', {'orders': orders})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid login credentials.")
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please login.")
            return redirect('login')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'store/register.html', {'form': form})

@login_required
def buy_now(request, product_id):
    
    product = get_object_or_404(Product, id=product_id)


    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        address = request.POST.get("address")

        print("name:", name)
        print("email:", email)
        print("address:", address)

        if not all([name, email, address]):
            return HttpResponse("Missing required fields")
        total_price = product.price

        order = Order.objects.create(
            product=product,
            user=request.user,
            customer_name=name,
            customer_email=email,
            address=address,
            total_price=total_price,
            created_at=timezone.now()
        )

        return render(request, 'store/thankyou.html', {
    'product': product,
    'total_price': total_price,
    'name': name,
})

            

    return render(request, "store/buy_now.html", {"product": product})


@login_required
def view_cart(request):
    cart_items = OrderItem.objects.filter(user=request.user, ordered=False)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        del cart[product_id_str]
        request.session['cart'] = cart

    return redirect('cart')

def checkout(request):
    cart = request.session.get('cart', {})
    products = []

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        products.append({
            'product': product,
            'quantity': quantity,
            'subtotal': product.price * quantity
        })

    total_price = sum(item['subtotal'] for item in products)

    return render(request, 'checkout.html', {
        'products': products,
        'total_price': total_price
    })


def cart_view(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []
    total_price = 0

    for product in products:
        quantity = cart[str(product.id)]
        total = product.price * quantity
        total_price += total
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total': total
        })

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })
def product_detail(request, product_id):
    print("product_id:", product_id)
    product = get_object_or_404(Product, id=product_id)
    print("product:", product)
    return render(request, 'store/product_detail.html', {'product': product})
