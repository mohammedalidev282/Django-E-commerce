from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('register/',views.register,name="register"),
    path('collection/',views.collection, name="collection"),
    path('collection/<str:name>/',views.collectionView, name="collection"),
    path('collection/<str:cname>/<str:pname>',views.product_details, name="product_details"),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_page, name="logout"),
    path("addtocart",views.add_To_Cart, name="addtocart"),
    path("cart",views.cart_page, name="cart"),
    path("remove_cart/<str:cid>",views.remove_cart, name="remove_cart"),
    path("fav",views.favorate_items, name="fav"),
    path("fav_page",views.favorate_page, name="fav_page"),
    path("remove_fav/<str:fid>",views.remove_fav, name="remove_fav"),
    path("payment",views.payment_page, name="payment")


]
