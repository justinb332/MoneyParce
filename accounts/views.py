import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django import forms

from accounts.forms import SignUpForm, CustomPasswordResetForm, EnableTwoFactorAuthForm
from accounts.models import CustomUser

import uuid

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    logout(request)
    # return render(request, 'accounts/logout.html')
    return render(request, 'home/home.html')

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def __init__(self):
        super(CustomLoginView, self).__init__()

        # for field in self.fields:
        #     self.fields[field].widget.attrs.update({'class': 'form-control'})

    def form_valid(self, form):
        user = form.get_user()
        if user.is_2fa_enabled:
            # Clear old 2FA info
            user.two_factor_secret = None
            user.two_factor_expiry = None

            # Generate new code
            secret_code = str(uuid.uuid4().hex[:6]).upper()
            user.two_factor_secret = secret_code
            user.two_factor_expiry = timezone.now() + timezone.timedelta(minutes=10)
            user.save()

            subject = 'Your One-Time Verification Code'
            message = f'Your verification code is: {secret_code}. This code will expire in 10 minutes.'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)

            self.request.session['user_id_for_2fa'] = user.id
            logger.info(f"User {user.username}: Stored user ID {user.id} in session for 2FA.")
            return redirect('verify_2fa_login')
        else:
            login(self.request, user)
            return super().form_valid(form)

    def get_success_url(self):
        return self.request.GET.get('next', reverse('home'))

from django.core.exceptions import ValidationError

def reset_password_view(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            try:
                user = CustomUser.objects.get(username=form.cleaned_data['username'])
            except CustomUser.DoesNotExist:
                form.add_error(None, 'Invalid username.')
                return render(request, 'accounts/reset.html', {'form': form})

            provided_answer = form.cleaned_data['security_answer'].strip().lower()
            correct_answer = user.security_answer.strip().lower()

            if provided_answer == correct_answer:
                user.set_password(form.cleaned_data['new_password1'])
                user.save()
                messages.success(request, 'Password reset successful. You can now log in.')
                return redirect('login')
            else:
                form.add_error('security_answer', 'Security answer does not match.')
    else:
        form = CustomPasswordResetForm()

    return render(request, 'accounts/reset.html', {'form': form})

#logger = logging.getLogger(__name__)

def verify_2fa_login(request):
    user_id = request.session.get('user_id_for_2fa')
    logger.info(f"verify_2fa_login: Retrieved user ID {user_id} from session.")
    if not user_id:
        logger.warning("verify_2fa_login: user_id not found in session. Redirecting to login.")
        return redirect('login')

    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        logger.error(f"verify_2fa_login: User with ID {user_id} not found. Redirecting to login.")
        return redirect('login')

    if request.method == 'POST':
        verification_code = request.POST.get('verification_code')

        if user.two_factor_secret and user.two_factor_expiry and timezone.now() < user.two_factor_expiry:
            if verification_code == user.two_factor_secret:
                CustomUserModel = get_user_model()
                fresh_user = CustomUserModel.objects.get(pk=user.pk)

                login(request, fresh_user)
                del request.session['user_id_for_2fa']
                return redirect('home')
            else:
                messages.error(request, 'Invalid verification code. Please try again.')
        else:
            messages.error(request, 'The verification code has expired or is invalid. Please log in again.')
            return redirect('login')

    return render(request, 'accounts/verify_2fa_login.html')

@login_required
def profile_settings(request):
    user = CustomUser.objects.get(pk=request.user.pk)

    if request.method == 'POST':
        enable_2fa = request.POST.get('enable_2fa') == 'on'
        logger.info(f"[POST] Checkbox value: {enable_2fa}")

        from django.core.mail import send_mail
        from django.conf import settings

        if enable_2fa and not user.is_2fa_enabled:
            user.is_2fa_enabled = True
            user.two_factor_secret = None
            user.two_factor_expiry = None

            # Generate code
            secret_code = str(uuid.uuid4().hex[:6]).upper()
            user.two_factor_secret = secret_code
            user.two_factor_expiry = timezone.now() + timezone.timedelta(minutes=10)
            user.save()

            # Send email
            send_mail(
                subject='Your One-Time Verification Code',
                message=f'Your verification code is: {secret_code}. It will expire in 10 minutes.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False
            )

            logout(request)
            request.session['user_id_for_2fa'] = user.id
            messages.info(request, '2FA enabled. Check your email for a verification code.')
            return redirect('verify_2fa_login')


        elif not enable_2fa and user.is_2fa_enabled:
            user.is_2fa_enabled = False
            user.two_factor_secret = None
            user.two_factor_expiry = None
            user.save()
            messages.success(request, '2FA disabled.')
            return redirect('profile_settings')

    return render(request, 'home/settings.html')