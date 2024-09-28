from django.db import models


class BaseManagerModel(models.Manager):
    def get_queryset(self):
        return super(BaseManagerModel, self).get_queryset().filter(is_deleted=False)

    def get_publish(self, *args, **kwargs):
        return self.get_queryset().get(active=True, *args, **kwargs)

    def filter_publish(self, *args, **kwargs):
        return self.get_queryset().filter(active=True, *args, **kwargs)

    def all_publish(self):
        return self.get_queryset().filter(active=True).all()
