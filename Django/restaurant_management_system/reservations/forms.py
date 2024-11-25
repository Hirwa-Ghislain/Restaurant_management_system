from django import forms
from .models import CustomerReservation

class CustomerReservationForm(forms.ModelForm):
    class Meta:
        model = CustomerReservation
        fields = ['date', 'time', 'number_of_guests', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'number_of_guests': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Special requests or additional details...'}),
        }
