from django.core.exceptions import ValidationError


def validate_name_me(name):

    if name.lower() == "me":
        raise ValidationError('Имя не должно быть me')
