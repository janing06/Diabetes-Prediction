from django import forms
from .models import Patient, Diagnosis

class PatientFrom(forms.ModelForm):
     class Meta:
          model = Patient
          fields = ['first_name','middle_name','last_name','sex','address','barangay']
          widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Middle Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'sex': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'barangay': forms.Select(attrs={'class': 'form-select'}),
            'created_at': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'updated_at': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }

