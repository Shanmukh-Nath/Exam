from django.db import models
from django.contrib.auth.models import User
from questions.question_models import Question_DB
from questions.questionpaper_models import Question_Paper
from django.core import serializers


class Gallery(models.Model):
    tit=models.CharField(max_length=50)
    img=models.ImageField(upload_to='gallery')
    des=models.CharField(max_length=500)
    def __str__(self):
        return self.tit


class Contact(models.Model):
    name=models.CharField(max_length=200)
    roll_no=models.CharField(max_length=200)
    mob=models.CharField(max_length=200)
    mail=models.CharField(max_length=200)
    type=models.CharField(max_length=200)
    def __str__(self):
        return self.name


class StudentInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, blank=True)
    stream = models.CharField(max_length=50, blank=True)
    picture = models.ImageField(upload_to = 'student_profile_pics', blank=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = 'Student Info'

class Stu_Question(Question_DB):
    professor = None
    student = models.ForeignKey(User, limit_choices_to={'groups__name': "Student"}, on_delete=models.CASCADE, null=True)
    choice = models.CharField(max_length=3, default="E")

    def __str__(self):
        return str(self.student.username) + " "+ str(self.qno) +"-Stu_QuestionDB"

class Tag_score(models.Model):
    student = models.ForeignKey(User,on_delete=models.CASCADE)
    python = models.IntegerField(default=0)
    web = models.IntegerField(default=0)
    ml = models.IntegerField(default=0)
    dsa = models.IntegerField(default=0)
    dbms = models.IntegerField(default=0)

class StuExam_DB(models.Model):
    examname = models.CharField(max_length=100)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    qpaper = models.ForeignKey(Question_Paper, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Stu_Question)
    completed = models.IntegerField(default=0)
    score = models.FloatField(default=0)
    random_questions = models.ManyToManyField(Question_DB,related_name='random_questions_set')

    def __str__(self):
        return str(self.student.username) +" " + str(self.examname) + " " + str(self.qpaper.qPaperTitle) + "-StuExam_DB"


class StuResults_DB(models.Model):
    student = models.ForeignKey(User, limit_choices_to={'groups__name': "Student"}, on_delete=models.CASCADE, null=True)
    exams = models.ManyToManyField(StuExam_DB)

    def __str__(self):
        return str(self.student.username) +" -StuResults_DB"