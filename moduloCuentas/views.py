from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login

# Create your views here.


def home(request):
    return render(request, 'home/index.html')


@login_required
def tpv(request):
    return render(request, 'templatesVentas/cuerpoVenta.html')


def exit(request):
    logout(request)
    return redirect('home')


def register(request):

    data = {'form': CustomUserCreationForm()}

    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)

        if user_creation_form.is_valid():

            user_creation_form.save()
            user = authenticate(
                username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            login(request,user)
            return redirect('home')

    return render(request, 'registration/register.html', data)
