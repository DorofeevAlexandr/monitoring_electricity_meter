import datetime as dt
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible
from django.db import models


class ReadDateForElectroCounters(forms.Form):
    day = forms.DateField(initial=dt.date.today,
                          label="Выберите дату",
                          required=True,
                          widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
                          input_formats=["%Y-%m-%d"]
                          )


class ReadMonthForElectroCounters(forms.Form):
    start_day = forms.DateField(initial=dt.date.today,
                          label="Выберите месяц",
                          required=True,
                          widget=forms.DateInput(format="%Y-%m", attrs={"type": "month"}),
                          input_formats=["%Y-%m"]
                          )
