from django.core.exceptions import ValidationError
from django.utils import timezone


def year_validator(value):
    """Валидация значения года произведения."""
    if not (0 < value <= timezone.now().year):
        raise ValidationError('Некорректное значение года!')
