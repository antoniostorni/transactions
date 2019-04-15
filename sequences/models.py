from django.db import models

# Create your models here.


class Sequence(models.Model):

    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):

    date = models.DateField()
    description = models.CharField(max_length=200)
    amount = models.FloatField()
    sequence = models.ForeignKey(Sequence, related_name="transactions", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.description
