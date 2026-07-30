from django.shortcuts import render , get_object_or_404
from .models import Product , Category
def product_list(request):
    category_id = request.GET.get('category')
    categories = Category.objects.all()
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    return render (request, 'store/product_list.html' , {'products': products, 'categories': categories})
def product_detail(request,pk):
    product = get_object_or_404(Product,pk=pk)
    return render(request,'store/product_detail.html',{'product':product})
