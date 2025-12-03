from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm



def index(request):

    return render(request, 'index.html')

# def login(request):
#
#     return render(request, 'login.html')


# views.py


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})