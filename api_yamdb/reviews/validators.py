'''Custom model field validators'''
from django.forms import ValidationError
from django.utils import timezone


def year_validator(value):
    if timezone.now().year < value:
        raise ValidationError(
            f"Год публикации не может быть позднее текущего года."
        )
