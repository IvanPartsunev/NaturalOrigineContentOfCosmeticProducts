from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from NaturalOriginContentOfCosmeticProducts.calculate_noi.forms import CalculateNaturalOriginContentForm, MyFormSet


class CalculateNaturalOriginContentView(FormView):
    template_name = "calculate_raw_materials/calculate-natural-origin-content.html"
    form_class = CalculateNaturalOriginContentForm
    success_url = reverse_lazy("index")

    def post(self, request, *args, **kwargs):
        formset = MyFormSet(request.POST)

        if formset.is_valid() and any(form.cleaned_data for form in formset):
            return self.form_valid(formset)
        else:
            return render(request, self.template_name, {"formset": formset})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formset"] = MyFormSet()
        return context

    def form_valid(self, formset):
        for form in formset:
            form.save()
        return render(self.request, self.success_url)
