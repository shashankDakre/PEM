from django.db import models

class Users(models.Model):
    fullName=models.CharField(max_length=100)
    Email=models.EmailField(unique=True)
    phoneNumber=models.BigIntegerField(unique=True)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    password=models.CharField(max_length=100)

class Host_register(models.Model):
    name= models.CharField(max_length=100)
    mobile = models.BigIntegerField(unique=True)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


    

class Profile_pic(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile/', null=True, blank=True)
    def __str__(self):
        return f"Profile picture for {self.user.username}"


class Event(models.Model):
    host=models.ForeignKey(Host_register,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    event_date = models.DateField()
    description = models.TextField()
    location = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    category = models.CharField(max_length=255)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
    quantity=models.IntegerField(default=1)
    total_price=models.IntegerField(default=0)
   

    def __str__(self):
        return self.title
    
class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Bookings(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    booking_date = models.DateField(auto_now_add=True)
    quantity=models.IntegerField(default=1)
    total_price=models.IntegerField(default=0)


class Payments(models.Model):
    user=models.ForeignKey(Users,on_delete=models.CASCADE)
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    amount=models.FloatField()
    payment_id=models.CharField()
    razorpay_payment_id=models.CharField()




