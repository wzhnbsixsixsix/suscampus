from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, update_session_auth_hash
from .forms import SignUpForm, LoginForm, ChangeUsernameForm
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser
from shop.models import UserBalance
from leaderboards.models import TreeScore


# Handles data submitted from signup page's form
def signup_page(request):
    form = SignUpForm()

    # If a form is submitted, the following happens
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Checks if given email is unique before saving new user data
            if CustomUser.objects.filter(email=form.cleaned_data["email"]).exists():
                form.add_error("email", "Email is already in use.")
            # Saves new user data, and sends email verification
            else:
                user = form.save()
                send_email_verification(user)
                return redirect('accounts:login')

    context = {'form': form}
    return render(request, 'accounts/signup.html', context)


# Sends an verification email with a link to the new user
def send_email_verification(user):
    subject = "Email Verification for Sustainable Campus"
    link = f"http://127.0.0.1:8000/accounts/email_verification/{user.verification_token}"
    message = f"Hello {user.first_name}, \n\nPlease verify your email through the following link below:\n{link}\n\nThank You!"
    sender = settings.EMAIL_HOST_USER  # Sender of email is stored in settings.py
    receiver = [user.email]

    send_mail(subject, message, sender, receiver)


# Determines what happens when the verification link is clicked
def email_verification(request, token):
    # Retrieves user data using given verification token, returns error if invalid
    try:
        user = CustomUser.objects.get(verification_token=token)
    except CustomUser.DoesNotExist:
        messages.error(request, "Invalid or expired verification token")
        return redirect('accounts:signup')

    # Verifies user if they are unverified, and creates user balance for account
    if user.verified == False:
        user.verified = True
        user.save()

        # Creates a user balance for player
        UserBalance.objects.create(user_id=user)

        # Creates a score counter for the tree game for player
        TreeScore.objects.create(user_id=user)

        messages.success(request, "User has now been verified, you can now log in.")
    else:
        messages.error(request, "User is already verified")

    return redirect('accounts:login')


# Handles data submitted by login page's form
def login_page(request):
    form = LoginForm(request)

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.verified:
                    login(request, user)
                    return redirect('main:map')
                else:
                    form.add_error(None, 'Invalid username or password')
            else:
                form.add_error(None, 'Invalid username or password')
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, "Log out successfully")
    return redirect("accounts:login")



@login_required
def profile_page(request):
    context = {
        'username': request.user.username,
        'email': request.user.email,
        'form': PasswordChangeForm(request.user)  
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def change_username(request):
    """
    This function processes POST requests when the user submits a new username through the form. If the request method is POST and the form data is valid,
    it updates the user's username and redirects to the profile page. If the data is invalid, it reloads the profile page with the current form errors.
    If the request method is not POST, it loads the username change form with the current user information.
    """
    if request.method == 'POST':
        # Create a form instance with the submitted data and the current user instance
        form = ChangeUsernameForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Username modification was successful!")
            return redirect('accounts:profile')
        else:
            return render(request, 'accounts/profile.html', {
                'form': form,  # Form containing error message
                'show_modal': True
            })
    else:
        # If not a POST request, create a blank form instance with the current user information
        form = ChangeUsernameForm(instance=request.user)

    # Render the profile page with the username change form
    return render(request, 'accounts/profile.html', {
        'form': form,
        'show_modal': False
    })


@login_required
def change_password(request):
    """
    Handles password change requests for authenticated users. Uses Django's form validation
    to ensure new password meets security requirements. Maintains user session after password
    change by updating auth hash.
    """
    base_context = {
        'username': request.user.username,
        'email': request.user.email,
        'form': PasswordChangeForm(request.user)
    }

    if request.method == 'POST':
        # Initialize password change form with user and POST data
        form = PasswordChangeForm(request.user, request.POST)
        # Validate form data
        if form.is_valid():
            # Save new password
            user = form.save()
            # Maintain session continuity after password change
            update_session_auth_hash(request, user)
            # Set success notification
            messages.success(request, 'Your password has been updated successfully!')
            # Redirect to profile page
            return redirect('accounts:profile')
        else:
            base_context.update({
                'form': form,
                'username': request.user.username,  # 显式保留用户名
                'email': request.user.email  # 显式保留邮箱
            })
            # Set error notification for invalid form
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'accounts/profile.html', base_context)

    else:
        # Initialize empty form for GET requests
        form = PasswordChangeForm(request.user)
    # Render password change template with form context
    return render(request, 'accounts/profile.html', base_context)

def password_reset(request):
    form = SignUpForm()

    # If a form is submitted, the following happens
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Checks if given email is unique before saving new user data
            if CustomUser.objects.filter(email=form.cleaned_data["email"]).exists():
                form.add_error("email", "Email is already in use.")
            # Saves new user data, and sends email verification
            else:
                user = form.save()
                send_email_verification(user)
                return redirect('accounts:login')

    context = {'form': form}
    return render(request, 'accounts/signup.html', context)