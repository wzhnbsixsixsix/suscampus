from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
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
            username = request.POST["username"]
            password = request.POST["password"]

            user = authenticate(request, username=username, password=password)
            
            if user is not None: 
                login(request, user)
                return redirect('home')
            
            else:
                form.add_error(None, 'Invalid username or password')
            
        else:
            context = {'form':form}
            return render(request, 'account/login.html', context)

    context = {'form':form}
    return render(request, 'accounts/login.html', context)