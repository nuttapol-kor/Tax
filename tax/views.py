from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import TaxForm
from .models import TaxCal

def home(request):
    return HttpResponse('<h1>Tax Home</h1>')

def income_tax_rate(income):
    if income <= 150_000:
        return (0, "0%")
    elif income <= 300_000:
        return ((income - 150_000) * .05, "5%")
    elif income <= 500_000:
        return (((income - 300_000) * .1) + 7_500, "10%")
    elif income <= 750_000:
        return (((income - 500_000) * .15) + 27_500, "15%")
    elif income <= 1_000_000:
        return (((income - 750_000) * .2) + 65_000, "20%")
    elif income <= 2_000_000:
        return (((income - 1_000_000) * .25) + 115_000, "25%")
    elif income <= 5_000_000:
        return (((income - 2_000_000) * .3) + 365_000, "30%")
    else:
        return (((income - 5_000_000) * .35) + 1_265_000, "35%")

def calculate(request):
    if request.method == "POST":
        form = TaxForm(request.POST)
        if form.is_valid():
            obj = TaxCal(**form.cleaned_data)
            # income = (form.cleaned_data['salary'] * form.cleaned_data['month']) + form.cleaned_data['crypto_profit']
            # expenses = income * .5
            # if expenses > 100_000:
            #     expenses = 100_000
            # discount = form.cleaned_data['personal_discount'] + form.cleaned_data['social_security'] + form.cleaned_data['life_insurance'] + form.cleaned_data['health_insurance'] + form.cleaned_data['rmf_fund'] + form.cleaned_data['ssf_fund'] + form.cleaned_data['pvd_fund']
            net_income = obj.income() - obj.expenses() - obj.discount()
            print(net_income)
            tax_rate, rate = income_tax_rate(net_income)
            print(tax_rate)
            tax = form.cleaned_data['withholding_tax'] - tax_rate
            result = ""
            if tax < 0:
                result = (f"คุณต้องเสียภาษีเพิ่มอีก {abs(tax)} บาท")
            else:
                result = (f"คุณจะได้รับคืนภาษีที่จ่ายเกินไว้ {tax} บาท")
            context = {
                "income": obj.income(),
                "expenses": obj.expenses(),
                "discount": obj.discount(),
                "net_income": net_income,
                "tax_rate": tax_rate,
                "rate": rate,
                "withholding_tax": form.cleaned_data['withholding_tax'],
                "result": result
            }
            return render(request, "tax/result.html", context)
            
    else:
        form = TaxForm()
    return render(request, "tax/calculate.html", {"form":form})