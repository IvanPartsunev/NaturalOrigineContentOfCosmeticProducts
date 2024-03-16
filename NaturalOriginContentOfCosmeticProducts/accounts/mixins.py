from django.contrib.auth.mixins import AccessMixin


class OwnerRequiredMixin(AccessMixin):
    """Verify that the current user has this profile."""
    permission_denied_message = "You are not authorized to open this page!"

    #  TODO Override get_permission_denied_message to render my own 403 page

    def dispatch(self, request, *args, **kwargs):
        if request.user.pk != kwargs.get('pk', None):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
