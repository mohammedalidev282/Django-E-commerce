from django.shortcuts import render,redirect
from . models import *
from django.contrib import messages
import json
from django.http import JsonResponse
from . form import CustomUserForm
from django.contrib.auth import authenticate,login,logout
#payment integration option
import razorpay
from decimal import Decimal
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST



# Create your views here.
def home(request):
    i_Product=Product.objects.filter( trending=1)
    return render(request,"index.html",{"I_Products":i_Product})

#Login page and register page
def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    
    if request.method == "POST":
        name = request.POST.get('username')
        passkey = request.POST.get('password')
        user = authenticate(request, username=name, password=passkey)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in Successfully")
            return redirect("/")
        else:
            messages.error(request, "invalid User Name and Password")
            return redirect('login')
            
    return render(request, "login.html")
#logut page
def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logout Successfully")
        return redirect("/")





def register(request):
    form=CustomUserForm()
    if request.method == 'POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Register Successfully You Can Login")
            return redirect('login')
    return render(request, "register.html",{'form':form})


# 

def collection(request):
    Categorys=Category.objects.filter(status=0)
    return render(request, "collection.html",{ 'Categorys': Categorys })

def collectionView(request,name):
    if(Category.objects.filter(status=0,name=name)):
        Products=Product.objects.filter(category__name=name)
        return render(request, "products/index.html",{"products": Products,"category":name})
    else:
        messages.warning(request,"No Such Category Found")
        return redirect('collection') 

#product categfory viewa function
def product_details(request,cname,pname):
    if(Category.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            products=Product.objects.filter(name=pname,status=0).first()
            return render(request,"products/product_detail.html",{"products_items":products})
        else:
            message.error(request,"No such Product Found") 
            return redirect('collection')
    else:
        message.error(request," Category Not Found")
        return redirect('collection')           


def add_To_Cart(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.loads(request.body)

            pr_qt = data.get('product_qt')
            pr_id = data.get('pid')
            
            product_status = Product.objects.get(id=pr_id)
            if product_status:
                # You can keep request.user.id in filter, or use request.user
                if Cart.objects.filter(user=request.user, product_id=pr_id):
                    return JsonResponse({'status': 'Product Alredy in Cart'}, status=200)
                else:
                    if product_status.quantity >= int(pr_qt): # Make sure quantity is compared as an integer if needed
                        # FIX HERE: use request.user instead of request.user.id
                        Cart.objects.create(
                            user=request.user, 
                            product_id=pr_id, 
                            pr_qty=pr_qt
                        )    
                        return JsonResponse({'status': 'Product Add to cart'}, status=200)
                    else:
                        return JsonResponse({'status': 'Stock not Availabel'}, status=200)    

        return JsonResponse({
            'status': 'Login To Add To Cart'
        })

    return JsonResponse({
        'status': 'Invalid Access'
    })


#payment cart page
def get_razorpay_client():
    return razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

@login_required(login_url='login')
def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        total=sum(
            (item.total_cost for item in cart),
            Decimal('0.00')
        )
        return render(request,"Cart.html",
        {
        'cart':cart,
        'total':total
        })
    else:
        return redirect('login')   


def payment_page(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart = Cart.objects.filter(user=request.user)

    total = sum(
        (item.total_cost for item in cart),
        Decimal('0.00')
    )

    if not cart.exists() or total <= 0:
        messages.error(request, "Your cart is empty!")
        return redirect('cart')

    client = get_razorpay_client()

    order = client.order.create({
        'amount': int(total * 100),
        'currency': 'INR',
        'receipt': f'cart_{request.user.id}'
    })

    return render(request, 'payment.html', {
        'order': order,
        'total': total,
        'razorpay_key': settings.RAZORPAY_KEY_ID,
    })
#remove cart view function
def remove_cart(request,cid):
    cart_items=Cart.objects.get(id=cid)
    cart_items.delete()
    return redirect("/cart")
#favorates views functions

def favorate_items(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            pr_id = data.get('pid')
            product_status = Product.objects.get(id=pr_id) 
            if product_status:
                if Favorates.objects.filter(user=request.user, product_id=pr_id):
                    return JsonResponse({'status': 'Product Alredy in Favorate'}, status=200)
                else:
                    Favorates.objects.create(user=request.user, product_id=pr_id) 
                    return JsonResponse({'status': 'Product Favorate to Add'})
        else:
            return JsonResponse({'status': 'Login To Add To Cart'})
    else:
        return JsonResponse({'status': 'Invalid Access'})

#fav page view functio 
def favorate_page(request):
    if request.user.is_authenticated:  # <-- Remove parentheses () here
        fav = Favorates.objects.filter(user=request.user)
        return render(request, "Fav.html", {'fav': fav})
    else:
        return redirect("/")
#remove fav view function
def remove_fav(request,fid):
    fav_items=Favorates.objects.get(id=fid)
    fav_items.delete()
    return redirect("/fav_page")

#Payment integrations
