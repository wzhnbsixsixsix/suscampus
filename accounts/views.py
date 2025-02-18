from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from .forms import SignUpForm, LoginForm
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser

# Create your views here.
def signup_page(request):
    form = SignUpForm()

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_email_verification(user)
            return redirect('login')

    context = {'form':form}
    return render(request, 'accounts/signup.html', context)



def send_email_verification(user):
    subject = "Email Verification for Sustainable Campus"
    link = f"http://127.0.0.1:8000/accounts/email_verification/{user.verification_token}"
    message =f"Hello {user.first_name}, \n\nPlease verify your email through the following link below:\n{link}\n\nThank You!"
    sender=settings.EMAIL_HOST_USER
    receiver = [user.email]

    send_mail(subject, message, sender, receiver)



def email_verification(request, token):
    user = CustomUser.objects.get(verification_token=token)

    if user.verified == False:
        user.verified = True
        user.save()
        messages.success(request, "The email you provided has now been verified, you can now log in.")
        return redirect('login')
    else:
        messages.error(request, "The verification link you used is invalid or has expired")
        return redirect('signup')



def login_page(request):
    form = LoginForm(request)

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)
            
            if user is not None: 
                if user.verified == True:
                    login(request, user)
                    return redirect('home')

                else:
                    form.add_error(None, 'Email has not been verified')

            else:
                print("checkpoint 3")
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
    return redirect("login")



