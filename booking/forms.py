# forms.py
from django import forms
from .models import Hostel

class HostelForm(forms.ModelForm):
    class Meta:
        model = Hostel
        fields = ['name', 'description', 'price', 'available_rooms']
