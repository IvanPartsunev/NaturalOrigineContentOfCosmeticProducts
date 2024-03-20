from django.http import JsonResponse
from django.shortcuts import render

from NaturalOriginContentOfCosmeticProducts.raw_materials.models import RawMaterial


def index(request):
    return render(request, 'core/index.html')


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
