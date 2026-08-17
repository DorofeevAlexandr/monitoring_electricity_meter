from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Этот параметр указывает Django, что этот класс не является представлением таблицы
        abstract = True


class UUIDMixin(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.AutoField(primary_key=True, editable=False)

    class Meta:
        abstract = True


class ElectroCounters(UUIDMixin, TimeStampedMixin):
    number = models.IntegerField(verbose_name='Номер счетчика', default=100, unique=True,
                                 validators=[MinValueValidator(0), MaxValueValidator(255)])
    client_name = models.CharField(verbose_name='Наименование клиента', max_length=40, unique=True)
    address = models.IntegerField(verbose_name='Сетевой адрес регистра', default=100, unique=True,
                                  validators=[MinValueValidator(0), MaxValueValidator(255)])
    transformation_coefficient = models.IntegerField(verbose_name='Коэф. трансформации', default=1,
                                                     validators=[MinValueValidator(0)])
    energy_indic = models.BigIntegerField(verbose_name='Значение эн. на счетчике', default=0, validators=[MinValueValidator(0)])
    energy = models.BigIntegerField(verbose_name='Значение энергии', default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.number} - {self.client_name}'

    class Meta:
        db_table = 'electro_counters'
        verbose_name = 'Электросчетчик'
        verbose_name_plural = 'Электросчетчики'
