from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="電子郵件", widget=forms.EmailInput(attrs={"class": "form-control"}))
    phone = forms.CharField(label="電話", max_length=15, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    birthday = forms.DateField(label="生日", required=False, widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}))

    class Meta:
        model = User
        fields = ("username", "email", "phone", "birthday", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            UserProfile.objects.create(
                user=user,
                phone=self.cleaned_data.get("phone"),
                birthday=self.cleaned_data.get("birthday")
            )
        return user
