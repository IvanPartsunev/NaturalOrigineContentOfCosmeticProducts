from django.contrib.auth import mixins as auth_mixins
from django.db import models


class CreateUpdateMixin(models.Model):
    created_on = models.DateField(auto_now_add=True)
    edited_on = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class StaffRequiredMixin(auth_mixins.UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class FormatAdminDate:
    def formatted_edited_on(self, obj):
        return obj.edited_on.strftime("%d-%m-%Y")

    formatted_edited_on.short_description = "Edited On"

    def formatted_created_on(self, obj):
        return obj.created_on.strftime("%d-%m-%Y")

    formatted_created_on.short_description = "Created On"

    readonly_fields = ("formatted_edited_on", "formatted_created_on")
