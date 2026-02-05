from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

###自定義註冊表單，繼承自Django內建的UserCreationForm，並添加額外的欄位
class RegisterForm(UserCreationForm):
    user_name = forms.CharField(
        label="姓名",
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        label="電子郵件",
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    phone = forms.CharField(
        label="電話",
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    birthday = forms.DateField(
        label="生日",
        required=False,
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"})
    )
    address = forms.CharField(
        label="地址",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    identity = forms.CharField(
        label="身份證字號",
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    class Meta:
        model = User
        fields = ("username","user_name","email","identity","password1","password2","birthday","address","phone")

    def clean_username(self):
        #驗證用戶名是否已存在
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('此帳號已存在，請使用其他帳號。')
        return username

    def clean_email(self):
        #驗證電子郵件是否已存在
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('此電子郵件已被註冊，請使用其他電子郵件。')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                user_name=self.cleaned_data.get("user_name"),
                phone=self.cleaned_data.get("phone"),
                birthday=self.cleaned_data.get("birthday"),
                email=self.cleaned_data.get("email"),
                address=self.cleaned_data.get("address"),
                identity=self.cleaned_data.get("identity")
            )
        return user
