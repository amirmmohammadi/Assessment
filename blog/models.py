import datetime
import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel, TimeStampBaseModel


# Create your models here.


class Content(BaseModel):
    id = models.UUIDField(verbose_name=_('ID'), primary_key=True, default=uuid.uuid4, editable=False)

    owner = models.ForeignKey(to='user.User', on_delete=models.CASCADE, verbose_name=_('Owner'))
    title = models.CharField(verbose_name=_('Title'), max_length=255)
    body = models.TextField(verbose_name=_('Body'))

    score_average = models.FloatField(verbose_name=_('Score Average'), default=0)
    score_count = models.PositiveIntegerField(verbose_name=_('Score Count'), default=0)
    calculated_to = models.DateTimeField(verbose_name=_('Calculated To'), auto_now_add=True)

    class Meta:
        verbose_name = _('Content')
        verbose_name_plural = _('Contents')

    def __str__(self):
        return self.title

    def detect_spam_scores(self):
        now = timezone.now()

        time_from_payload = 1  # hour
        time_from_slice = 10  # minutes

        time_from = now - datetime.timedelta(hours=time_from_payload)
        last_content_scores = ContentScore.objects.filter(created_at__gte=time_from, content=self)

        dict_me = {}

        for i in range(0, 60 * time_from_payload, time_from_slice):
            time_slice_start = time_from + datetime.timedelta(minutes=i)
            time_slice_end = time_slice_start + datetime.timedelta(minutes=time_from_slice)

            time_slice = last_content_scores.filter(created_at__gte=time_slice_start, created_at__lt=time_slice_end)
            average = time_slice.aggregate(Avg('score'))['score__avg'] or 0.0

            dict_me[average] = (time_slice_start, time_slice_end)

        spam_rate_threshold = 20 / 100
        average_overall = sum(dict_me.keys()) / len(dict_me) if dict_me else 0

        for average, (start_time, end_time) in dict_me.items():
            if average > 0 and (average / average_overall) > spam_rate_threshold:
                ContentScore.objects.filter(created_at__gte=start_time, created_at__lt=end_time).update(is_spam=True)


class ContentScore(TimeStampBaseModel):
    owner = models.ForeignKey(to='user.User', on_delete=models.CASCADE, verbose_name=_('User'))
    content = models.ForeignKey(Content, on_delete=models.CASCADE, verbose_name=_('Content'))
    score = models.PositiveIntegerField(verbose_name=_('Score'), validators=[MinValueValidator(1), MaxValueValidator(5)])
    is_spam = models.BooleanField(verbose_name=_('Is Spam'), default=False)

    class Meta:
        ordering = ['created_at',]
        verbose_name = _('Content Score')
        verbose_name_plural = _('Content Scores')
        unique_together = (('content', 'owner'),)
