from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class CarBrand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Car(models.Model):
    FUEL_CHOICES = [
        ('essence', 'Essence'),
        ('diesel', 'Diesel'),
        ('hybride', 'Hybride'),
        ('electrique', 'Électrique'),
    ]
    
    TRANSMISSION_CHOICES = [
        ('manuelle', 'Manuelle'),
        ('automatique', 'Automatique'),
    ]
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE, related_name='cars')
    year = models.PositiveIntegerField()
    fuel = models.CharField(max_length=20, choices=FUEL_CHOICES)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    seats = models.PositiveIntegerField()
    luggage = models.PositiveIntegerField(help_text="Number of suitcases that can fit")
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    main_image = models.ImageField(upload_to='cars/')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='cars/')
    is_main = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Image for {self.car.name}"

class CarFeature(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='features')
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmée'),
        ('cancelled', 'Annulée'),
        ('completed', 'Terminée'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='reservations')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Reservation #{self.id} - {self.user.username} - {self.car.name}"

class ReservationOption(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='options')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return f"{self.name} for Reservation #{self.reservation.id}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    license_number = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return f"Profile for {self.user.username}"

class Testimonial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='testimonials')
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Testimonial by {self.user.username}"