import datetime
import uuid as uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum

User = get_user_model()


class Accrual(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='accruals')
    date = models.DateField(db_index=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    payment = models.OneToOneField(to='Payment', related_name='accruals',
                                   on_delete=models.SET_NULL,
                                   blank=True, null=True)
    info = models.CharField(max_length=200, blank=True, null=True)
    paid = models.BooleanField(default=False)
    patient = models.ForeignKey(to='Patient', on_delete=models.CASCADE,
                                related_name='accruals')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, blank=True,
                            unique=False)

    def __str__(self):
        return f'Сессия с {self.patient.name} от {self.date}' \
               f' на сумму {self.amount}'

    @property
    def current_amount(self):
        amount = Accrual.objects.filter(
            user=self.user_id
        ).aggregate(Sum('amount'))
        return amount['amount__sum']

    @property
    def month_amount(self):
        month = datetime.datetime.now()
        amount = Accrual.objects.filter(
            user=self.user_id,
            date__month=month.strftime('%m')
        ).aggregate(Sum('amount'))
        return amount['amount__sum']


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='payments')
    date = models.DateField(db_index=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    method = models.ForeignKey(to='Method', on_delete=models.DO_NOTHING,
                               related_name='payments')
    info = models.CharField(max_length=200, blank=True, null=True)
    patient = models.ForeignKey(to='Patient', on_delete=models.CASCADE,
                                related_name='payments')

    def __str__(self):
        return f'Оплата от {self.patient.name} от {self.date}' \
               f' на сумму {self.amount}'

    @property
    def current_amount(self):
        amount = Payment.objects.filter(
            user=self.user
        ).aggregate(Sum('amount'))
        return amount['amount__sum']

    @property
    def month_amount(self):
        month = datetime.datetime.now()
        amount = Payment.objects.filter(
            user=self.user_id,
            date__month=month.strftime('%m')
        ).aggregate(Sum('amount'))
        return amount['amount__sum']


class Method(models.Model):
    name = models.CharField(max_length=25)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,
                             related_name='methods')

    def __str__(self):
        return self.name


class Patient(models.Model):
    name = models.CharField(max_length=20)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,
                             related_name='patients')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'Клиент {self.name}'
