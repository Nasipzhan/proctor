from django.db import models
from django import forms


class Test(models.Model):
    name = models.CharField(max_length=30)


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.CharField(max_length=100)


class Answer(models.Model):
    name = models.CharField(max_length=100)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    valid = models.BooleanField(default=False)
# Create your models here.


class SearchForm(forms.Form):
    search = forms.CharField()

    class Meta:
        fields = ('search')
        labels = {
            'search': ('Поиск'),
        }
