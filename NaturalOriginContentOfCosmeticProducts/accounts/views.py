from time import sleep

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import views as auth_views, login, logout

from NaturalOriginContentOfCosmeticProducts.accounts.forms import AccountCreateForm, AccountProfileForm
from NaturalOriginContentOfCosmeticProducts.accounts.models import AccountModel, AccountProfileModel


class AccountCreateView(views.CreateView):
    queryset = AccountModel.objects.all()
    form_class = AccountCreateForm
    template_name = "accounts/register_account.html"
    success_url = reverse_lazy("account_profile_update")

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, form.instance)
        return result


class AccountProfileUpdateView(views.UpdateView):
    queryset = AccountProfileModel.objects.all().prefetch_related("company")
    form_class = AccountProfileForm
    template_name = "accounts/update_account_profile.html"
    success_url = reverse_lazy("index")


# class AccountDetailView(views.DetailView):
#     queryset = AccountModel.objects.all().select_related("accountprofilemodel")


class AccountLoginView(auth_views.LoginView):
    template_name = "accounts/login_account.html"
    redirect_authenticated_user = True


def account_logout(request):
    logout(request)
    return redirect('index')



