from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms

class Question_DB(models.Model):
    professor = models.ForeignKey(User, limit_choices_to={'groups__name': "Professor"}, on_delete=models.CASCADE,
                                  null=True,default=22)
    qno = models.AutoField(primary_key=True)
    question = models.CharField(max_length=100000000)
    optionA = models.CharField(max_length=100)
    optionB = models.CharField(max_length=100)
    optionC = models.CharField(max_length=100)
    optionD = models.CharField(max_length=100)
    answer = models.CharField(max_length=200)
    max_marks = models.IntegerField(default=1)
    programming_code = models.TextField(blank=True, null=True)
    tag=models.CharField(default='python',max_length=300)

    def __str__(self):
        return f'Question No.{self.qno}: {self.question} \n\tOptions: \n\tA. {self.optionA} \n\tB. {self.optionB} \n\tC. {self.optionC} \n\tD. {self.optionD} \n\tProgramming Code: \n\t{self.programming_code} \n\tTag: \n\t{self.tag}'


class RandomQuestion(models.Model):
    student = models.ForeignKey(User, limit_choices_to={'groups__name': "Student"}, on_delete=models.CASCADE)
    question = models.ForeignKey(Question_DB, on_delete=models.CASCADE)
    order = models.IntegerField()
    choice = models.CharField(max_length=50,default='E')


class QForm(ModelForm):
    class Meta:
        model = Question_DB
        fields = '__all__'
        exclude = ['qno', 'professor']
        widgets = {
            'question': forms.TextInput(attrs = {'class':'form-control'}),
            'optionA': forms.TextInput(attrs = {'class':'form-control'}),
            'optionB': forms.TextInput(attrs = {'class':'form-control'}),
            'optionC': forms.TextInput(attrs = {'class':'form-control'}),
            'optionD': forms.TextInput(attrs = {'class':'form-control'}),
            'answer': forms.TextInput(attrs = {'class':'form-control'}),
            'max_marks': forms.NumberInput(attrs = {'class':'form-control'}),
        }