from django.db import models

# Create your models here.
class Country(models.Model):
    CONTINENTS = [
        ("AF", "Africa"),
        ("AN", "Antarctica"),
        ("AS", "Asia"),
        ("EU", "Europe"),
        ("NA", "North America"),
        ("OC", "Oceania"),
        ("SA", "South and Central America"),
    ]
    country_name = models.CharField(max_length=60, unique=True)
    continent = models.CharField(max_length=2, choices=CONTINENTS)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<country_name=%s, continent=%s, date_created=%s>" % (self.country_name, self.get_continent_display(), self.date_created)

class Language(models.Model):
    language = models.CharField(max_length=180)
    language_code = models.CharField(max_length=10)
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="languages",
    )

    def __str__(self):
        return "<language=%s, language_code=%s, country=%s>" % (self.language, self.language_code, self.country)
