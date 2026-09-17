from django.shortcuts import render, redirect 
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from .forms import RegistrationForm

def hello_world(request):
    return HttpResponse("Hello, world!")

# Đã gộp/bỏ hàm index trùng lặp
def index(request):
    context = {
        'message': 'Đây là trang home app dùng Jinja Template'
    }
    return render(request, 'page/home.html', context)

def contact(request):
    return render(request, 'page/contact.html')

def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request, 'page/register.html', {'form': form})

def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, "Successfully Logged In")
            return HttpResponseRedirect("/")
        else:
            messages.error(request, "Invalid Credentials")
            return render(request, 'page/login.html') # Đã sửa pages -> page
    return render(request, "page/login.html") # Đã sửa pages -> page

def logout_view(request):
    auth_logout(request)
    messages.success(request, "Successfully logged out")
    return HttpResponseRedirect('/login/')