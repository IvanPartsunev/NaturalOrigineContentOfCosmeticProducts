from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from django.contrib.auth import views as auth_views, mixins as auth_mixins

from NaturalOriginContentOfCosmeticProducts.calculate_noi.forms import ProductCalculateNaturalContentForm, MyFormSet, \
    ProductCreateForm
from NaturalOriginContentOfCosmeticProducts.calculate_noi.mixins import CalculateSaveMixin, OwnerRequiredMixin
from NaturalOriginContentOfCosmeticProducts.calculate_noi.models import Product, ProductFormula, \
    ProductFormulaRawMaterial
from NaturalOriginContentOfCosmeticProducts.raw_materials.models import RawMaterial


class ProductCreateView(views.CreateView):
    queryset = Product.objects.all()
    form_class = ProductCreateForm
    template_name = "products/product-create.html"
    success_url = reverse_lazy("index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.request.session["product_id"] = kwargs.get("pk")
        return context

    def get_success_url(self):
        return reverse("product_details", kwargs={"pk": self.object.pk})
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductDetailsView(OwnerRequiredMixin, auth_mixins.LoginRequiredMixin, views.DetailView):
    queryset = Product.objects.all()
    template_name = "products/product-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product_name = self.object.product_name
        product_id = self.object.pk

        self.request.session["product_name"] = product_name
        self.request.session["product_id"] = product_id

        return context


class ProductListView(auth_mixins.LoginRequiredMixin, views.ListView):
    template_name = "products/product-list.html"
    paginate_by = 5
    ordering = ["product_name"]

    def get_queryset(self):
        queryset = Product.objects.filter(owner_id=self.request.user.pk)
        return queryset


class ProductDeleteView(OwnerRequiredMixin, auth_mixins.LoginRequiredMixin, views.DeleteView):
    queryset = Product.objects.all()
    template_name = "products/product-delete.html"
    success_url = reverse_lazy("index")


class ProductCalculateNaturalContentView(CalculateSaveMixin, views.FormView):

    template_name = "products/calculate-natural-content.html"
    form_class = ProductCalculateNaturalContentForm
    success_url = reverse_lazy("index")

    def post(self, request, *args, **kwargs):
        formset = MyFormSet(request.POST)
        if formset.is_valid() and any(form.cleaned_data for form in formset):
            return self.form_valid(formset)
        else:
            existing_materials = RawMaterial.objects.all()
            context = {
                "formset": formset,
                "existing_materials": existing_materials,
                "product_name": self.request.session.get("product_name"),
                "formula_description": self.request.session.get("formula_description")
            }
            return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formset"] = MyFormSet()
        context["existing_materials"] = RawMaterial.objects.all()
        context["product_name"] = self.request.session.get("product_name")
        context["formula_description"] = self.request.session.get("formula_description")
        return context

    def form_valid(self, formset):
        self.save_not_existing_raw_materials(formset)

        product_natural_content = self.calculate_product_natural_content(formset)

        if not product_natural_content:
            existing_materials = RawMaterial.objects.all()
            return render(self.request, self.template_name, {
                "formset": formset,
                "existing_materials": existing_materials,
                "error": "Sum of raw material's content should be 100% or above!"
            })

        self.save_natural_origin_content(product_natural_content)
        self.save_formula_recipe(formset)

        self.request.session.clear()

        return super().form_valid(formset)


class ProductFormulaCreateView(auth_mixins.LoginRequiredMixin, views.CreateView):
    queryset = ProductFormula.objects.all()
    template_name = "products/product-formula-create.html"
    success_url = reverse_lazy("product_calculate_noc")
    fields = ["description"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product_name"] = self.request.session.get("product_name")

        return context

    def form_valid(self, form):
        product_id = self.request.session.get("product_id")

        form.instance.product_id = product_id
        form.save()

        formula_description = form.instance.description
        formula_id = form.instance.pk

        self.request.session["formula_description"] = formula_description
        self.request.session["formula_id"] = formula_id

        return super().form_valid(form)


class ProductFormulaDeleteView(OwnerRequiredMixin, auth_mixins.LoginRequiredMixin, views.DeleteView):
    queryset = Product.objects.all()
    template_name = "products/product-delete.html"
    success_url = reverse_lazy("index")

