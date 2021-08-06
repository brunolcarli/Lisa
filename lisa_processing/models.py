from django.db import models


class Term(models.Model):
    """
    Stores a term (token) and metadata about it.
    """
    text = models.CharField(max_length=50, null=False, blank=False, unique=True)
    part_of_speech = models.CharField(max_length=12, null=True, blank=True)
    lemma = models.CharField(max_length=30, null=True, blank=True)
    root = models.CharField(max_length=30, null=True, blank=True)
    polarity = models.IntegerField(default=0)
    meaning = models.BinaryField(null=True)
    is_currency = models.BooleanField(null=True)
    is_punct = models.BooleanField(null=True)
    is_stop = models.BooleanField(null=True)
    is_offensive = models.BooleanField(null=True)
    is_digit = models.BooleanField(null=True)
