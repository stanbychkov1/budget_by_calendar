from . import models


# def add_payment_to_accrual(instance, accruals):
#     models.Accrual.payment.through.objects.bulk_create(
#         [
#             models.Accrual.payment.through(
#                 payment=instance,
#                 accrual=accrual,
#             ) for accrual in accruals
#         ],
#     )
#     for accrual in accruals:
#         accrual.paid = True
#         accrual.save()
