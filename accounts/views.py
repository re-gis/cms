from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.views import View
from accounts.models import CustomUser
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, "accounts/register.html", {"form": form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect("login")
        return render(request, "accounts/register.html", {"form": form})


class CustomLoginView(View):
    template_name = "accounts/login.html"
    form_class = LoginForm

    def get_success_url(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return reverse("project_list")
        else:
            return reverse("assigned_projects")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(self.get_success_url())
            else:
                form.add_error(None, "Invalid username or password.")
        return render(request, self.template_name, {"form": form})


class CustomLogoutView(LogoutView):
    next_page = "login"


def redirect_to_login(request):
    return redirect("login")
