from django.shortcuts import render,redirect
from .models import Product,Cart,CartItem,Order,OrderItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile
from django.views.decorators.cache import never_cache
# Create your views here.
@never_cache
def product_list(request):
    products=Product.objects.filter(stock__gt=0)
    return render(request,'products/Productlist.html',{'products':products})
@never_cache
def product_detail(request,id):
    product=Product.objects.get(id=id)
    return render(request,'products/productdetail.html',{'product':product})
@login_required
def add_to_cart(request,id):
    if not request.user.is_authenticated:
        messages.warning(request,'You have to signup or login before adding products to cart!')
        return redirect(f'accounts/login/?next=/products/{id}/')
    product=Product.objects.get(id=id)
    cart,created=Cart.objects.get_or_create(user=request.user)
    cartitems,created=CartItem.objects.get_or_create(product=product,cart=cart)
    cartitems.quantity+=1
    cartitems.save()
    messages.success(request,"Item has been added to cart")
    return redirect('product_detail',id=id)

@login_required
def go_to_cart(request):
    cart,created=Cart.objects.get_or_create(user=request.user)
    cartitems=CartItem.objects.filter(cart=cart)
    return render(request,'products/cart.html',{'cartitems':cartitems})

def placeorder(request):
    if UserProfile.objects.filter(user=request.user).exists():
        profile=UserProfile.objects.get(user=request.user)
        order=Order.objects.create(user=request.user,adress=profile.adress)
        cart=Cart.objects.get(user=request.user)
        cartitems=CartItem.objects.filter(cart=cart)
        for item in cartitems:
            OrderItem.objects.create(order=order,product=item.product,quantity=item.quantity)
            item.product.stock-=item.quantity
            item.product.save()
        cartitems.delete()
        messages.success(request,'Orders have been placed!')
        return redirect('go_to_cart')
    else:
        messages.warning(request,'You need to have a valid profile before buying items!')
        return redirect('go_to_cart')

@login_required
def go_to_ordereditems(request):
    order=Order.objects.filter(user=request.user).order_by("-placed_at")
    return render(request,'products/ordereditems.html',{'orders':order})

@login_required
def buy_item(request,id):
    if UserProfile.objects.filter(user=request.user).exists():
        profile=UserProfile.objects.get(user=request.user)
        order=Order.objects.create(user=request.user,adress=profile.adress)
        product=Product.objects.get(id=id)
        OrderItem.objects.create(order=order,product=product,quantity=1)
        product.stock-=1
        product.save()
        messages.success(request,'Order has been placed!')
        return redirect('product_list')
    else:
        messages.warning(request,'You have to signup or login before adding products to cart!')
        return redirect(f'accounts/login/?next=/products/{id}/')
def home(request):
    return render(request,'products/home.html')