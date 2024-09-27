import datetime

from celery import shared_task
from django.db.models import Avg
from django.utils import timezone

from .models import ContentScore, Content


@shared_task(name='update_all_content_average_scores', run_every='hour')
def update_all_content_average_scores():
    """To find votes registered as spam. We divided the averages recorded for one hour into 6 parts.

If the average scores change by more than 20% in this 10-minute period, we consider all the votes in that hour as spam.

We do not consider the number of votes and the increase in the number of votes as spam because these votes may be real. We only consider sudden changes in the average as spam"""
    updates = []
    now = timezone.now()

    contents = Content.valid_objects.all()

    for content in contents:
        content.detect_spam_scores()

        new_average_score = ContentScore.objects.filter(
            content=content, is_spam=False, created_at__gte=content.calculated_to
        ).aggregate(Avg('score'))['score__avg'] or 0.0

        new_score_count = ContentScore.objects.filter(
            content=content, is_spam=False, created_at__gte=content.calculated_to).count()

        updated_score_count = content.score_count + new_score_count

        if updated_score_count > 0:
            updated_average_score = ((content.score_average * content.score_count) + (
                    new_average_score * new_score_count)) / updated_score_count

        else:
            updated_average_score = 0.0

        updates.append(Content(
            id=content.id,
            score_average=updated_average_score,
            score_count=updated_score_count,
            calculated_to=now
        ))

    if updates:
        Content.objects.bulk_update(updates, ['score_average', 'score_count', 'calculated_to'])

