from django.shortcuts import redirect, render
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


