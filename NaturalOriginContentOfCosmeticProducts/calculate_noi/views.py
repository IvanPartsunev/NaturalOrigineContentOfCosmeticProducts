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

        self.save_not_existing_raw_materials(formset)
        self.calculate_product_natural_content(formset)

        return super().form_valid(formset)

    def save_not_existing_raw_materials(self, formset):
        all_raw_materials = RawMaterial.objects.values_list("trade_name", flat=True)
        for form in formset:
            form.cleaned_data.get("")
            if form.cleaned_data.get("current_trade_name") in all_raw_materials:
                continue
            else:
                form.save()

    def calculate_product_natural_content(self, raw_materials):
        product_raw_natural_content = []

        for raw_material in raw_materials:
            content_in_formulation = raw_material.cleaned_data.get("raw_material_content")
            natural_origin_content = raw_material.cleaned_data.get("natural_origin_content")

            calculated = content_in_formulation * natural_origin_content / 100
            product_raw_natural_content.append(calculated)

        return sum(product_raw_natural_content)
