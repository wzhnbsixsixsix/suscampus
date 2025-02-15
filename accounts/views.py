from django.shortcuts import redirect, render
from django.contrib.auth import login
from .forms import signUpForm, loginForm

# Create your views here.
def signUpPage(request):
    form = signUpForm()

    if request.method == 'POST':
        form = signUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    context = {'form':form}
    return render(request, 'accounts/signup.html', context)


def loginPage(request):
    form = loginForm()

    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')

    context = {'form':form}
    return render(request, 'accounts/login.html', context)