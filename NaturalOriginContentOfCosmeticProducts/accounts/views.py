from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from django.contrib.auth import views as auth_views, mixins as auth_mixins, login, logout

from NaturalOriginContentOfCosmeticProducts.accounts.forms import AccountCreateForm, AccountProfileForm
from NaturalOriginContentOfCosmeticProducts.accounts.mixins import OwnerRequiredMixin
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


class AccountLoginView(auth_views.LoginView):
    template_name = "accounts/login_account.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        next_url = self.request.POST.get("next") or self.request.GET.get("next")
        if next_url and next_url.startswith("/"):
            return next_url

        return super().get_success_url()


def account_logout(request):
    logout(request)
    return redirect('index')


class AccountProfileDetailsView(OwnerRequiredMixin, auth_mixins.LoginRequiredMixin, views.DetailView):
    queryset = AccountProfileModel.objects.all().prefetch_related("company")
    template_name = "accounts/details_account_profile.html"


class AccountProfileUpdateView(OwnerRequiredMixin, auth_mixins.LoginRequiredMixin, views.UpdateView):
    queryset = AccountProfileModel.objects.all().prefetch_related("company")
    form_class = AccountProfileForm
    template_name = "accounts/update_account_profile.html"

    def get_success_url(self):
        return reverse("account_profile_details", kwargs={"pk": self.object.pk})
