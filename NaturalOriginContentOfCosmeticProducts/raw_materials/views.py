from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from NaturalOriginContentOfCosmeticProducts.raw_materials.forms import RawMaterialForm
from NaturalOriginContentOfCosmeticProducts.raw_materials.models import RawMaterial


class CreateRawMaterialView(CreateView):

    form_class = RawMaterialForm
    template_name = "raw_material/create_raw_material.html"
    success_url = "index.html"


class UpdateRawMaterialView(UpdateView):
    queryset = RawMaterial.objects.all()
    form_class = RawMaterialForm
    template_name = "raw_material/update_raw_material.html"
    # TODO make success url to redirect to raw material details if
    #  raw material is successfully updated and to return back to form if not.

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
