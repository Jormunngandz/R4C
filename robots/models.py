import datetime
from typing import List, Union, Tuple

from django.db import models
from django.db.models import Count, QuerySet

from django.utils import timezone


class Robot(models.Model):
    serial = models.CharField(max_length=5, blank=False, null=False)
    model = models.CharField(max_length=2, blank=False, null=False)
    version = models.CharField(max_length=2, blank=False, null=False)
    created = models.DateTimeField(blank=False, null=False)

    @classmethod
    def get_last_week_robots_statistic(cls) -> Union[List, None]:
        """Формируем запрос с роботами за последнюю неделю.
            Группируем роботов по модели и версии, считаем их количество для каждой серии.
            Формируем и возвращаем список содержащий отфильтрованные списки для каждой модели"""
        seven_day_before: datetime.datetime = (timezone.now().date() - datetime.timedelta(days=7))
        last_week_robots: QuerySet[Robot] = (cls.objects.filter(created__gte=seven_day_before)
                                             .only('model', 'version')
                                             .values('model', 'version')
                                             .annotate(total=Count("model")))

        if last_week_robots:
            # Получаем множество моделей собранных за неделю
            last_week_robot_models: set[Robot] = set(last_week_robots.values_list("model", flat=True))
            # Формируем список для каждой модели и добавляем в общий список
            filtered_by_model: List[Tuple] = [last_week_robots.filter(model=robot_model)
                                              .values_list('model', 'version', 'total')
                                              for robot_model in last_week_robot_models]
            return filtered_by_model
