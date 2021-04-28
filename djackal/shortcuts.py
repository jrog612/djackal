from django.apps import apps
from django.db.models import Q
from django.shortcuts import _get_queryset

from djackal.exceptions import NotFound


def get_object_or_None(klass, *args, **kwargs):
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None


def get_object_or(klass, this=None, *args, **kwargs):
    return get_object_or_None(klass, *args, **kwargs) or this


def get_object_or_404(model, **fields):
    obj = get_object_or_None(model, **fields)
    if obj is None:
        raise NotFound(model, fields)
    return obj


def model_update(instance, **fields):
    for key, value in fields.items():
        setattr(instance, key, value)

    instance.save()
    return instance


def get_model(*args, **kwargs):
    return apps.get_model(*args, **kwargs)


def gen_q(key, *filter_keywords):
    q_object = Q()
    for q in filter_keywords:
        q_object |= Q(**{q: key})
    return q_object
