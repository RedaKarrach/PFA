from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import datetime
from decimal import Decimal
from .models import Car,CarBrand,Reservation, Testimonial, UserProfile
from .forms import ReservationForm, UserProfileForm, TestimonialForm, SignUpForm
from django.contrib.auth import logout
from django.views.decorators.http import require_GET


def home(request):
    # Get featured cars (you can customize this query)
    featured_cars = Car.objects.filter(is_available=True).order_by('?')[:4]
    
    # Get approved testimonials
    testimonials = Testimonial.objects.filter(is_approved=True).order_by('-created_at')[:2]
    
    context = {
        'featured_cars': featured_cars,
        'testimonials': testimonials,
    }
    
    return render(request, 'rental/index.html', context)

def profile_dashboard(request):
    reservations = Reservation.objects.filter(user=request.user)  # ou request.user.id selon ton modèle
    return render(request, 'rental/profile_dashboard.html', {'reservations': reservations})

def catalog(request):
    # Get all available cars
    cars = Car.objects.filter(is_available=True)
    
    # Get filter parameters
    brands = request.GET.getlist('brand')
    fuels = request.GET.getlist('fuel')
    max_price = request.GET.get('max_price')
    sort = request.GET.get('sort', 'price-asc')
    
    # Apply filters
    
    if brands:
        cars = cars.filter(brand__slug__in=brands)
    
    if fuels:
        cars = cars.filter(fuel__in=fuels)
    
    if max_price:
        cars = cars.filter(price_per_day__lte=max_price)
    
    # Apply sorting
    if sort == 'price-asc':
        cars = cars.order_by('price_per_day')
    elif sort == 'price-desc':
        cars = cars.order_by('-price_per_day')
    elif sort == 'name-asc':
        cars = cars.order_by('name')
    elif sort == 'name-desc':
        cars = cars.order_by('-name')
    
    # Pagination
    paginator = Paginator(cars, 6)  # 6 cars per page
    page_number = request.GET.get('page', 1)
    cars_page = paginator.get_page(page_number)
    
    # Get all brands for the filter form
    all_brands = CarBrand.objects.all()
    
    context = {
        'cars': cars_page,
        'all_brands': all_brands,
        'selected_brands': brands,
        'selected_fuels': fuels,
        'max_price': max_price,
        'sort': sort,
    }
    
    return render(request, 'rental/catalog.html', context)

def car_details(request, slug):
    car = get_object_or_404(Car, slug=slug)
    
    
    context = {
        'car': car,
    }
    
    return render(request, 'rental/car_details.html', context)

@login_required
def reservation(request, car_slug):
    car = get_object_or_404(Car, slug=car_slug)
    
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            # Create reservation but don't save yet
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.car = car
            
            # Calculate total price
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            days = (end_date - start_date).days
            
            # Base price
            total_price = car.price_per_day * days
            
            # Add options price
            options = request.POST.getlist('options')
            option_prices = {
                'insurance': Decimal('15.00'),
                'gps': Decimal('5.00'),
                'child_seat': Decimal('8.00'),
                'additional_driver': Decimal('10.00'),
            }
            
            for option in options:
                if option in option_prices:
                    total_price += option_prices[option] * days
            
            reservation.total_price = total_price
            reservation.save()
            
            # Save options
            for option in options:
                if option in option_prices:
                    reservation.options.create(
                        name=option.replace('_', ' ').title(),
                        price=option_prices[option] * days
                    )
            
            messages.success(request, 'Votre réservation a été confirmée avec succès!')
            return redirect('reservation_confirmation', reservation_id=reservation.id)
    else:
        # Pre-fill form with data from GET parameters
        initial_data = {}
        if 'start_date' in request.GET and 'end_date' in request.GET:
            initial_data['start_date'] = request.GET.get('start_date')
            initial_data['end_date'] = request.GET.get('end_date')
        
        form = ReservationForm(initial=initial_data)

    context = {
        'car': car,
        'form': form,
    }
    
    return render(request, 'rental/reservation.html', context)

@login_required
def reservation_confirmation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    
    context = {
        'reservation': reservation,
    }
    
    return render(request, 'rental/reservation_confirmation.html', context)


@login_required
def profile(request):
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            
            # Update user model fields
            user = request.user
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.save()
            
            messages.success(request, 'Votre profil a été mis à jour avec succès!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    context = {
        'form': form,
    }
    
    return render(request, 'rental/profile.html', context)

@login_required
def add_testimonial(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.user = request.user
            testimonial.save()
            
            messages.success(request, 'Merci pour votre témoignage! Il sera publié après validation.')
            return redirect('home')
    else:
        form = TestimonialForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'rental/add_testimonial.html', context)


class CustomLoginView(LoginView):
    template_name = 'rental/login.html'

def user_logout(request):
    logout(request)  # this clears the session and logs out the user
    return redirect('home')  # redirect to home page or wherever you want

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():  # Checks if the form data is valid
            user = form.save()  # Saves the user to the database
            login(request, user)  # Logs the user in automatically
            return redirect('home')  # Redirect to home or another view
    else:
        form = UserCreationForm()  # Empty form for GET request
    
    return render(request, 'register.html', {'form': form})



def check_availability(request):
    if request.method == 'GET':
        car_id = request.GET.get('car_id')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        if not all([car_id, start_date, end_date]):
            return JsonResponse({'available': False, 'message': 'Missing parameters'})
        
        try:
            car = Car.objects.get(id=car_id)
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            # Check if car is available for the selected dates
            conflicting_reservations = Reservation.objects.filter(
                car=car,
                status__in=['pending', 'confirmed'],
            ).filter(
                Q(start_date__lte=end_date, end_date__gte=start_date)
            )
            
            if conflicting_reservations.exists():
                return JsonResponse({'available': False, 'message': 'Car is not available for the selected dates'})
            
            return JsonResponse({'available': True, 'message': 'Car is available'})
        
        except Car.DoesNotExist:
            return JsonResponse({'available': False, 'message': 'Car not found'})
        except Exception as e:
            return JsonResponse({'available': False, 'message': str(e)})
    
    return JsonResponse({'available': False, 'message': 'Invalid request'})


#added 17/04/25
def about(request):
    return render(request, 'rental/about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Logique pour traiter le message (exemple : envoyer un email)
        messages.success(request, 'Votre message a été envoyé avec succès !')
        return render(request, 'rental/contact.html')

    return render(request, 'rental/contact.html')