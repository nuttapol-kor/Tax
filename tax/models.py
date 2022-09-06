from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

class TaxCal(models.Model):
    salary = models.FloatField(
        verbose_name="เงินเดือน",
        validators=[MinValueValidator(0.0, "เงินเดือนต้องมีค่ามากกว่าศูนย์")]
    )
    month = models.IntegerField(
        verbose_name="จำนวนเดือนที่ได้รับเงิน",
        validators=[MinValueValidator(1, "จำนวนเดือนต้องอยู่ระหว่าง 1 ถึง 12"), MaxValueValidator(12, "จำนวนเดือนต้องอยู่ระหว่าง 1 ถึง 12")]
    )
    crypto_profit = models.FloatField(
        verbose_name="กำไรที่ได้รับจากคริปโตเคอเรนซี"
    )

    personal_discount = models.FloatField(
        verbose_name="ค่าลดหย่อนส่วนตัว",
        default= 60_000
    )
    social_security = models.FloatField(
        verbose_name="ประกันสังคม",
        validators=[MaxValueValidator(5_100, "ไม่เกิน 5,100 บาท")]
    )
    life_insurance = models.FloatField(
        verbose_name="ประกันชีวิตและประกันสะสมทรัพย์",
        validators=[MaxValueValidator(100_000, "ไม่เกิน 100,000 บาท")]
    )
    health_insurance = models.FloatField(
        verbose_name="ประกันสุขภาพ",
        validators=[MaxValueValidator(25_000, "ไม่เกิน 25,000 บาท")]
    )

    rmf_fund = models.FloatField(
        verbose_name="กองทุนรวมเพื่อการเลี้ยงชีพ (RMF)",
        validators=[MaxValueValidator(500_000, "ไม่เกิน 500,000 บาท")]
    )
    ssf_fund = models.FloatField(
        verbose_name="กองทุนรวมเพื่อการออม (SSF)",
        validators=[MaxValueValidator(200_000, "ไม่เกิน 200,000 บาท")]
    )
    pvd_fund = models.FloatField(
        verbose_name="กองทุนสำรองเลี้ยงชีพ (PVD)",
        validators=[MaxValueValidator(500_000, "ไม่เกิน 500,000 บาท")]
    )

    withholding_tax = models.FloatField(
        verbose_name="ภาษีหัก ณ ที่จ่าย"
    )

    def clean(self):
        income = (self.salary * self.month) + self.crypto_profit
        # other insurance
        if self.life_insurance + self.health_insurance > 100_000:
            raise ValidationError("ประกันอื่นๆ (รวมทุกข้อไม่เกิน 100,000 บาท)")
        # fund
        if self.rmf_fund > income * .3:
            raise ValidationError("RMF ไม่ควรเกิน 30% ของเงินได้")
        if self.ssf_fund > income * .3:
            raise ValidationError("SSF ไม่ควรเกิน 30% ของเงินได้")
        if self.pvd_fund > income * .15:
            raise ValidationError("PVD ไม่ควนเกิน 15% ของเงินได้")

        if self.withholding_tax > income:
            raise ValidationError("ภาษีหัก ณ ที่จ่ายไม่ควรเกินจำนวนเงินได้")
        
    def discount(self):
        return self.personal_discount + self.social_security + self.life_insurance + self.health_insurance + self.rmf_fund + self.ssf_fund + self.pvd_fund

    def income(self):
        return (self.salary * self.month) + self.crypto_profit

    def expenses(self):
        e = self.income() * .5
        if e > 100_000:
            e = 100_000
        return e
        