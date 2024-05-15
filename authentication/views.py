from django.shortcuts import render
from django.contrib.auth.forms import (
    AuthenticationForm,
)
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.views import (PasswordResetDoneView, PasswordResetConfirmView,
                                        PasswordResetCompleteView, PasswordChangeView,
                                       PasswordChangeDoneView, PasswordResetView)
from .models import User as Member
from django.http.response import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from .forms import UserRegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class SignUpSuccessful(TemplateView):
    template_name = 'authentication/thanks.html'
class UserDetail(LoginRequiredMixin, DetailView):
    model = Member
    template_name = 'courses/profile_detail.html'
    login_url = "authentication:login"
    redirect_field_name = "redirect_to"

class UserUpdateView(LoginRequiredMixin, UpdateView):
    fields = ['username', 'first_name', 'last_name', 'email', 'country', 'region', 'city', 'phone_number', 'residential_address', 'avatar']
    model = Member
    template_name = 'authentication/user_update.html'
    login_url = "authentication:login"
    redirect_field_name = "redirect_to"
class UserLoginView(View):
    """
     Logs author into dashboard.
    """
    template_name = 'authentication/login.html'
    context_object = {"login_form": AuthenticationForm}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context_object)

    def post(self, request, *args, **kwargs):

        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            
            login(request, user)
            messages.success(request, f"Login Successful ! "
                                f"Welcome {user.username}.")
            
            return redirect('shop:home')

        else:
            messages.error(request,
                           f"Please enter a correct username and password. Note that both fields may be case-sensitive."
                           )
            return render(request, self.template_name, self.context_object)

class UserRegisterView(View):
    """
      View to let users register
    """
    template_name = 'authentication/register.html'
    context = {
        "register_form": UserRegisterForm()
    }

    def get(self, request):
        success_message = "Successful"

        self.context['success_message'] = success_message
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):

        register_form = UserRegisterForm(request.POST)

        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.is_active = True
            user.is_staff = True
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('authentication/activate_email.html'
                                       , {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'protocol': 'https',
            }
            )
            from_email = 'tabitha.market@gmail.com'
            to_email = register_form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, from_email, to=[to_email]
            )
            email.send()

            return HttpResponseRedirect(reverse_lazy('authentication:email_verification_confirm'))

        else:
            messages.error(request, "Please provide valid information.")
            # Redirect user to register page
            return render(request, self.template_name, self.context)

    # def get_success_url(self):
    #     return reverse('authentication:signup_successful')


class PasswordResetView(PasswordResetView):
    template_name = 'authentication/pwd_reset_form.html'
    email_template_name = "authentication/email_text/password_reset_email.html"
    from_email = ''
    subject_template_name = "authentication/email_text/password_reset_subject.txt"
    success_url = reverse_lazy("authentication:password_reset_done")

class PasswordResetDoneView(PasswordResetDoneView):
    template_name = 'authentication/email_text/password_reset_done.html' 

class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'authentication/email_text/password_reset_confirm.html'
    success_url = reverse_lazy("authentication:password_reset_complete")

class PasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'authentication/email_text/password_reset_complete.html'

class PasswordChangeView(PasswordChangeView):
    template_name = 'authentication/email_text/password_change_form.html'
    success_url = reverse_lazy("authentication:password_change_done")

class PasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'authentication/email_text/password_change_done.html'

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(
            request, f'Hi {user.username}, your registration was successful!! .')
        return reverse('authentication:login')
    else:
        return reverse_lazy('authentication:email_verification_invalid')


class EmailVerificationConfirm(TemplateView):
    template_name = 'authentication/email_verification_confirm.html'


class EmailVerificationInvalid(TemplateView):
    template_name = 'authentication/email_verification_invalid.html'