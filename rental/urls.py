from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CustomLoginView
from . import views
from .views import CreateCheckoutSessionView
from django.views.generic import TemplateView

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('car/<slug:slug>/', views.car_details, name='car_details'),
    path('reservation/<slug:car_slug>/', views.reservation, name='reservation'),
    path('reservation-confirmation/<int:reservation_id>/', views.reservation_confirmation, name='reservation_confirmation'),
    
    # User account
    path('profile/', views.profile, name='profile'),
    path('testimonial/add/', views.add_testimonial, name='add_testimonial'),
    path('mon-compte/', views.profile_dashboard, name='profile_dashboard'),
    
    # Authentication
    #path('login/', auth_views.LoginView.as_view(template_name='rental/login.html'), name='login'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', auth_views.LoginView.as_view(template_name='rental/register.html'), name='register'),
    
    # Password reset
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='rental/password_reset.html'), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='rental/password_reset_done.html'), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='rental/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='rental/password_reset_complete.html'), 
         name='password_reset_complete'),
    
    # API endpoints
    path('api/check-availability/', views.check_availability, name='check_availability'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('success/', TemplateView.as_view(template_name='rental/success.html'), name='success'),
    path('cancel/', TemplateView.as_view(template_name='rental/cancel.html'), name='cancel'),

]