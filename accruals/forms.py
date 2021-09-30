import datetime

from django import forms


class CalendarDateForm(forms.Form):
    start_date = forms.DateField(widget=forms.SelectDateWidget)
    end_date = forms.DateField(widget=forms.SelectDateWidget)

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')

        if start_date < datetime.date(2021, 9, 1):
            self.errors['start_date'] = 'Дата должна быть не меньше' \
                                        ' 1 сентября 2021 года'
        return start_date

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        if end_date > datetime.date.today() + + datetime.timedelta(days=1):
            self.errors['end_date'] = 'Дата должна быть не больше' \
                                      ' следующего дня'
        return end_date
