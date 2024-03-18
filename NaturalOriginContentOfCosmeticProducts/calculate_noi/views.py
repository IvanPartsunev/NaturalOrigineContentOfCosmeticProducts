from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as view

from NaturalOriginContentOfCosmeticProducts.calculate_noi.forms import CalculateNaturalContentForm, MyFormSet
from NaturalOriginContentOfCosmeticProducts.raw_materials.models import RawMaterial


class CalculateNaturalContentView(view.FormView):
    template_name = "calculate_natural_content/calculate-natural-content.html"
    form_class = CalculateNaturalContentForm
    success_url = reverse_lazy("index")

    def post(self, request, *args, **kwargs):
        formset = MyFormSet(request.POST)

        if formset.is_valid() and any(form.cleaned_data for form in formset):
            return self.form_valid(formset)
        else:
            existing_materials = RawMaterial.objects.all()
            return render(request, self.template_name, {"formset": formset, "existing_materials": existing_materials})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formset"] = MyFormSet()
        context["existing_materials"] = RawMaterial.objects.all()
        return context

    def form_valid(self, formset):
        for form in formset:
            form.save()
        return render(self.request, self.success_url)


def get_material_data_for_autofill(request):
    raw_material_id = request.GET.get("raw_material_id")
    raw_material = RawMaterial.objects.get(pk=raw_material_id)

    data = {
        'name': raw_material.trade_name,
        'inci': raw_material.inci_name,
        'type': raw_material.material_type,
        'nat_content': raw_material.natural_origin_content,
    }
    return JsonResponse(data)
