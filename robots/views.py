import json
from datetime import datetime

from typing import Dict, List

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.timezone import make_aware
from django.views import View


from .forms import AddRobotForm
from .models import Robot


class AddNewRobotsView(View):
    @classmethod
    def post(cls, request) -> HttpResponse:
        form: AddRobotForm = AddRobotForm(files=request.FILES)
        if form.is_valid():
            try:
                data: Dict = json.loads(request.FILES['json_data'].read())
                new_robots: List[Robot] = [Robot(serial=''.join((el.get('model', ''), el.get('version', ''))),
                                                 model=el.get('model', ''),
                                                 version=el.get('version', ''),
                                                 created=make_aware(datetime.fromisoformat(el.get('created', ''))))
                                           for el in data]
                for new_robot in new_robots:
                    new_robot.full_clean()
            except ValidationError as e:
                result = f'Invalid JSON data ({e})'
                status = 400
            except json.JSONDecodeError:
                result = 'Invalid JSON data'
                status = 400
            else:
                Robot.objects.bulk_create(new_robots)
                result = 'Robots created'
                status = 200
            return render(request, "robots/add_new_robots.html", context={"form": form,
                                                                          "result": result}, status=status)
        return render(request, "robots/add_new_robots.html", context={"form": form}, status=400)

    @classmethod
    def get(cls, request):
        return render(request, "robots/add_new_robots.html", context={"form": AddRobotForm})

