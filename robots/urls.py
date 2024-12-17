from django.urls import path

from robots.views import AddNewRobotsView

urlpatterns = [
    path('add_info', AddNewRobotsView.as_view(), name='add_robots'),

]