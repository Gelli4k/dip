from django.db import models

from goals.models.boards import Board
from goals.models.mixin import DatesModelMixin


class GoalCategory(DatesModelMixin):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    board = models.ForeignKey(
        Board,
        verbose_name='Доска',
        on_delete=models.PROTECT,
        related_name='categories',
        null=True,
    )
    title = models.CharField(
        verbose_name='Название',
        max_length=255
    )
    user = models.ForeignKey(
        'core.User',
        verbose_name='Автор',
        on_delete=models.PROTECT
    )
    is_deleted = models.BooleanField(
        verbose_name='Удалена',
        default=False
    )
