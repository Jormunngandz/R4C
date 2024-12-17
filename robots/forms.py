from django import forms


class AddRobotForm(forms.Form):
    json_data = forms.FileField()
