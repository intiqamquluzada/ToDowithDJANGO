from django.shortcuts import render, redirect
from .models import User, Profile
from django.contrib.auth import login, logout
from .forms import LoginForm


def login_view(request):
    context = {}
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST or None)
        if form.is_valid():
            user = User.objects.get(username=form.cleaned_data.get("username"))
            login(request, user)
            return redirect("todo:list")
    context['form'] = form
    return render(request, 'login.html', context)


def register_view(request):
    context = {}
    if request.method == "POST":
        user = User.objects.create(
            first_name=request.POST.get('name'),
            last_name=request.POST.get('surname'),
            username=request.POST.get('username'),

        )
        user.set_password(request.POST.get("password"))
        user.save()
        login(request, user)
        return redirect("accounts:register")

    return render(request, 'register.html', context)


def logout_view(request):
    logout(request)
    return redirect('accounts:login')
