import datetime as dt
from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from backend.electricity_meter.models import ElectroCounters

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Электросчетчики"

@admin.register(ElectroCounters)
class ElectroCountersAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    fields = ('number', 'client_name', 'address', 'energy_indic', 'transformation_coefficient', 'energy')
    list_display = ('number', 'client_name', 'address', 'energy_indic', 'transformation_coefficient', 'energy')
    readonly_fields = ['energy_indic', 'energy']
    # Фильтрация в списке
    # list_filter = ('name', 'format',)
    # Поиск по полям
    search_fields = ('client_name', )
    save_on_top = True
