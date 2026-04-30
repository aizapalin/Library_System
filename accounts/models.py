from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver # Add this
from allauth.account.signals import user_signed_up # Add this
import random

class CustomUser(AbstractUser):
    ROLE_CHOICES = (('guest', 'Guest'), ('librarian', 'Librarian'))
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='guest')
    is_librarian = models.BooleanField(default=False)
    is_head_librarian = models.BooleanField(default=False)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)
    library_id = models.CharField(max_length=12, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.library_id:
            while True:
                candidate = f"{random.randint(10000000, 99999999)}"
                if not type(self).objects.filter(library_id=candidate).exists():
                    self.library_id = candidate
                    break
        super().save(*args, **kwargs)

# --- SIGNAL TO AUTO-PROMOTE TO SUPERUSER ---
@receiver(user_signed_up)
def set_superuser_on_signup(request, user, **kwargs):
    # New signups are guests by default unless promoted by admin.
    user.role = 'guest'
    user.save()