from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fn = models.CharField(max_length=100, verbose_name="First Name")
    ln = models.CharField(max_length=100, verbose_name="Last Name")
    mobno = models.CharField(max_length=90)
    DIST_CHOICES = [
    ("Akola", "Akola"),
    ("Amravati", "Amravati"),
    ("Aurangabad", "Aurangabad"),
    ("Bhandara", "Bhandara"),
    ("Buldhana", "Buldhana"),
    ("Chandrapur", "Chandrapur"),
    ("Dhule", "Dhule"),
    ("Gadchiroli", "Gadchiroli"),
    ("Gondia", "Gondia"),
    ("Hingoli", "Hingoli"),
    ("Jalna", "Jalna"),
    ("Nagpur", "Nagpur"),
    ("Nanded", "Nanded"),
    ("Nashik", "Nashik"),
    ("Osmanabad", "Osmanabad"),
    ("Pune", "Pune"),
    ("Parbhani", "Parbhani"),
    ("Ratnagiri", "Ratnagiri"),
    ("Sangli", "Sangli"),
    ("Satara", "Satara"),
    ("Sindhudurg", "Sindhudurg"),
    ("Solapur", "Solapur"),
    ("Thane", "Thane"),
    ("Wardha", "Wardha"),
    ("Washim", "Washim"),]
    
    city = models.CharField(max_length=100, choices=DIST_CHOICES)
    pincode = models.CharField(max_length=6)

class Index(models.Model):
    CAT={(1,'Acer'),(2,'Asus'),(3,'Dell'),(4,'HP'),(5,'Lenovo')}
    bname = models.CharField(max_length=50, verbose_name="Brand Name")
    mname = models.CharField(max_length=100, verbose_name="Model Name")
    price = models.IntegerField(verbose_name="Original Price")
    oprice = models.IntegerField(verbose_name="Offer Price")
    offer = models.FloatField(verbose_name="Offer Discount")
    cat = models.IntegerField(verbose_name="Category", choices=CAT)
    ss = models.FloatField(verbose_name="Screen Size")
    hds = models.CharField(max_length=30,verbose_name="Hard Disk Size")
    rms = models.IntegerField(verbose_name="RAM Memory Installed Size")
    os = models.CharField(max_length=100, verbose_name="Operating System")
    is_active = models.BooleanField(default=True)
    pimage=models.ImageField(upload_to="image")

    def __str__(self):
        return self.bname

class Cart(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    pid = models.ForeignKey(Index, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)

class Order(models.Model):
    orderid = models.CharField(max_length=50)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    pid = models.ForeignKey(Index, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    amt = models.FloatField(default=0)
    date = models.DateField(default=timezone.now)

class Orderhistory(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    orderid = models.ForeignKey(Order, on_delete=models.CASCADE)
    pid = models.ForeignKey(Index, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    amt = models.FloatField(default=0)
    date = models.DateField(default=timezone.now)
