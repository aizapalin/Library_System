from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


# This form creates new users who should always become librarians.
class LibrarianRegisterForm(UserCreationForm):
    # This field collects the librarian email during account creation.
    email = forms.EmailField(required=True)

    # This section defines which model and fields this form should use.
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "email", "password1", "password2")

    # This save method auto-assigns librarian role flags before saving.
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get("email", "")
        # This sets librarian flags so users from this form are not regular guests.
        if hasattr(user, "is_librarian"):
            user.is_librarian = True
        if hasattr(user, "role"):
            user.role = "librarian"
        if commit:
            user.save()
        return user

