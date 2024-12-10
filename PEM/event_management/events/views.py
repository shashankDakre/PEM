from events.models import Users,Profile_pic,Payments,Bookings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password, check_password
from .models import Event, Category
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
import razorpay
import random
from django.contrib.auth import logout as auth_logout
from .models import Users, Host_register, Category, Event


def signup(request):
    if request.method=="POST":
        fullName=request.POST['fullName']
        phoneNumber = request.POST['phoneNumber']
        Email = request.POST['Email']
        city = request.POST['city']
        state = request.POST['state']
        address = request.POST['address']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']

        if confirmPassword == password:
            if Users.objects.filter(Email=Email).exists():
                messages.info(request,'Email exists')
                return redirect('/signup/')
            elif Users.objects.filter(phoneNumber=phoneNumber).exists():
                messages.info(request,'Number already Exists')
                return redirect('/signup/')
            else:
                password = make_password(password)
                customer = Users.objects.create(fullName=fullName,Email=Email,state=state,city=city,address=address,phoneNumber=phoneNumber,password=password)
                customer.save()
                return redirect('/login/')
        else:
            messages.info(request,'Password and confirm password does not match')
            return redirect('/signup/')
    return render(request, 'signup.html')
###########################################################
def login(request):
    if request.method == "POST":
        Email = request.POST.get('Email')  
        password = request.POST.get('password')

        if not Email or not password:
            messages.info(request, 'Both email and password are required.')
            return redirect('/login/')
        
        try:
            
            customer = Users.objects.get(Email=Email)

            
            if check_password(password, customer.password):
                
                request.session['id'] = customer.id
                return redirect('/index/')
            else:
                
                messages.info(request, 'Invalid credentials. Please check your password.')
                return redirect('/login/')

        except ObjectDoesNotExist:
           
            messages.info(request, 'Email does not exist.')
            return redirect('/login/')
 
    return render(request, 'login.html')

# views.py
# def logout(request):
#     print(f'User before logout: {request.user}')
    
#     # Check if the user is authenticated
#     if request.user.is_authenticated:
#         auth_logout(request)  # Use Django's built-in logout function
#         print(f'User logged out: {request.user}')
#         return redirect('home')  # Redirect to the home page (or any other page)
#     else:
# 
#         return redirect('/') 

###############################################################3

def host_register(request):
    if request.method == "POST":
        fullName=request.POST['fullName']
        phoneNumber = request.POST['phoneNumber']
        Email = request.POST['Email']
        city = request.POST['city']
        state = request.POST['state']
        address = request.POST['address']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']
      
        if password == confirmPassword :
            if Host_register.objects.filter(email=Email).exists():
                messages.info(request, "Email Exists, Please try with new email")
                return redirect('/host_register/')
            elif Host_register.objects.filter(mobile = phoneNumber).exists():
                messages.info(request, "Mobile Number Exists, Please try with new number")
                return redirect('/host_register/')
            else:
                password = make_password(password)
                new_customer = Host_register.objects.create(name=fullName, email=Email, mobile=phoneNumber, city=city, state=state, address=address,password=password)
                new_customer.save()
                return redirect('/host_login/')
        else:
            messages.info(request, "Password did'nt match")
            return redirect('/host_register/')

    return render(request,'host_register.html')

#############################################################################

def host_login(request):
    if request.method == "POST":
        
        Email = request.POST.get('Email')  
        password = request.POST.get('password')

        
        if not Email or not password:
            messages.info(request, 'Both email and password are required.')
            return redirect('/host_login/')
        
        try:
        
            host = Host_register.objects.get(email=Email)

            
            if check_password(password, host.password):
               
                request.session['host_id'] = host.id
                return redirect('/host_profile/')
            else:
               
                messages.info(request, 'Invalid credentials. Please check your password.')
                return redirect('/host_login/')

        except ObjectDoesNotExist:
       
            messages.info(request, 'Email does not exist.')
            return redirect('/host_login/')
    
   
    return render(request, 'host_login.html')

###################################################################

def host_profile(request):
    user = request.session.get('host_id')
    user = Host_register.objects.get(id =user)
    events= Event.objects.filter(host=user)
    return render(request,"host_profile.html",{"user":user,"events":events}) 
    # try:
    #   profile_pic = Profile_pic.objects.get(user=user)
    #   return render (request,"host_profile.html",{'user':user,'profile_pic':profile_pic})
    # except Profile_pic.DoesNotExist:
    #   return render(request,"host_profile.html",{"reads":user}) 



####################################################


def host_logout(request):
    customer = request.session.get('host_id')
    request.session.flush()
    return redirect('/host_login/')

#####################################################

def logout(request):
    request.session.flush()
    return redirect('/')

#######################################################

def profile_pic(request, id=None):
    user_id = request.session.get('id')  
    
    if not user_id:
        return redirect('/login/')  
    
    try:
       
        user = Users.objects.get(id=user_id)
        profile_picture, created = Profile_pic.objects.get_or_create(user=user)

        if request.method == "POST":
           
            profile_pic = request.FILES.get("profile_pic")
            if profile_pic:
                profile_picture.profile_pic = profile_pic  
                profile_picture.save() 

               
                messages.success(request, 'Profile picture uploaded successfully!')

       
        return render(request, 'profile.html', {'user': user, 'profile_pic': profile_picture})

    except Users.DoesNotExist:
        messages.error(request, "User not found")
        return redirect('/login/')  
        
####################################################################


def profile(request):
    user_id = request.session.get('id')
    if not user_id:
        return redirect('/login/')
    try:
        
        user = Users.objects.get(id=user_id)
    except Users.DoesNotExist:
        
        return HttpResponse("User not found. Please login again.", status=404)
    try:
        bookings=Bookings.objects.filter(user=user)
        profile_pic = Profile_pic.objects.get(user=user)
        return render (request,"profile.html",{'user':user,'profile_pic':profile_pic,'bookings':bookings})
    except Profile_pic.DoesNotExist:
      bookings=Bookings.objects.filter(user=user)
      return render(request,"profile.html",{"user":user,'bookings':bookings})    

###############################################################

def delete_profile(request, profile_id):
    user_id = request.session.get('id')
    
    if not user_id:
        return redirect('/login/')  
    
    try:
        
        profile_picture = Profile_pic.objects.get(id=profile_id)

        
        if profile_picture.user.id == user_id:
            
            profile_picture.delete()
            messages.success(request, "Profile picture deleted successfully.")
        else:
            messages.error(request, "You are not authorized to delete this profile picture.")
        
    except Profile_pic.DoesNotExist:
        messages.error(request, "Profile picture not found.")

    return redirect('/profile/')     

###################################################################

def home(request):
    return render(request, 'home.html')

def index(request):
    return render(request, 'index.html')

#####################################################################
def events(request):
    return render(request, 'events.html')

################################################################

def add_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        event_date = request.POST.get('event_date')
        description = request.POST.get('description')
        location = request.POST.get('location')
        category_name = request.POST.get('category')
        image = request.FILES.get('image')
        ticket_price = request.POST.get('ticket_price')
        
        
        user_id = request.session.get('host_id')
        
        try:
            host = Host_register.objects.get(id=user_id)
            
        except ( Host_register.DoesNotExist):
            return HttpResponse("host information not found.", status=404)

        if not title or not event_date or not description or not location or not category_name or not ticket_price:
            return HttpResponse("Some required fields are missing.", status=400)

   
        try:
            category = Category.objects.get(name=category_name)  
        except Category.DoesNotExist:
            
            category = Category.objects.create(name=category_name)

        try:
            
            event = Event.objects.create(
                host=host,  
                title=title,
                event_date=event_date,
                description=description,
                location=location,
                category=category,  
                image=image,
                ticket_price=ticket_price  
            )

            return redirect('/host_profile/')

        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=500)

    return render(request, 'add_event.html')


################################################################


def event_detail(request,id):
    try:
        
        event = Event.objects.get(id=id)
        bookings=Bookings.objects.filter(event=event)

        return render(request, 'event_detail.html', {'event': event,'bookings':bookings})

    except Event.DoesNotExist:
        return HttpResponse("Event not found", status=404)


################################################################


def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})

def music(request):
    events = Event.objects.filter(category='Music')
    return render(request, 'music.html', {'events': events})

def sports(request):
    events = Event.objects.filter(category='Sports')
    return render(request, 'sports.html', {'events': events})

def food(request):
    events = Event.objects.filter(category='Food')
    return render(request, 'food.html', {'events': events})

def tech(request):
    events = Event.objects.filter(category='Technology')
    return render(request, 'tech.html', {'events': events})

def fashion(request):
    events = Event.objects.filter(category='Fashion')
    return render(request, 'fashion.html', {'events': events})

def workshop(request):
    events = Event.objects.filter(category='Workshop')
    return render(request, 'workshop.html', {'events': events})

################################################################

def checkout(request, event_id):
   
    event = get_object_or_404(Event, id=event_id)

    
    quantity = request.GET.get('quantity', 1)  
    total_price = request.GET.get('total_price', event.price) 

    try:
        quantity = int(quantity)
        total_price = float(total_price)
    except ValueError:
        quantity = 1
        total_price = event.price

    if request.method == 'POST':
       
        return HttpResponse(f"Your purchase of {quantity} ticket(s) for {event.title} has been confirmed. Total price: ${total_price}")

    return render(request, 'checkout.html', {
        'event': event,
        'quantity': quantity,
        'total_price': total_price
    })

################################################################

def update_quantity(request,id,action,path):
    print("helloooo",path)
    cart_item = Event.objects.get(id=id)
    if action == "plus":
      cart_item.quantity += 1
      cart_item.total_price = cart_item.ticket_price * cart_item.quantity
    elif action == "minus" and cart_item.quantity  > 0 :
        cart_item.quantity -= 1
        cart_item.total_price = cart_item.ticket_price * cart_item.quantity
    cart_item.save()
    users_id=request.session.get('id')
    user= Users.objects.get(id=users_id)
    if (path == 'tech'):
        return redirect('/tech/') 
    elif (path == 'sports'):
       return redirect('/sports/') 
    elif (path == 'food'):
       return redirect('/food/') 
    elif (path == 'music'):
       return redirect('/music/') 
    elif (path == 'fashion'):
       return redirect('/fashion/') 
    elif (path == 'workshop'):
       return redirect('/workshop/') 
    return render(request,'events.html')


################################################################



def payment(request,amount):
    client=razorpay.Client(auth=('rzp_test_a8OmF04Ppiwsc6','3hH4nbEz5DKkBBzR1iLKZdt4'))
    response_payment=client.order.create(dict(amount=int(amount),currency="INR"))
    print('response_payment',response_payment)
    return redirect('/profile/')

################################################################

def success(request,amount,id,payment_id,session):
    user=Users.objects.get(id=session)
    event=Event.objects.get(id=id)
    quantity=event.quantity
    booking=Bookings.objects.create(user=user,event=event,quantity=quantity,total_price=amount)
    booking.save()
    subs=Payments.objects.create(user=user,amount=amount,event=event,razorpay_payment_id=payment_id)
    subs.save()
    return redirect(f'/payment/{amount}/')

################################################################