from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View

# Create your views here.
from charity.forms import RegisterForm, LoginForm, EditProfileForm, EditPasswordForm, RemindPasswordForm, \
    ResetPasswordForm
from charity.models import Donation, Category, Institution
from charity.tokens import account_activation_token


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
        quantity = request.POST.get("bags")
        categories = request.POST.getlist("categories")  # pobiera listę z nazwami kategorii
        categories_objects = Category.objects.filter(name__in=categories)
        institution = request.POST.get("organization")
        institution_object = Institution.objects.get(name=institution)
        address = request.POST.get("address")
        city = request.POST.get("city")
        zip_code = request.POST.get("postcode")
        phone_number = request.POST.get("phone")
        date = request.POST.get("data")
        time = request.POST.get("time")
        comment = request.POST.get("more_info")
        donation = Donation.objects.create(quantity=quantity, address=address, phone_number=phone_number,
                                           city=city, zip_code=zip_code, pick_up_date=date, pick_up_time=time,
                                           pick_up_comment=comment, user=request.user,
                                           institution_id=institution_object.id)
        donation.categories.set(categories_objects)
        donation.save()
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
                                            password=password, is_active=False)
            current_site = get_current_site(request)
            mail_subject = 'Aktywuj swoje konto na Oddaj w dobre ręce!'
            message = render_to_string('account_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            activation_email = EmailMessage(
                mail_subject, message, to=[email]
            )
            activation_email.send()
            return redirect(reverse('landing_page'))

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


class EditUserProfileView(View):
    def get(self, request):
        form = EditProfileForm(initial={"first_name": request.user.first_name,
                                        "last_name": request.user.last_name,
                                        "email": request.user.email})
        return render(request, 'edit_profile.html', context={"form": form})

    def post(self, request):
        form = EditProfileForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.user.email, password=form.cleaned_data["password"])
            if user is not None:
                user.first_name = form.cleaned_data["first_name"]
                user.last_name = form.cleaned_data["last_name"]
                user.email = form.cleaned_data["email"]
                user.save()
                return redirect(reverse('profile'))
            else:
                form = EditProfileForm(initial={"first_name": form.cleaned_data["first_name"],
                                                "last_name": form.cleaned_data["last_name"],
                                                "email": form.cleaned_data["email"]})
                message = "Podano błędne hasło!"
                return render(request, "edit_profile.html", context={"form": form,
                                                                     "message": message})
        return render(request, 'edit_profile.html', context={"form": form})


class EditUserPasswordView(View):
    def get(self, request):
        form = EditPasswordForm()
        return render(request, 'edit_password.html', context={"form": form})

    def post(self, request):
        form = EditPasswordForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.user.email, password=form.cleaned_data["old_password"])
            if user is not None:
                user.set_password(form.cleaned_data["new_password"])
                user.save()
                return redirect(reverse('profile'))
            else:
                message = "Podano błędne hasło!"
                return render(request, "edit_profile.html", context={"form": form,
                                                                     "message": message})
        return render(request, 'edit_profile.html', context={"form": form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('landing_page')
    else:
        return redirect('register')


class RemindPasswordView(View):
    def get(self, request):
        form = RemindPasswordForm()
        return render(request, 'remind_password.html', context={"form": form})

    def post(self, request):
        form = RemindPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.get(email=email)
            if not user:
                form = RemindPasswordForm()
                return render(request, 'remind_password.html', context={"form": form,
                                                                        "message": "Nie ma takiego konta!"})
            else:
                current_site = get_current_site(request)
                mail_subject = 'Resetuj hasło do konta na portalu Oddaj w dobre ręce!'
                message = render_to_string('password_reset_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.id)),
                    'token': account_activation_token.make_token(user),
                })
                password_reset_email = EmailMessage(
                    mail_subject, message, to=[email]
                )
                password_reset_email.send()
                return redirect(reverse('landing_page'))

        return render(request, "remind_password.html")


def reset(request, uidb64, token):
    if request.method == "GET":
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            form = ResetPasswordForm()
            return render(request, "reset_password.html", context={"user": user,
                                                                   "form": form})
        else:
            return redirect("landing_page")
    elif request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = request.POST.get("email")
            user = User.objects.get(email=email)
            user.set_password(form.cleaned_data["new_password"])
            user.save()
            return redirect(reverse('login'))
        else:
            return render(request, 'reset_password.html', context={"form": form})
