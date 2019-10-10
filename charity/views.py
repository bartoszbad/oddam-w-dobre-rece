from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View

# Create your views here.
from charity.forms import RegisterForm, LoginForm
from charity.models import Donation, Category, Institution


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
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        return render(request, "form.html", context={"categories": categories,
                                                     "institutions": institutions})

    def post(self, request):
        print("post")
        quantity = request.POST.get("bags")
        print(quantity)
        return redirect(reverse("form_confirmation"))


class AddDonationConfirmView(View):
    def get(self, request):
        return render(request, "form-confirmation.html")


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
            existing_email = User.objects.filter(email=username)
            if user is not None:
                login(request, user)
                url = request.GET.get('next', '/')
                return redirect(url)
            elif not existing_email:
                return redirect(reverse('register'))
            else:
                new_form = LoginForm()
                return render(request, "login.html", context={"form": new_form,
                                                              "message": "Podano błędne dane!"})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('landing_page'))


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


class UserProfileView(View):
    def get(self, request):
        donations = Donation.objects.filter(user_id=request.user.id).order_by('is_taken')
        return render(request, 'profile.html', context={"user": request.user,
                                                        "donations": donations})


class DonationStatusEditView(View):
    def get(self, request, donation_id):
        donation = get_object_or_404(Donation, pk=donation_id)
        donation.is_taken = not donation.is_taken
        donation.save()
        return redirect(f'/Profile/#donations')

