from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm
from django.contrib import messages


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Аккаунт создан для {username}!")
            return redirect("login")
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, template_name='register.html', context=context)


def profile(request):
    return render(request, template_name='profile.html')
