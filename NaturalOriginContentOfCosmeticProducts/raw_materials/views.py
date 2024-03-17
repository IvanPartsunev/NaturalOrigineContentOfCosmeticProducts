from django.contrib.auth import mixins as auth_mixins
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from django.views.generic.edit import FormMixin

from NaturalOriginContentOfCosmeticProducts.raw_materials.forms import RawMaterialForm
from NaturalOriginContentOfCosmeticProducts.raw_materials.models import RawMaterial


class RawMaterialCreateView(auth_mixins.LoginRequiredMixin, views.CreateView):

    form_class = RawMaterialForm
    template_name = "raw_material/create_raw_material.html"
    success_url = "index.html"


class RawMaterialListView(views.ListView):
    model = RawMaterial
    template_name = "raw_material/list-of-raw-material.html"
    paginate_by = 5
    ordering = ["trade_name"]


class RawMaterialDetailsView(FormMixin, views.DetailView):
    queryset = RawMaterial.objects.all()
    form_class = RawMaterialForm
    template_name = "raw_material/details-of-raw-material.html"
    success_url = reverse_lazy("details_raw_material")


class RawMaterialUpdateView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    queryset = RawMaterial.objects.all()
    form_class = RawMaterialForm
    template_name = "raw_material/update_raw_material.html"

    def get_success_url(self):
        return reverse("details_raw_material", kwargs={"pk": self.object.pk})

    # def get_object(self, queryset=None):
    #     initital_pk = self.request.GET.get("raw_material")
    #
    #     if self.request.method == "GET" and initital_pk:
    #         obj = RawMaterial.objects.get(pk=initital_pk)
    #         return obj
    #     else:
    #         return super().get_object(queryset)
    #
    # def get_context_data(self, **kwargs):
    #
    #     context = super().get_context_data(**kwargs)
    #     context["existing_materials"] = RawMaterial.objects.all()
    #
    #     return context





class RawMaterialDeleteView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    pass



