from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel
from user.choices import GenderChoice


# Create your models here.


class User(AbstractUser, BaseModel):
    gender = models.IntegerField(verbose_name=_('Gender'), default=GenderChoice.Unknown, choices=GenderChoice.choices)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
