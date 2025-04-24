import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
import uuid
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from accounts.forms import SignUpForm, CustomPasswordResetForm, EnableTwoFactorAuthForm
from accounts.models import CustomUser
from django.urls import reverse

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
    return render(request, 'accounts/logout.html')

logger = logging.getLogger(__name__)

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

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

def reset_password_view(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.get(username=form.cleaned_data['username'])
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            return redirect('login')
    else:
        form = CustomPasswordResetForm()
    return render(request, 'accounts/reset.html', {'form': form})


#logger = logging.getLogger(__name__)

def verify_2fa_login(request):
    user_id = request.session.get('user_id_for_2fa')
    logger.info(f"verify_2fa_login: Retrieved user ID {user_id} from session.") # Added log
    if not user_id:
        logger.warning("verify_2fa_login: user_id not found in session. Redirecting to login.") # Added log
        return redirect('login')

    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        logger.error(f"verify_2fa_login: User with ID {user_id} not found. Redirecting to login.") # Added log
        return redirect('login')

    if request.method == 'POST':
        verification_code = request.POST.get('verification_code')

        if user.two_factor_secret and user.two_factor_expiry and timezone.now() < user.two_factor_expiry:
            if verification_code == user.two_factor_secret:
                login(request, user)
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
    user = request.user
    form = EnableTwoFactorAuthForm(initial={'enable_2fa': user.is_2fa_enabled})

    if request.method == 'POST':
        form = EnableTwoFactorAuthForm(request.POST)
        if form.is_valid():
            enable_2fa = form.cleaned_data['enable_2fa']
            logger.info(f"User {user.username} submitted profile settings. Enable 2FA: {enable_2fa}")

            if enable_2fa and not user.is_2fa_enabled:
                user.is_2fa_enabled = True

                # Clear old 2FA info
                user.two_factor_secret = None
                user.two_factor_expiry = None

                # Generate new code
                secret_code = str(uuid.uuid4().hex[:6]).upper()
                user.two_factor_secret = secret_code
                user.two_factor_expiry = timezone.now() + timezone.timedelta(minutes=10)
                user.save()

                logger.info(f"User {user.username}: Generated code {secret_code}, expiry {user.two_factor_expiry}")

                messages.success(request,
                                 'Two-Factor Authentication has been enabled. You will be asked to verify your login next time you sign in.')
                return redirect('profile_settings')


            elif not enable_2fa and user.is_2fa_enabled:
                logger.info(f"User {user.username} is disabling 2FA.")
                user.is_2fa_enabled = False
                user.two_factor_secret = None
                user.two_factor_expiry = None
                user.save()
                messages.success(request, 'Two-Factor Authentication has been disabled.')
                return redirect('profile_settings')

    context = {'form': form}
    return render(request, 'accounts/profile_settings.html', context)
