from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Reservation, UserProfile, Testimonial

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
        
        return user

class ReservationForm(forms.ModelForm):
    OPTIONS_CHOICES = [
        ('insurance', 'Assurance tous risques (15€/jour)'),
        ('gps', 'GPS (5€/jour)'),
        ('child_seat', 'Siège enfant (8€/jour)'),
        ('additional_driver', 'Conducteur additionnel (10€/jour)'),
    ]
    
    options = forms.MultipleChoiceField(
        choices=OPTIONS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = Reservation
        fields = ('start_date', 'end_date')
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date:
            if start_date >= end_date:
                raise forms.ValidationError("La date de fin doit être postérieure à la date de début.")
        
        return cleaned_data

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'city', 'postal_code', 'license_number')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Pre-fill user fields if profile exists
        if self.instance and self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ('rating', 'comment')
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
