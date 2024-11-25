from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout
from .forms import CustomCustomerCreationForm, CustomAuthenticationForm
from django.conf import settings


def landing(request):
    return render(request, 'landing.html')

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = CustomCustomerCreationForm(request.POST)
        if form.is_valid():
            customer = form.save()
            print(f"Customer {customer.username} created successfully!")
            login(request, customer)
            return redirect('/home')
    else:
        form = CustomCustomerCreationForm()
    return render(request, 'customers/register.html', {'form': form})

def customer_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            if username == "admin" and password == "ubumuntu123":
                print("Admin credentials matched!")  
                request.session['is_admin'] = True
                return redirect('/dashboard')
            else:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/home')  
                else:

                    form.add_error(None, 'Invalid credentials')
        else:
            form.add_error(None, 'Please correct the errors below.')

    else:
        form = CustomAuthenticationForm()

    return render(request, 'customers/login.html', {'form': form})


def customer_logout(request):
    logout(request)
    return redirect('customer_login')