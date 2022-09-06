from django import forms
from .models import TaxCal

class TaxForm(forms.ModelForm):

    class Meta:
        model = TaxCal
        exclude = ['personal_discount']

    # def clean_salary(self, *args, **kwargs):
    #     salary = self.cleaned_data.get("salary")
    #     if salary <= 0:
    #         raise forms.ValidationError("เงินเดือนต้องมากกว่า 0")
    #     return salary
