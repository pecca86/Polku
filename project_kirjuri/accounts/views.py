from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView
from . import forms
from .forms import UserCreateForm

# Create your views here.
class SignUp(CreateView):
    #form_class = forms.UserCreateForm
    form_class = UserCreateForm
    success_url = reverse_lazy("logout")
    template_name = "accounts/signup.html"
