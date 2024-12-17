from django.urls import path

from robots.views import GetLastWeekRobotsStatistic

urlpatterns = [
    path('last-week-robots', GetLastWeekRobotsStatistic.as_view(), name='last_week'),
]