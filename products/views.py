from django.shortcuts import render,redirect
from .models import Product,Cart,CartItem,Order,OrderItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.http import HttpResponse

def create_superuser_temp(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'YourStrongPassword123')
        return HttpResponse('Superuser created!')
    return HttpResponse('Already exists')
@never_cache
def product_list(request):
    products=Product.objects.all()
    return render(request,'products/Productlist.html',{'products':products})
@never_cache
def product_detail(request,id):
    product=Product.objects.get(id=id)
    return render(request,'products/productdetail.html',{'product':product})
@login_required
def add_to_cart(request,id):
    print(request.method)
    if request.method=='POST':
        if not request.user.is_authenticated:
            return JsonResponse({'success':False,'error':'unAuthenticated'})
        product=Product.objects.get(id=id)
        if not product.stock<=0:
            cart,created=Cart.objects.get_or_create(user=request.user)
            cartitems,created=CartItem.objects.get_or_create(product=product,cart=cart)
            cartitems.quantity+=1
            cartitems.save()
            return JsonResponse({'success':True})
        else:
            return JsonResponse({"success":False,'error':'noStock'})
    else:
        return JsonResponse({'success':False,'error':'Invalid request'})

@login_required
def go_to_cart(request):
    cart,created=Cart.objects.get_or_create(user=request.user)
    cartitems=CartItem.objects.filter(cart=cart)
    return render(request,'products/cart.html',{'cartitems':cartitems})

def placeorder(request):
    if request.method=='POST':
        if UserProfile.objects.filter(user=request.user).exclude(address='').exists():
            print(request.method)
            profile=UserProfile.objects.get(user=request.user)
            order=Order.objects.create(user=request.user,address=profile.address)
            cart=Cart.objects.get(user=request.user)
            cartitems=CartItem.objects.filter(cart=cart)
            for item in cartitems:
                OrderItem.objects.create(order=order,product=item.product,quantity=item.quantity)
                item.product.stock-=item.quantity
                item.product.save()
            cartitems.delete()
            return JsonResponse({'success':True})
        else:
            return JsonResponse({'success':False,'error':'Profile not created'})
    else:
        return JsonResponse({'success':False,'error':'Invalid request'})

@login_required
def go_to_ordereditems(request):
    order=Order.objects.filter(user=request.user).order_by("-placed_at")
    return render(request,'products/ordereditems.html',{'orders':order})

@login_required
def buy_item(request,id):
    print(request.method)
    if request.method=='POST':
        if UserProfile.objects.filter(user=request.user).exists():
            profile=UserProfile.objects.get(user=request.user)
            order=Order.objects.create(user=request.user,address=profile.address)
            product=Product.objects.get(id=id)
            if not product.stock<=0:
                OrderItem.objects.create(order=order,product=product,quantity=1)
                product.stock-=1
                product.save()
                messages.success(request,'Order has been placed!')
                return JsonResponse({'success':True,'new_stock':product.stock})
            else:
                return JsonResponse({'success':False,'error':'Out of stock!'})
        else:
            messages.warning(request,'You have to signup or login before adding products to cart!')
            return JsonResponse({'success':False,'error':'Please complete your profile first!'})
    else:
        return JsonResponse({'success':False,'error':'Invalid request!'})
def home(request):
    return render(request,'products/home.html')