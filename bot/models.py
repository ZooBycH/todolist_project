from django.db import models

from core.models import User


class TgUser(models.Model):
    class Meta:
        verbose_name = "Пользователь телеграм"
        verbose_name_plural = "Пользователи телеграм"

    tg_user_id = models.IntegerField(verbose_name="ID пользователя в телеграм")
    tg_chat_id = models.IntegerField(verbose_name="ID чата в телеграм")
    verification_code = models.CharField(max_length=32, verbose_name="Код для верификации")
    user = models.ForeignKey(
        User, verbose_name="Связанный пользователь приложения", on_delete=models.PROTECT, null=True
    )
