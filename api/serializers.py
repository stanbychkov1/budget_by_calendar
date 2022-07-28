from rest_framework import serializers

from accruals.calculate_usd_amount import calc_usd_amount
from accruals.models import Payment, Accrual


class PaymentSerializer(serializers.ModelSerializer):
    accrual_id = serializers.CharField(write_only=True)
    date = serializers.DateField(required=False)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Payment
        fields = ('accrual_id', 'user', 'date',
                  'amount', 'method', 'patient', 'currency',)

    def validate(self, attrs):
        # Проверка существует ли такое начисление и принадлежит ли пользователю
        try:
            accrual = Accrual.objects.get(id=attrs.get('accrual_id'),
                                          user=attrs.get('user'),
                                          patient=attrs.get('patient'))
        except Accrual.DoesNotExist:
            raise serializers.ValidationError(
                (f'Данная запись не принаделижт пользователю'
                 f' или не существует'))
        # Если дата оплаты не передана, передается дата начисления
        if not attrs.get('date'):
            attrs['date'] = accrual.date
        return attrs

    def create(self, validated_data):
        currency = validated_data.get('currency')
        amount = validated_data.get('amount')
        date = validated_data.get('date')
        # Высчтывание суммы в долларах перед созданием экземпляра модели
        amount_USD = calc_usd_amount(currency, amount, date)
        payment = Payment(
            user=validated_data.get('user'),
            date=date,
            amount=amount,
            method=validated_data.get('method'),
            info=None,
            patient=validated_data.get('patient'),
            currency=currency,
            amount_USD=amount_USD
        )
        payment.save()

        # Обновление экхемпляра начисления: начисление оплачено и
        # связан с оплатой
        accrual = Accrual.objects.get(
            id=validated_data.get('accrual_id')
        )
        accrual.paid = True
        accrual.payment_id = payment.id
        accrual.save()
        return payment
