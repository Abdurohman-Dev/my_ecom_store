from django.shortcuts import render , get_object_or_404 , redirect
from .models import Product , Category
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Product
def product_list(request):
    category_id = request.GET.get('category')
    search_query = request.GET.get('search')
    categories = Category.objects.all()
    products = Product.objects.all()
    if category_id:
        products = Product.objects.filter(category_id=category_id)
        selected_category = int(category_id)
    else:
        selected_category = None
    if search_query:
        products = products.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
    product_count = products.count()

    
    return render (request, 'store/product_list.html' , {
        'products': products,
        'categories': categories, 
        'product_count': product_count, 
        'selected_category': selected_category,
        'search_query': search_query
    })
def product_detail(request,pk):
    product = get_object_or_404(Product,pk=pk)
    return render(request,'store/product_detail.html',{'product':product})
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'አካውንትህ  በትክክል ተፈጥሯል! እባክዎን ወደ መግቢያ ገጽ ይግቡ.')
            return redirect('login')  # Redirect to the login page after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'store/signup.html', {'form': form})
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_detail')
@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'store/cart_detail.html', {'cart': cart})
    