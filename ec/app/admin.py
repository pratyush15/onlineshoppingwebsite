from django.contrib import admin
from .models import Product  
from .models import Customer, Cart, OrderPlaced, Wishlist    
# Register your models here.  
@admin.register(Product) 
class ProductModelAdmin(admin.ModelAdmin): 
    list_display = ['id','title','discounted_price','category','product_image']      

@admin.register(Customer)    
class CustomerModelAdmin(admin.ModelAdmin): 
    list_display = ['id', 'user', 'locality','city','state','zipcode']  

@admin.register(Cart)    
class CartModelAdmin(admin.ModelAdmin): 
    list_display = ['id', 'user', 'product','quantity']   

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin): 
    list_display = ['id', 'user','product','quantity']      

@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin): 
    list_display = ['id','user','product'] 