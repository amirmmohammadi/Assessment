from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from common.managers import BaseManagerModel


# Create your models here.


class TimeStampBaseModel(models.Model):
    updated_at = models.DateTimeField(verbose_name=_('Updated at'), auto_now=True)
    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True, editable=False)

    class Meta:
        abstract = True


class BaseModel(TimeStampBaseModel):
    active = models.BooleanField(verbose_name=_('Active'), default=True)
    is_deleted = models.BooleanField(verbose_name=_('Is deleted'), default=False)
    deleted_at = models.DateTimeField(verbose_name=_('Deleted at'), null=True, blank=True)

    objects = models.Manager()
    valid_objects = BaseManagerModel()

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    class Meta:
        abstract = True
