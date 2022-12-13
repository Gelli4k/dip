from django.db import models
from goals.models.mixin import DatesModelMixin

from goals.models.category import GoalCategory


class Goal(DatesModelMixin):

    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'

    class Status(models.IntegerChoices):
        to_do = 1, 'К выполнению'
        in_progress = 2, 'В процессе'
        done = 3, 'Выполнено'
        archived = 4, 'Архив'

    class Priority(models.IntegerChoices):
        low = 1, 'Низкий'
        medium = 2, 'Средний'
        high = 3, 'Высокий'
        critical = 4, 'Критический'

    title = models.CharField(
        verbose_name='Название',
        max_length=255
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    status = models.PositiveSmallIntegerField(
        verbose_name='Статус',
        choices=Status.choices,
        default=Status.to_do)
    priority = models.PositiveSmallIntegerField(
        verbose_name='Приоритет',
        choices=Priority.choices,
        default=Priority.medium
    )
    due_date = models.DateField(
        verbose_name='Дата выполнения'
    )
    user = models.ForeignKey(
        'core.User',
        verbose_name='Автор',
        on_delete=models.PROTECT
    )
    category = models.ForeignKey(
        GoalCategory,
        verbose_name='Категория',
        related_name='goals',
        on_delete=models.CASCADE
    )
    