from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins

from NaturalOriginContentOfCosmeticProducts.products.forms import ProductCalculateNaturalContentForm, MyFormSet, \
    ProductCreateForm
from NaturalOriginContentOfCosmeticProducts.products.mixins import CalculateSaveMixin, OwnerRequiredMixin
from NaturalOriginContentOfCosmeticProducts.products.models import Product, ProductFormula
from NaturalOriginContentOfCosmeticProducts.raw_materials.models import RawMaterial


class ProductCreateView(views.CreateView):
    queryset = Product.objects.all()
    form_class = ProductCreateForm
    template_name = "products/product-create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse("product_details", kwargs={"pk": self.object.pk})
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductDetailsView(OwnerRequiredMixin, auth_mixins.LoginRequiredMixin, views.DetailView):
    queryset = Product.objects.prefetch_related("formulas")
    template_name = "products/product-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        last_formula = self.object.formulas.last()
        context["latest_formula"] = last_formula

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


class ProductUpdateView(OwnerRequiredMixin, auth_mixins.LoginRequiredMixin, views.UpdateView):
    queryset = Product.objects.all()
    template_name = "products/product-update.html"
    form_class = ProductCreateForm
    success_url = reverse_lazy("product_details")

    def get_success_url(self):
        return reverse("product_details", kwargs={"pk": self.object.pk})


class ProductDeleteView(OwnerRequiredMixin, auth_mixins.LoginRequiredMixin, views.DeleteView):
    queryset = Product.objects.all()
    template_name = "products/product-delete.html"
    success_url = reverse_lazy("product_list")


class ProductCalculateNaturalContentView(CalculateSaveMixin, views.FormView):

    template_name = "products/product-calculate-natural-content.html"
    form_class = ProductCalculateNaturalContentForm
    success_url = reverse_lazy("product_list")

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
                "error": self.CALCULATION_ERROR_MESSAGE,
            })

        self.save_natural_origin_content(product_natural_content)
        self.save_formula_recipe(formset)

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
        form.instance.owner = self.request.user
        product_id = self.request.session.get("product_id")

        form.instance.product_id = product_id
        form.save()

        self.request.session["formula_description"] = form.instance.description
        self.request.session["formula_id"] = form.instance.pk

        return super().form_valid(form)


class ProductFormulaDetailView(auth_mixins.LoginRequiredMixin, views.DetailView):
    queryset = ProductFormula.objects.all().prefetch_related("formula__raw_material")
    template_name = "products/product-formula-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        self.request.session["formula_description"] = self.object.description
        self.request.session["formula_id"] = self.object.pk

        product_id = self.request.session.get("product_id")
        product = get_object_or_404(Product, pk=product_id)

        product_formula = self.object
        raw_materials = product_formula.formula.all().select_related("raw_material") or None
        if raw_materials:
            related_raw_materials = {raw_material: raw_material.raw_material for raw_material in raw_materials}
            context['related_raw_materials'] = related_raw_materials

        context['product'] = product

        return context


class ProductFormulaDeleteView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    queryset = ProductFormula.objects.all().prefetch_related("formula__raw_material")
    template_name = "products/product-formula-details.html"
    success_url = reverse_lazy("index")

    def get_success_url(self):
        return reverse("product_details", kwargs={"pk": self.request.session.get("product_id")})
