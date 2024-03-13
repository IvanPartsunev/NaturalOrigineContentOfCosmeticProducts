from django.contrib import admin
from django.contrib.auth import admin as auth_admin, get_user_model
from NaturalOriginContentOfCosmeticProducts.accounts.forms import AccountCreateForm, AccountUpdateForm
from NaturalOriginContentOfCosmeticProducts.accounts.models import AccountProfileModel

UserModel = get_user_model()


@admin.register(UserModel)
class UserModelAdmin(auth_admin.UserAdmin):
    model = UserModel
    add_form = AccountCreateForm
    form = AccountUpdateForm

    list_display = (
        "email",
        "company_name",
        "is_staff",
        "is_superuser"
    )

    search_fields = (
        "email",
        "company_name",
    )

    ordering = ("company_name", )

    fieldsets = (
        (None, {'fields': ('email', 'company_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups',
                                    'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "company_name", "password1", "password2"),
            },
        ),
    )


@admin.register(AccountProfileModel)
class UserProfileModelAdmin(admin.ModelAdmin):
    list_display = (
        "company",
        "first_name",
        "last_name",
        "company_website",
        "company_logo",
    )
