from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from .forms import SignUpForm, LoginForm
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser

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

    context = {'form':form}
    return render(request, 'accounts/signup.html', context)


# Sends an verification email with a link to the new user
def send_email_verification(user):
    subject = "Email Verification for Sustainable Campus"
    link = f"http://127.0.0.1:8000/accounts/email_verification/{user.verification_token}"
    message =f"Hello {user.first_name}, \n\nPlease verify your email through the following link below:\n{link}\n\nThank You!"
    sender = settings.EMAIL_HOST_USER # Sender of email is stored in settings.py
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

    # Verifies user if they are unverified
    if user.verified == False:
        user.verified = True
        user.save()
        messages.success(request, "User has now been verified, you can now log in.")
    else:
        messages.error(request, "User is already verified")

    return redirect('accounts:login')

# Handles data submitted by login page's form
def login_page(request):
    form = LoginForm(request)

    # If a form is submitted, the following happens
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            # Retrieves username and password from submitted form
            username = request.POST.get("username")
            password = request.POST.get("password")

            # Retrieves user data for matching username and password
            user = authenticate(request, username=username, password=password)
            
            # Checks if user data has been retrieved
            if user is not None: 
                # Checks if user is verified
                if user.verified == True:
                    login(request, user)
                    return redirect('main:map')

                else:
                    form.add_error(None, 'Email has not been verified')

            else:
                form.add_error(None, 'Invalid username or password')
            
        else:
            context = {'form':form}
            return render(request, 'accounts/login.html', context)
    else:
        context = {'form':form}
        return render(request, 'accounts/login.html', context)


def logout_view(request):
    logout(request)
    messages.success(request, "Log out successfully")
    return redirect("accounts:login")


