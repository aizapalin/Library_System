from django import forms
from django.utils import timezone  # YOU NEED THIS IMPORT
from .models import BorrowRecord
from book_management.models import Book

class BorrowForm(forms.ModelForm):
    class Meta:
        model = BorrowRecord
        fields = ['book', 'member', 'due_date', 'status']
        widgets = {
            'book': forms.Select(attrs={'class': 'form-control'}),
            'member': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={
                'type': 'date',
                # This prevents selecting any day before today in the browser
                'min': timezone.now().date().isoformat()
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Keeps your fix for the FieldError
        self.fields['book'].queryset = Book.objects.all()

    # Optional: Backend validation to ensure data is clean even if 
    # someone manually types a date into the inspector
    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date < timezone.now().date():
            raise forms.ValidationError("You cannot cast a spell into the past! Please pick a future date.")
        return due_date