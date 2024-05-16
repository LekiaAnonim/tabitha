from django import forms
from django.utils.translation import gettext_lazy as _

from wagtail.users.forms import UserEditForm, UserCreationForm

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
)
from authentication.models import User


class UserSignInForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}), label='Email')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password..'}), label='Password')

    class Meta:
        model = User
        fields = ['email', 'password']
class UserRegisterForm(UserCreationForm):
    """
        Creates User registration form for signing up.
    """
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        # self.fields['username'].widget.attrs.pop("autofocus", None)

    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={
        "name": "email", "class": "input100",
        "placeholder": "Email"
    }
    ),
        help_text='Required. Input a valid email address.'
    )
    password1 = forms.CharField(label="Password",
    widget=forms.PasswordInput(attrs={
        "name": "password", "class": "input100",
        "placeholder": "Password"
    }
    ),
    )

    password2 = forms.CharField(label="Confirm Password",
                                help_text=_(
                                    "Enter the same password as before, for verification."),
    widget=forms.PasswordInput(attrs={"name": "Confirm Password", "class": "input100", "placeholder": "Confirm Password"}),
    )

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
        # widgets = {

        #     "username": forms.TextInput(attrs={
        #         "name": "username", "class": "input100",
        #         "placeholder": "Username"
        #     }),
        # }

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class CustomUserEditForm(UserEditForm):
    email = forms.CharField(required=False, label=_("Email"))
    country = forms.CharField(required=False, label=_("Country"))
    region = forms.CharField(required=False, label=_("State"))
    city = forms.CharField(required=False, label=_("City"))
    phone_number = forms.CharField(required=False, label=_("Phone number"))
    residential_address = forms.CharField(required=False, label=_("Residential address"))
    avatar = forms.ImageField(required=False, label=_("Avatar"))


class CustomUserCreationForm(UserCreationForm):
    email = forms.CharField(required=False, label=_("Email"))
    country = forms.CharField(required=False, label=_("Country"))
    region = forms.CharField(required=False, label=_("State"))
    city = forms.CharField(required=False, label=_("City"))
    phone_number = forms.CharField(required=False, label=_("Phone number"))
    residential_address = forms.CharField(required=False, label=_("Residential address"))
    avatar = forms.ImageField(required=False, label=_("Avatar"))