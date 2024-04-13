from django.contrib.auth import mixins as auth_mixins
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from django.views.generic.edit import FormMixin

from NaturalOriginContentOfCosmeticProducts.core.forms import SearchForm
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
    template_name = "raw_materials/raw-material-list.html"
    paginate_by = 12
    ordering = ["trade_name"]

    def get_queryset(self):
        queryset = RawMaterial.objects.filter(is_deleted=False).order_by("trade_name")
        search_query = self.request.GET.get("search_query")
        if search_query:
            queryset = queryset.filter(Q(trade_name__icontains=search_query) | Q(inci_name__icontains=search_query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("search_query", "")
        return context


class RawMaterialDetailsView(FormMixin, views.DetailView):
    queryset = RawMaterial.objects.all()
    form_class = RawMaterialForm
    template_name = "raw_materials/raw-material-details.html"

    def form_valid(self, form):
        return HttpResponseRedirect(reverse("product_details"), {"pk": self.object.pk})


class RawMaterialUpdateView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    """
    In GET method if material is selected from select raw material form, data for the raw material is loaded.
    """
    queryset = RawMaterial.objects.all()
    form_class = RawMaterialForm
    template_name = "raw_materials/raw-material-update.html"

    def get_success_url(self):
        return reverse("raw_material_details", kwargs={"pk": self.object.pk})

    def get_object(self, queryset=None):
        initital_name = self.request.POST.get("trade_name")

        if self.request.method == "POST" and initital_name:
            obj = RawMaterial.objects.get(trade_name=initital_name)
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

