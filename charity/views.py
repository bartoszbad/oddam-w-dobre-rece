from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

# Create your views here.
from charity.forms import RegisterForm, LoginForm
from charity.models import Donation


class LandingPageView(View):
    def get(self, request):
        donations = Donation.objects.all()
        bags_quantity = 0
        organizations = []
        for donation in donations:
            bags_quantity += donation.quantity
            if donation.institution not in organizations:
                organizations.append(donation.institution)
        context = {"bags_quantities": bags_quantity,
                   "organization_quantities": len(organizations)}
        return render(request, "index.html", context)


class AddDonationView(View):
    def get(self, request):
        return render(request, "form.html")


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", context={"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["login"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                url = request.GET.get('next', '/')
                return redirect(url)
            else:
                #raise ValidationError("Dane nie pasują")
                new_form = LoginForm()
                return render(request, "login.html", context={"form": new_form,
                                                              "message": "Podano błędne dane!"})



class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "register.html", context={"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(username=email, email=email,
                                            first_name=first_name, last_name=last_name,
                                            password=password)
            return redirect(reverse('login'))

        return render(request, "register.html", context={"form": form})
