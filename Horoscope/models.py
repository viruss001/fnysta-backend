from django.db import models

# Create your models here.
class Horo(models.Model):
    sign = models.CharField(max_length=100)
    horoscope = models.TextField()
    date = models.DateField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return f"{self.sign} - {self.date}"
    

class WeekHoro(models.Model):
    zodiac_sign = models.CharField(max_length=100)
    week_start = models.DateField()  # first day of the week
    week_end = models.DateField()    # last day of the week
    horoscope = models.JSONField()   # store structured JSON for weekly horoscope
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("zodiac_sign", "week_start")  # only one entry per sign per week
        ordering = ["-week_start"]

    def __str__(self):
        return f"{self.zodiac_sign} ({self.week_start} to {self.week_end})"

class MonthHoro(models.Model):
    zodiac_sign = models.CharField(max_length=100)
    month_start = models.DateField()  # first day of month
    month_end = models.DateField()    # last day of month
    horoscope = models.JSONField()    # JSON structure with sentence arrays
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("zodiac_sign", "month_start")

    def __str__(self):
        return f"{self.zodiac_sign} ({self.month_start} to {self.month_end})"
    

class YearHoro(models.Model):
    zodiac_sign = models.CharField(max_length=100)
    year = models.IntegerField()
    horoscope = models.JSONField()    # JSON with arrays of sentences
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("zodiac_sign", "year")  # one entry per zodiac sign per year

    def __str__(self):
        return f"{self.zodiac_sign} ({self.year})"