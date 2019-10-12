from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from charity.password_validators import validators


class RegisterForm(ModelForm):
    password_repeated = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': "Powtórz hasło"}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_repeated = cleaned_data.get("password_repeated")

        if password != password_repeated:
            raise forms.ValidationError(
                "Hasła nie pasują!"
            )

        validators(password)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "password_repeated"]
        widgets = {
            "password": forms.PasswordInput(attrs={'placeholder': 'Hasło'}),
            "email": forms.EmailInput(attrs={'placeholder': 'E-mail'}),
            "last_name": forms.TextInput(attrs={'placeholder': 'Nazwisko'}),
            "first_name": forms.TextInput(attrs={'placeholder': 'Imię'}),
        }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields["password"].label = False
        self.fields["password_repeated"].label = False
        self.fields["first_name"].label = False
        self.fields["last_name"].label = False
        self.fields["email"].label = False


class LoginForm(forms.Form):
    login = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'E-mail'}))
    password = forms.CharField(label="",
                               widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))


class EditProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password"]
        widgets = {
            "password": forms.PasswordInput(attrs={'placeholder': 'Hasło'})
        }

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields["password"].label = "Aby potwierdzić podaj hasło"
        self.fields["first_name"].label = "Zmień imię:"
        self.fields["last_name"].label = "Zmień nazwisko:"
        self.fields["email"].label = "Zmień email:"


class EditPasswordForm(forms.Form):
    old_password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'Stare hasło'}))
    new_password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'Nowe hasło'}))
    new_password_repeated = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz nowe hasło'}))

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        new_password_repeated = cleaned_data.get("new_password_repeated")

        if new_password != new_password_repeated:
            raise forms.ValidationError(
                "Hasła nie pasują!"
            )


class RemindPasswordForm(forms.Form):
    email = forms.EmailField(label="Podaj adres email konta:", widget=forms.EmailInput(attrs={'placeholder': 'Email'}))


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'placeholder': 'Nowe hasło'}))
    new_password_repeated = forms.CharField(label="",
                                            widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz nowe hasło'}))

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        new_password_repeated = cleaned_data.get("new_password_repeated")

        if new_password != new_password_repeated:
            raise forms.ValidationError(
                "Hasła nie pasują!"
            )
