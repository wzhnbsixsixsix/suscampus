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
    form = loginForm(request)

    if request.method == 'POST':
        form = loginForm(request, data=request.POST)
        print("checkpoint 1")
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)
            
            if user is not None: 
                print("checkpoint 2")
                login(request, user)
                return redirect('home')
            
            else:
                print("checkpoint 3")
                form.add_error(None, 'Invalid username or password')
            
        else:
            context = {'form':form}
            return render(request, 'accounts/login.html', context)

    context = {'form':form}
    return render(request, 'accounts/login.html', context)
