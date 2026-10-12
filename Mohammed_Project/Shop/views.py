from django.shortcuts import render,redirect
from . models import *
from django.contrib import messages
import json
from django.http import JsonResponse
from . form import CustomUserForm
from django.contrib.auth import authenticate,login,logout


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
            product_status=Product.objects.get(id=pr_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id,product_id=pr_id):
                    return JsonResponse({'status':'Product Alredy in Cart'},status=200)
                else:
                    if product_status.quantity>=pr_qt:
                        Cart.objects.create(user=request.user.id,product_id=pr_id,product_qty=pr_qt)    
                        return JsonResponse({'status':'Product Add to cart'},status=200)
                    else:
                        return JsonResponse({'status':'Stock not Availabel'},status=200)    
            

        return JsonResponse({
            'status': 'Login To Add To Cart'
        })

    return JsonResponse({
        'status': 'Invalid Access'
    })    