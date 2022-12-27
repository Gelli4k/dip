from django.core.validators import MinLengthValidator
from django.db import models
from django.core.management.utils import get_random_string


class TgUser(models.Model):
    tg_chat_id = models.BigIntegerField()
    tg_user_ud = models.BigIntegerField(unique=True)
    tg_username = models.CharField(max_length=30, validators=[MinLengthValidator(5)])
    user = models.ForeignKey('core.User', null=True, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=10, unique=True)

    def generate_verification_code(self) -> str:
        code = get_random_string(10)
        self.verification_code = code
        self.save()
        return code
