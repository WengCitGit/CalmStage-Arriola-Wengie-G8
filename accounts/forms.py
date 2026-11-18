from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class AccountRegistrationForm(UserCreationForm):
    PUBLIC_ROLE_CHOICES = [
        (CustomUser.Role.STUDENT, 'Student'),
        (CustomUser.Role.TEACHER, 'Teacher'),
    ]

    role = forms.ChoiceField(
        choices=PUBLIC_ROLE_CHOICES,
        required=True,
        label="Register As"
    )
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    contact_number = forms.CharField(max_length=20, required=False)
    program_or_department = forms.CharField(
        max_length=100,
        required=False,
        label="Academic Program / Department"
    )

    class Meta:
        model = CustomUser
        fields = [
            'role',
            'username',
            'first_name',
            'last_name',
            'email',
            'contact_number',
            'program_or_department',
            'password1',
            'password2',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email address already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email'].lower()
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user


class UserProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'email',
            'contact_number',
            'program_or_department',
            'profile_photo',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email is already in use by another account.")
        return email