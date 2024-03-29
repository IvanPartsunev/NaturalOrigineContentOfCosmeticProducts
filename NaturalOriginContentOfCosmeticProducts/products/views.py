from django.forms import formset_factory
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins

from NaturalOriginContentOfCosmeticProducts.core.forms import SearchForm
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
    """
    The Flow of the project away comes to here, and session data for product is set here.
    """

    queryset = Product.objects.prefetch_related("product")
    template_name = "products/product-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        """Obtain last formulation for the product"""
        last_formula = self.object.product.last()
        context["latest_formula"] = last_formula

        product_name = self.object.product_name
        product_id = self.object.pk

        self.request.session["product_name"] = product_name
        self.request.session["product_id"] = product_id

        return context


class ProductListView(auth_mixins.LoginRequiredMixin, views.ListView):
    """
    Start of creation or updating proces. Product session data is reset in this view.
    """

    template_name = "products/product-list.html"
    paginate_by = 12
    ordering = ["product_name"]

    def get_queryset(self):
        queryset = Product.objects.filter(owner_id=self.request.user.pk).order_by("product_name")
        search_query = self.request.GET.get("search_field")
        if search_query:
            queryset = queryset.filter(product_name__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForm(self.request.GET)

        self.request.session["product_name"] = None
        self.request.session["product_id"] = None

        return context


class ProductUpdateView(OwnerRequiredMixin, auth_mixins.LoginRequiredMixin, views.UpdateView):
    queryset = Product.objects.all()
    template_name = "products/product-update.html"
    form_class = ProductCreateForm

    def get_success_url(self):
        return reverse("product_details", kwargs={"pk": self.object.pk})


class ProductDeleteView(OwnerRequiredMixin, auth_mixins.LoginRequiredMixin, views.DeleteView):
    queryset = Product.objects.all()
    template_name = "products/product-delete.html"
    success_url = reverse_lazy("product_list")

    def post(self, request, *args, **kwargs):
        """
        Clear session data for deleted formula
        """
        self.request.session["product_name"] = None
        self.request.session["product_id"] = None
        return super().post(request, *args, **kwargs)


class ProductFormulaCreateView(auth_mixins.LoginRequiredMixin, views.CreateView):
    queryset = ProductFormula.objects.all()
    template_name = "products/product-formula-create.html"
    success_url = reverse_lazy("product_calculate_noc")
    fields = ["description"]
    labels = {
        "description": "Formula description"
    }

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


# class ProductFormulaUpdateView(auth_mixins.LoginRequiredMixin, views.DeleteView):
#     queryset = ProductFormula.objects.all()
#     template_name = "products/product-calculate-natural-content.html"
#     form_class = ProductCalculateNaturalContentForm
#     success_url = reverse_lazy("index")


class ProductFormulaDeleteView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    queryset = ProductFormula.objects.all().prefetch_related("formula__raw_material")
    template_name = "products/product-formula-details.html"

    def get_success_url(self):
        """
        Clear session data for deleted formula
        """
        self.request.session["formula_description"] = None
        self.request.session["formula_id"] = None
        return reverse("product_details", kwargs={"pk": self.request.session.get("product_id")})


class ProductCalculateNaturalContentView(CalculateSaveMixin, views.FormView):
    """
    This view is used to calculate and also update product formulations.

    """

    template_name = "products/product-calculate-natural-content.html"
    form_class = ProductCalculateNaturalContentForm
    success_url = reverse_lazy("product_list")

    def get(self, request, *args, **kwargs):
        formula_pk = kwargs.get("pk")
        if not formula_pk:
            return super().get(request, *args, **kwargs)

        product_formula_data = (ProductFormula.objects
                                .select_related("product")
                                .prefetch_related("formula__raw_material")
                                .get(pk=formula_pk))

        initial_data = []

        product = product_formula_data.product.product_name

        product_formula = product_formula_data.formula.all()

        for product in product_formula:
            data = {
                "current_trade_name": "",
                "inci_name": "",
                "raw_material_content": 0,
                "material_type": "",
                "natural_origin_content": 0,
            }
            raw_material = product.raw_material

            data["current_trade_name"] = raw_material.trade_name
            data["inci_name"] = raw_material.inci_name
            data["raw_material_content"] = product.raw_material_content
            data["material_type"] = raw_material.material_type
            data["natural_origin_content"] = raw_material.natural_origin_content

            initial_data.append(data)

        GetFormSet = formset_factory(ProductCalculateNaturalContentForm, extra=0)
        formset = GetFormSet(initial=initial_data)

        return self.render_to_response(self.get_context_data(formset=formset))

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
        existing_materials = RawMaterial.objects.all()
        submitted_formset = kwargs.get("formset")

        if self.request.method == "GET":
            context["formset"] = submitted_formset if submitted_formset else MyFormSet()
            context["existing_materials"] = existing_materials
            context["product_name"] = self.request.session.get("product_name")
            context["formula_description"] = self.request.session.get("formula_description")

        elif self.request.method == "POST":
            context["formset"] = submitted_formset if submitted_formset.is_valid() else MyFormSet()
            context["existing_materials"] = existing_materials
            context["product_name"] = self.request.session.get("product_name")
            context["formula_description"] = self.request.session.get("formula_description")

        return context

    def form_valid(self, formset):
        # TODO Product natural content to be saved in product formula, not directly in product.
        #  In product natural content have to be saved manually, decided by the user.
        #  Probably in update.

        self.save_not_existing_raw_materials(formset)

        product_natural_content = self.calculate_product_natural_content(formset)

        if not product_natural_content:
            existing_materials = RawMaterial.objects.all()
            return render(self.request, self.template_name, {
                "formset": formset,
                "existing_materials": existing_materials,
                "calculation_error": self.CALCULATION_ERROR_MESSAGE,
            })

        self.save_natural_origin_content(product_natural_content)
        self.save_formula_recipe(formset)

        return super().form_valid(formset)
