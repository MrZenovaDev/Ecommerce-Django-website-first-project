from .models import UserProfile
from django import forms

class ProfileOfUser(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['adress']