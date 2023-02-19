from django.core.exceptions import ValidationError
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from api_yamdb.settings import DEFAULT_FROM_EMAIL


def validate_name_me(name):
    if name.lower() == "me":
        raise ValidationError('Имя не должно быть me')


def send_verifiy_code(self, email, token, user_name):
    header = 'Ваш код подтверждения'
    message = (
        f'Приветствуем {user_name} путник 10 спринта! \n',
        f'Держи свой код: {token}'
    )
    try:
        send_mail(header, message, DEFAULT_FROM_EMAIL, email)
    except BadHeaderError:
        return HttpResponse()
