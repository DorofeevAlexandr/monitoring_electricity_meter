from django.urls import path, re_path, register_converter
from electricity_meter import views


urlpatterns = [
    path('', views.index, name='home'),
    path('electricity', views.electro_counters_value,
         name='electro_counters'),
    path('electricity_meter', views.electro_counters_statistics_for_the_day,
         name='electro_counters_statistics_for_the_day'),
    path('electricity_meter_month', views.electro_counters_statistics_for_the_month,
         name='electro_counters_statistics_for_the_month'),
    path('reports_month', views.reports_for_the_month,
         name='reports'),
    path('tuning', views.tuning, name='tuning'),
]
