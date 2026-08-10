from django.shortcuts import render , get_object_or_404 , redirect
from .models import OrderItem, Product , Category, Review
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Product, Order, OrderItem
from .forms import UserUpdateForm , ProfileUpdateForm
from .models import Profile as ProfileModel
from django.core.paginator import Paginator
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
    paginator = Paginator(products, 3)
    page_number = request.GET.get('page')    
    page_obj = paginator.get_page(page_number)
    return render (request, 'store/product_list.html' , {
        'products': page_obj,
        'categories': categories, 
        'product_count': product_count, 
        'selected_category': selected_category,
        'search_query': search_query
    })
def add_review(request, pk):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        product = get_object_or_404(Product, id=pk)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if rating and comment:
            Review.objects.create(
                product=product,
                user=request.user,
                rating=int(rating),
                comment=comment
            )
    return redirect('product_detail', pk=pk)
def product_detail(request,pk):
    product = get_object_or_404(Product,pk=pk)
    reviews = product.reviews.all().order_by('created_at')

    return render(request,'store/product_detail.html',{'product':product, 'reviews': reviews})
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
@login_required
def decrease_cart_item(request, product_id):
    cart = Cart.objects.get(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.filter(cart=cart,product=product).first()

    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_detail')
@login_required
def remove_cart_item(request, product_id):
    cart = Cart.objects.get(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.filter(cart=cart, product=product).first()
    if cart_item:
        cart_item.delete()
    return redirect('cart_detail')
@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')

        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            phone_number=phone_number,
            address=address,
            total_price=cart.get_total_price(),
            is_paid=True  # Assuming payment is successful for simplicity
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )

        cart.items.all().delete()  # Clear the cart after checkout
        return redirect('order_success')  # Redirect to a success page after checkout
    return render(request, 'store/checkout.html', {'cart': cart})
@login_required
def order_success(request):
    return render(request, 'store/order_success.html')
@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/my_orders.html', {'orders': orders})
@login_required
def Profile(request):
    profile_obj, created = ProfileModel.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile_obj)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'ፕሮፋይልዎ በትክክል ተስተካክሏል!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile_obj)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'store/profile.html', context)
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status == 'Pending' or not order.status:
        order.delete()
        messages.success(request, f"ትዕዛዝ #{order_id} በስኬት ተስርዝዋል። ")
    else:
        messages.error(request, "ይህ ትዕዛዝ ቀድሞ ስለተላከ መሰለዝ አይቻልም።")
    return redirect('my_orders')