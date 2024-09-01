from django.db.models import Count, Q , F   
from django.http import HttpResponse, JsonResponse 
from django.shortcuts import render, redirect   
from django.views import View 
from urllib import request   
from .models import Product, Customer, Cart, OrderPlaced, Wishlist  
from .forms import CustomerRegistrationForm, CustomerProfileForm    
from django.contrib import messages     
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator     

# Create your views here.   

@login_required  
def home(request):           
    totalitem=0   
    wishitem=0 
    if request.user.is_authenticated: 
        totalitem=len(Cart.objects.filter(user=request.user))     
        wishitem=len(Wishlist.objects.filter(user=request.user))
    return render(request,"app/home.html",locals())                

@login_required 
def about(request):       
    totalitem=0    
    wishitem=0 
    if request.user.is_authenticated: 
        totalitem=len(Cart.objects.filter(user=request.user))   
        wishitem=len(Wishlist.objects.filter(user=request.user)) 
    return render(request,"app/about.html",locals())  

@login_required    
def contact(request):    
    totalitem=0   
    wishitem=0 
    if request.user.is_authenticated: 
        totalitem=len(Cart.objects.filter(user=request.user))   
        wishitem=len(Wishlist.objects.filter(user=request.user))      
    return render(request,"app/contact.html",locals())        

@login_required 
def cancel(request):
    totalitem=0 
    wishitem=0 
    if request.user.is_authenticated: 
        totalitem=len(Cart.objects.filter(user=request.user)) 
        wishitem=len(Cart.objects.filter(user=request.user)) 
    return render(request,"app/cancel.html",locals())   

@login_required  
def wishlist(request):  
    totalitem=0  
    wishitem=0   
    wish=Wishlist.objects.filter(user=request.user)  
    if request.user.is_authenticated:   
        totalitem=len(Cart.objects.filter(user=request.user))  
        wishitem=len(Wishlist.objects.filter(user=request.user)) 
    return render(request,"app/wishlist.html",locals())            

@login_required 
def continued(request):   
    global tamount         
    my_integer = tamount  
    user = request.user     
    cart = Cart.objects.filter(user=user)  
    cart=Cart.objects.filter(user=user)  
    order_items = []

    for c in cart: 
        order_items.append(OrderPlaced(user=user, product=c.product, quantity=c.quantity))

    OrderPlaced.objects.bulk_create(order_items) 

    cart.delete()        
    totalitem=0  
    wishitem=0    
    if request.user.is_authenticated:   
        totalitem=len(Cart.objects.filter(user=request.user))  
        wishitem=len(Wishlist.objects.filter(user=request.user)) 
    context = {'my_integer': my_integer,'totalitem' : totalitem,'wishitem': wishitem}        
    return render(request,"app/continue.html",context)             

@login_required 
def add_to_cart(request):    
    user=request.user   
    product_id=request.GET.get('prod_id')         
    product=Product.objects.get(id=product_id)      
    Cart(user=user, product=product).save()  
    return redirect("/cart") 

@login_required  
def show_cart(request):   
    user=request.user 
    cart=Cart.objects.filter(user=user)  
    amount=0 
    for p in cart:   
        value=p.quantity * p.product.discounted_price  
        amount=amount+value 
    totalamount=amount+40                      # Rs.40 is the shipping charges      
    totalitem=0  
    wishitem=0 
    if request.user.is_authenticated: 
        totalitem=len(Cart.objects.filter(user=request.user))   
        wishitem=len(Wishlist.objects.filter(user=request.user))
    return render(request,"app/add-to-cart.html",locals())      

@login_required  
def plus_cart(request):   
    if request.method=='GET':  
        prod_id=request.GET['prod_id']     
        c=Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first() 
        c.quantity+=1 
        c.save()  
        user=request.user 
        cart=Cart.objects.filter(user=user) 
        amount=0 
        for p in cart:   
            value=p.quantity * p.product.discounted_price  
            amount=amount+value 
        totalamount=amount+40                     
        data={
            'quantity':c.quantity,
            'amount':amount, 
            'totalamount':totalamount 
        } 
        return JsonResponse(data)      

@login_required     
def minus_cart(request):   
    if request.method=='GET':  
        prod_id=request.GET['prod_id']     
        c=Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first() 
        c.quantity-=1   
        c.save() 
        user=request.user 
        cart=Cart.objects.filter(user=user) 
        amount=0 
        for p in cart:   
            value=p.quantity * p.product.discounted_price  
            amount=amount+value 
        totalamount=amount+40                     
        data={
            'quantity':c.quantity,
            'amount':amount, 
            'totalamount':totalamount 
        } 
        return JsonResponse(data)   

@login_required       
def remove_cart(request):    
    if request.method=='GET':  
        prod_id=request.GET['prod_id']      
        c=Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first() 
        c.delete()  
        user=request.user 
        cart=Cart.objects.filter(user=user) 
        amount=0 
        for p in cart:   
            value=p.quantity * p.product.discounted_price   
            amount=amount+value  
        totalamount=amount+40                     
        data={
            'amount':amount, 
            'totalamount':totalamount 
        } 
        return JsonResponse(data)       

@login_required 
def plus_wishlist(request): 
    if request.method=='GET': 
        prod_id=request.GET['prod_id'] 
        product=Product.objects.get(id=prod_id) 
        user=request.user
        Wishlist(user=user,product=product).save() 
        data={
            'message':'Wishlist Added Successfully',
        } 
        return JsonResponse(data)   

@login_required    
def minus_wishlist(request):   
    if request.method=='GET': 
        prod_id=request.GET['prod_id'] 
        product=Product.objects.get(id=prod_id) 
        user=request.user 
        Wishlist.objects.filter(user=user,product=product).delete()   
        data={
            'message':'Wishlist removed successfully',
        } 
        return JsonResponse(data)   
      
@login_required  
def search(request): 
    query=request.GET['search']      #get a search text written in the text field  
    totalitem=0   
    wishitem=0  
    if request.user.is_authenticated: 
        totalitem=len(Cart.objects.filter(user=request.user))    
        wishitem=len(Wishlist.objects.filter(user=request.user)) 
    product=Product.objects.filter(Q(title__icontains=query))   
    return render(request,"app/search.html",locals()) 

@method_decorator(login_required, name='dispatch') 
class checkout(View):   
    tamount=0      #Initialize as a class attribute  
    camount=0      #Initialize as a class attribute 
    def get(self,request):       
        global tamount   
        global camount 
        user=request.user 
        add=Customer.objects.filter(user=user) 
        cart_items=Cart.objects.filter(user=user)   
        famount=0 
        for p in cart_items:    
            value=p.quantity * p.product.discounted_price  
            famount=famount+value 
        totalamount=famount+40   
        tamount=totalamount         #Set the value to the class attribute    
        camount=totalamount   
        totalitem=0   
        wishitem=0  
        if request.user.is_authenticated: 
            totalitem=len(Cart.objects.filter(user=request.user))    
            wishitem=len(Wishlist.objects.filter(user=request.user))
        return render(request,'app/checkout.html',locals())  

@method_decorator(login_required, name='dispatch') 
class CategoryView(View):  
    def get (self,request,val):    
        product=Product.objects.filter(category=val)    
        title=Product.objects.filter(category=val).values('title').annotate(total=Count('title'))     
        totalitem=0  
        wishitem=0 
        if request.user.is_authenticated: 
            totalitem=len(Cart.objects.filter(user=request.user))  
            wishitem=len(Wishlist.objects.filter(user=request.user)) 
        return render(request,"app/category.html",locals())       

@method_decorator(login_required, name='dispatch') 
class CategoryTitle(View):    
    def get(self,request,val): 
        product=Product.objects.filter(title=val)  
        title=Product.objects.filter(category=product[0].category).values('title')     
        totalitem=0  
        wishitem=0 
        if request.user.is_authenticated: 
            totalitem=len(Cart.objects.filter(user=request.user)) 
            wishitem=len(Wishlist.objects.filter(user=request.user))
        return render(request,"app/category.html",locals())    
     
@method_decorator(login_required, name='dispatch')       
class ProductDetail(View): 
    def get (self,request,pk):  
             product = Product.objects.get(pk=pk)   
             wishlist=Wishlist.objects.filter(Q(product=product) & Q(user=request.user))    
             totalitem=0  
             wishitem=0       
             if request.user.is_authenticated:   
                 totalitem=len(Cart.objects.filter(user=request.user))   
                 wishitem=len(Wishlist.objects.filter(user=request.user)) 
             return render(request,"app/productdetail.html",locals())   
    
class CustomerRegistrationView(View):  
    def get(self,request):      
        form=CustomerRegistrationForm()      
        return render(request,'app/customerregistration.html',locals())   
    def post(self,request): 
        form=CustomerRegistrationForm(request.POST)   
        if form.is_valid():   
            form.save()   
            messages.success(request,"Congratulations! User created successfully.")   
        else: 
            messages.warning(request,"Invalid user data.")    
        return render(request,'app/customerregistration.html',locals())    
      
@method_decorator(login_required,name='dispatch') 
class ProfileView(View):   
    def get(self, request):   
        form=CustomerProfileForm()   
        totalitem=0  
        wishitem=0 
        if request.user.is_authenticated: 
            totalitem=len(Cart.objects.filter(user=request.user))  
            wishitem=len(Wishlist.objects.filter(user=request.user))
        return render(request,'app/profile.html',locals())  
    def post(self, request):  
        form=CustomerProfileForm(request.POST) 
        if form.is_valid():  
            user=request.user 
            name=form.cleaned_data['name'] 
            locality=form.cleaned_data['locality']   
            city=form.cleaned_data['city'] 
            mobile=form.cleaned_data['mobile']  
            zipcode=form.cleaned_data['zipcode']  
            state=form.cleaned_data['state']    

            reg=Customer(user=user, name=name, locality=locality, city=city, mobile=mobile, zipcode=zipcode, state=state) 
            reg.save()  
            messages.success(request,"Congratulations! Profile saved successfully")  
        
        else: 
            messages.warning("Invalid input data!")  
        return render(request,'app/profile.html',locals())    

@login_required    
def address(request): 
    add=Customer.objects.filter(user=request.user)   
    totalitem=0  
    wishitem=0
    if request.user.is_authenticated: 
        totalitem=len(Cart.objects.filter(user=request.user))  
        wishitem=len(Wishlist.objects.filter(user=request.user))
    return render(request,"app/address.html",locals())    

@login_required 
def orderplaced(request):    
    cust_id=request.GET.get('cust_id')   
    user=request.user 
    customer=Customer.objects.get(id=cust_id)    
    cart=Cart.objects.filter(user=user) 
    for c in cart: 
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()  
        c.delete()   
    return redirect("/orders")  

@login_required 
def orders(request):    
        order_placed=OrderPlaced.objects.filter(user=request.user)      
        totalitem=0      
        wishitem=0
        if request.user.is_authenticated: 
            totalitem=len(Cart.objects.filter(user=request.user))  
            wishitem=len(Wishlist.objects.filter(user=request.user))
        return render(request,"app/orders.html",locals())        

@method_decorator(login_required,name='dispatch') 
class updateAddress(View):                       
    def get(self,request,pk):   
        add=Customer.objects.get(pk=pk) 
        form=CustomerProfileForm(instance=add)  
        return render(request,"app/updateAddress.html",locals())    
    def post(self,request,pk):  
        form=CustomerProfileForm(request.POST)  
        if form.is_valid():  
            add=Customer.objects.get(pk=pk) 
            add.name=form.cleaned_data['name'] 
            add.locality=form.cleaned_data['locality'] 
            add.city=form.cleaned_data['city'] 
            add.mobile=form.cleaned_data['mobile']  
            add.zipcode=form.cleaned_data['zipcode'] 
            add.state=form.cleaned_data['state']     
            add.save()    
            messages.success(request,"Congratulations! Profile updated successfully")   
        else: 
            messages.warning("Invalid input data!")    
        return redirect("address")    
 


    
   
    
    




         
   
 