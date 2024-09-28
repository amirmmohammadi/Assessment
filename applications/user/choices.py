from django.db import models
from django.utils.translation import gettext_lazy as _


class GenderChoice(models.IntegerChoices):
    Male = 1, _("Male")
    Female = 2, _("Female")
    Unknown = 0, _("Unknown")
