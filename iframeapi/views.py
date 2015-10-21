"""
Views for the iframeapi OPAL Plugin
"""
from django.db import models as django_models
from django.http import HttpResponseBadRequest
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.template.response import TemplateResponse
from opal import models as opal_models
from opal.core.search.queries import get_model_from_column_name
from opal.utils import camelcase_to_underscore


def get_template_name(model):
    model_name = camelcase_to_underscore(model.__name__)
    template_name = 'iframe_templates/{0}.html'.format(model_name)
    try:
        template_name = get_template(template_name).template.name
        return dict(template=template_name)
    except TemplateDoesNotExist:
        return dict(
            template='iframe_templates/template-not-found.html',
            status=400
        )


def bad_request(request):
    column_names = []

    for model in django_models.get_models():
        if issubclass(model, (opal_models.PatientSubrecord, opal_models.EpisodeSubrecord,)):
            column_names.append(model.__name__.lower())

    return TemplateResponse(
        request=request,
        template="iframe_templates/bad_request.html",
        context=dict(column_names=column_names),
        status=400
    )


def iframe_api(request):
    # This has to be here because Django wants to make sure it's the first
    # thing to import models and gets distinctly snippish if you beat it.
    from iframeapi.models import ApiKey

    hospital_number = request.GET.get("hospitalNumber")
    record_name = request.GET.get("record")
    latest = bool(request.GET.get("latest"))

    try:
        api_key = ApiKey.objects.get(key=request.GET.get("key"))
    except ApiKey.DoesNotExist:
        return bad_request(request)

    api_key.used()

    if record_name and hospital_number:

        model = get_model_from_column_name(record_name)

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

            response_kwargs = {
                "request": request,
                "context": context
            }

            response_kwargs.update(get_template_name(model))

            return TemplateResponse(**response_kwargs)

    return bad_request(request)
