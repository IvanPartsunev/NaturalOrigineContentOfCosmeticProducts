from django.contrib.auth import mixins as auth_mixins
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from django.views.generic.edit import FormMixin

from NaturalOriginContentOfCosmeticProducts.core.mixins import StaffRequiredMixin
from NaturalOriginContentOfCosmeticProducts.raw_materials.forms import RawMaterialForm
from NaturalOriginContentOfCosmeticProducts.raw_materials.models import RawMaterial


class RawMaterialCreateView(auth_mixins.LoginRequiredMixin, views.CreateView):

    form_class = RawMaterialForm
    template_name = "raw_materials/raw-material-create.html"
    success_url = reverse_lazy("raw_material_list")

    def form_valid(self, form):
        material_type = form.cleaned_data.get("material_type")
        if material_type == "NN":
            form.instance.natural_origin_content = 0

        return super().form_valid(form)


class RawMaterialListView(views.ListView):
    queryset = RawMaterial.objects.filter(is_deleted=False)
    template_name = "raw_materials/raw-material-list.html"
    paginate_by = 5
    ordering = ["trade_name"]


class RawMaterialDetailsView(FormMixin, views.DetailView):
    queryset = RawMaterial.objects.all()
    form_class = RawMaterialForm
    template_name = "raw_materials/raw-material-details.html"

    def form_valid(self, form):
        return HttpResponseRedirect(reverse("product_details"), {"pk": self.object.pk})


class RawMaterialUpdateView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    queryset = RawMaterial.objects.all()
    form_class = RawMaterialForm
    template_name = "raw_materials/raw-material-update.html"

    def get_success_url(self):
        return reverse("raw_material_details", kwargs={"pk": self.object.pk})

    def get_object(self, queryset=None):
        initital_pk = self.request.GET.get("raw_material")

        if self.request.method == "GET" and initital_pk:
            obj = RawMaterial.objects.get(pk=initital_pk)
            return obj
        else:
            return super().get_object(queryset)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["existing_materials"] = RawMaterial.objects.all()

        return context


class RawMaterialDeleteView(auth_mixins.LoginRequiredMixin, StaffRequiredMixin, views.DeleteView):
    queryset = RawMaterial.objects.all()
    template_name = "raw_materials/raw-material-delete.html"
    success_url = reverse_lazy("raw_material_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.is_deleted = True
        self.object.save()
        return HttpResponseRedirect(success_url)

