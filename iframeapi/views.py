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
    most_recent = bool(request.GET.get("mostRecent"))

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

                if most_recent:
                    result = result_set.order_by("-episode__date_of_episode").first()

            if result_set is not None:
                if most_recent:
                    context = {
                        "most_recent": most_recent,
                        "object": result
                    }
                else:
                    context=dict(object_list=result_set)

                return TemplateResponse(
                    request=request,
                    template=get_template_name(model),
                    context=context
                )

    return HttpResponseBadRequest("missing hospital number or column")
