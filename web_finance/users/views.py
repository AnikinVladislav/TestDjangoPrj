from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from .forms import *

# Create your views here.
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            messages.success(request, ("Erorr Logging In, Try Again"))
            return redirect('login')  
    else:
        return render(request, "users/login.html")

def logout_user(request):
    logout(request)
    messages.success(request, ("You were logout"))
    return redirect('main')


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, ("Account was registrated"))
            return redirect('main')
    else:
        form = RegisterUserForm()
    return render(request, "users/register.html",{
        'form': form,
    })

class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('main')

    def get_object(self):
        return self.request.user


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('main')
