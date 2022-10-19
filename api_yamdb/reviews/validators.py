from django.forms import ValidationError
from django.utils import timezone


def year_validator(pub_year):
    if timezone.now().year < pub_year:
        raise ValidationError(
            "Год публикации не может быть позднее текущего года."
        )
    return pub_year


def score_validator(score):
    if not (1 <= score <= 10 and isinstance(score, int)):
        raise ValidationError(
            "Оценкой может быть целое число в диапазоне от 1 до 10."
        )
    return score


def username_validator(username):
    """
    Validates that username not equal to sting 'me'
    """
    if username.lower() == 'me':
        raise ValidationError(
            f"Недопустимое имя пользователя: {username}."
        )
    return username
