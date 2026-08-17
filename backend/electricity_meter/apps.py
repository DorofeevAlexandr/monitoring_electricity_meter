from django.apps import AppConfig


class ElectricityMeterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'electricity_meter'
    verbose_name = 'Электросчетчик'
    verbose_name_plural = 'Электросчетчики'

