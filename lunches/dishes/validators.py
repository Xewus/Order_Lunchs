from django.db import models
from django.core.exceptions import ValidationError

def validate_only_one_instance(obj):
    model = obj.__class__
    if (model.objects.count() > 0 and
            obj.id != model.objects.get().id):
        raise ValidationError(
            f'Разрешена только одна модель {model.__name__}. '
            'При необходимости можно изменить существующую модель'
        )
