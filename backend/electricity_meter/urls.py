from django.urls import path, re_path, register_converter
from backend.electricity_meter import views


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
    path('open_pdf_file_view/<path:filename>/', views.open_pdf_file_view, name='open_pdf_file_view'),
    path('download_statement/<path:statement_date>/', views.download_statement, name='download_statement'),
    path('download_invoice/<path:invoice_date>/', views.download_invoice, name='download_invoice'),
]
