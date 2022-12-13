from django.db import models
from goals.models.mixin import DatesModelMixin

from goals.models.goal import Goal


class GoalComment(DatesModelMixin):

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    text = models.TextField(verbose_name='Текст')
    goal = models.ForeignKey(
        Goal,
        verbose_name='Цель',
        related_name='comments',
        on_delete=models.PROTECT
    )
    user = models.ForeignKey(
        'core.User',
        verbose_name='Автор',
        related_name='comments',
        on_delete=models.PROTECT
    )
