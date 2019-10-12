"""oddam_w_dobre_rece URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from charity.views import LandingPageView, AddDonationView, LoginView, RegisterView, LogoutView, UserProfileView, \
    DonationStatusEditView, AddDonationConfirmView, EditUserProfileView, EditUserPasswordView, activate, \
    RemindPasswordView, reset, ContactFormView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name="landing_page"),
    path('AddDonation/', login_required(AddDonationView.as_view()), name="add_donation"),
    path('Login/', LoginView.as_view(), name="login"),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name="activate"),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', reset, name="reset"),
    path('Register/', RegisterView.as_view(), name="register"),
    path('Logout/', login_required(LogoutView.as_view()), name="logout"),
    path('Profile/', login_required(UserProfileView.as_view()), name="profile"),
    path('EditProfile/', login_required(EditUserProfileView.as_view()), name="edit_profile"),
    path('ChangePassword/', login_required(EditUserPasswordView.as_view()), name="edit_password"),
    path('Donation/<int:donation_id>/', login_required(DonationStatusEditView.as_view()), name="status"),
    path('AddDonationConfirm/', login_required(AddDonationConfirmView.as_view()), name="form_confirmation"),
    path('RemindPassword/', RemindPasswordView.as_view(), name="remind_password"),
    path('ContactForm/', ContactFormView.as_view(), name="contact_form")
]
