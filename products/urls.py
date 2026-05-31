from django.urls import path
from . import views 

urlpatterns=[
    path('',views.product_list,name="product_list"),
    path('<int:id>/',views.product_detail,name="product_detail"),
    path("cart/<int:id>",views.add_to_cart,name='add_to_cart'),
    path('cart/',views.go_to_cart,name='go_to_cart'),
    path('placeorder/',views.placeorder,name='placeorder'),
    path('ordereditems/',views.go_to_ordereditems,name='ordereditems'),
    path('buyitem/<int:id>',views.buy_item,name='buy_item'),
    path('',views.home,name='home'),
]