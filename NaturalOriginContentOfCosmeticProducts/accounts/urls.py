from django.urls import path

from NaturalOriginContentOfCosmeticProducts.accounts.views import AccountCreateView, AccountProfileUpdateView, \
    AccountLoginView, account_logout_view, AccountProfileDetailsView

urlpatterns = (
    path("registation/", AccountCreateView.as_view(), name="account_registration"),
    path("login/", AccountLoginView.as_view(), name="account_login"),
    path("logout/", account_logout_view, name="account_logout"),
    path("profile_update/<int:pk>", AccountProfileUpdateView.as_view(), name="account_profile_update"),
    path("profile_details/<int:pk>", AccountProfileDetailsView.as_view(), name="account_profile_details"),
)
