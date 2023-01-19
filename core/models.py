from django.contrib.auth.models import AbstractUser

"""Создаем свою модель для пользователя, наследуем ее от AbstractUser"""


class User(AbstractUser):
    pass
