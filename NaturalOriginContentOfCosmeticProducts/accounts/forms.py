from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms

from NaturalOriginContentOfCosmeticProducts.accounts.models import AccountProfileModel

UserModel = get_user_model()


class AccountCreateForm(auth_forms.UserCreationForm):
    class Meta(auth_forms.UserCreationForm.Meta):
        model = UserModel
        fields = (
            "email",
            "company_name",
        )


class AccountUpdateForm(auth_forms.UserChangeForm):
    class Meta(auth_forms.UserChangeForm.Meta):
        model = UserModel
        fields = "__all__"


class AccountProfileForm(forms.ModelForm):
    class Meta:
        model = AccountProfileModel
        fields = (
            "first_name",
            "last_name",
            "company_website",
            "company_logo"
        )


