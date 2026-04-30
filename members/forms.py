from django import forms
from .models import Member

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'is_active']
        
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name...'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name...'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address...'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Contact Number...'}),
            'address': forms.Textarea(attrs={'placeholder': 'Dwelling Place...', 'rows': 3}),
        }