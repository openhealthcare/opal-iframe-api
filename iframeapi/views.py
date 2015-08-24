"""
Views for the iframeapi OPAL Plugin
"""
from django.http import HttpResponseBadRequest
from django.template.response import TemplateResponse
from opal.core.search.queries import get_model_from_column_name
from opal.utils import camelcase_to_underscore
from opal import models as opal_models
from iframeapi.models import ApiKey


def get_template_name(model):
    name = camelcase_to_underscore(model.__name__)
    return ['iframe_templates/{0}.html'.format(name)]


def iframe_api(request):
    hospital_number = request.GET.get("hospitalNumber")
    column_name = request.GET.get("column")
    latest = bool(request.GET.get("latest"))

    try:
        api_key = ApiKey.objects.get(key=request.GET.get("key"))
    except ApiKey.DoesNotExist:
        return HttpResponseBadRequest("missing or invalid key")

    api_key.used()

    if column_name and hospital_number:
        model = get_model_from_column_name(column_name)

        if model:
            result_set = None

            if issubclass(model, opal_models.PatientSubrecord):
                result_set = model.objects.filter(
                    patient__demographics__hospital_number=hospital_number
                )

            if issubclass(model, opal_models.EpisodeSubrecord):
                result_set = model.objects.filter(
                    episode__patient__demographics__hospital_number=hospital_number
                )

            if latest:
                order_by = getattr(model, "_sort", None)

                if order_by is not None:
                    result = result_set.order_by(model._sort).last()
                else:
                    # if not order fall back to the standard object ordering
                    result = result_set.last()

                context = {
                    "latest": latest,
                    "object": result
                }
            else:
                context = dict(object_list=result_set)

            return TemplateResponse(
                request=request,
                template=get_template_name(model),
                context=context
            )

    return HttpResponseBadRequest("missing hospital number or column")
