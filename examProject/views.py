from django.shortcuts import render, get_object_or_404
from student.models import StuExam_DB,Tag_score
from questions.question_models import RandomQuestion,Question_DB
from questions.questionpaper_models import Question_DB

def index(request):
    #cal()
    tag_score()
    return render(request,'homepage.html')


def cal():
    stud_ids = RandomQuestion.objects.values_list('student_id',flat=True).distinct()

    for student in stud_ids:

        answered = RandomQuestion.objects.filter(student_id=student)
        score=0
        for answer in answered:
            question = Question_DB.objects.get(qno=answer.question.qno)
            if answer.choice.lower() == question.answer.lower() or answer.choice == question.answer:
                score+=question.max_marks


        if StuExam_DB.objects.filter(student_id=student).exists() :
            stu_db = get_object_or_404(StuExam_DB,student_id=student)
            stu_db.score = score
            stu_db.save()


def tag_score():
    stud_ids = RandomQuestion.objects.values_list('student_id', flat=True).distinct()

    for student in stud_ids:

        answered = RandomQuestion.objects.filter(student_id=student)
        python = 0
        web = 0
        ml = 0
        dsa = 0
        dbms = 0
        for answer in answered:
            question = Question_DB.objects.get(qno=answer.question.qno)
            if answer.choice.lower() == question.answer.lower() or answer.choice == question.answer:
                if question.tag.lower() == 'python':
                    python+=1
                elif question.tag.lower() == 'ml':
                    ml+=1
                elif question.tag.lower() == 'dsa':
                    dsa+=1
                elif question.tag.lower() == 'dbms':
                    dbms+=1
                else:
                    web+=1

        stu = Tag_score.objects.get_or_create(student_id=student)[0]
        stu.python = python
        stu.ml = ml
        stu.dbms = dbms
        stu.dsa = dsa
        stu.web = web
        stu.save()