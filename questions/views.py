import random

from django.db.models import Window, F
from django.db.models.functions import RowNumber
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.models import Group
from student.models import *
from django.utils import timezone
from student.models import StuExam_DB,StuResults_DB
from questions.questionpaper_models import QPForm
from questions.question_models import QForm,RandomQuestion
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from . import models
from django.shortcuts import render
from django.utils import timezone
from random import sample




def generate_paper(request,id):
    student = request.user
    if request.method == 'GET':
        exam_id = id
        exam = Exam_Model.objects.get(id=exam_id)
        qpaper = exam.question_paper
        prof_id = qpaper.professor
        ques1 = Question_DB.objects.exclude(professor_id=prof_id)
        tags = ques1.values('tag').distinct()

        print(tags.values('tag'))
        ques = []
        '''for tag in tags:
            length = len(Question_DB.objects.filter(tag=tag['tag']).annotate(row_num=Window(expression=RowNumber())).order_by('qno'))
            x = random.randint(1, length-6)
            y = x + 20
            que = Question_DB.objects.filter(tag=tag['tag']).annotate(row_num=Window(expression=RowNumber())).order_by(
                'qno')[x:y]
            if not que in ques:
                ques += que'''
        length = len(Question_DB.objects.all())
        print(length)
        for i in range(1, length):
            x = random.randint(1, length - 6)
            y = x + 15
            que = Question_DB.objects.all().order_by('qno')[x:y]
            if not que in ques:
                ques+=que
            if len(que):
                break

        random.shuffle(ques)

        # Create instances of RandomQuestion for each randomly generated question
        for i, q in enumerate(ques):
            rq = RandomQuestion(student=student, question=q, order=i)
            rq.save()

        return ques




def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

@login_required(login_url='faculty-login')
def view_exams_prof(request):
    prof = request.user
    prof_user = User.objects.get(username=prof)
    permissions = False
    if prof:
        permissions = has_group(prof,"Professor")
    if permissions:
        new_Form = ExamForm(prof_user)
        if request.method == 'POST' and permissions:
            form = ExamForm(prof_user,request.POST)
            if form.is_valid():
                exam = form.save(commit=False)
                exam.professor = prof
                exam.save()
                form.save_m2m()
                return redirect('view_exams')

        exams = Exam_Model.objects.filter(professor=prof)
        return render(request, 'exam/mainexam.html', {
            'exams': exams, 'examform': new_Form, 'prof': prof,
        })
    else:
        return redirect('view_exams_student')

@login_required(login_url='faculty-login')
def add_question_paper(request):
    prof = request.user
    prof_user = User.objects.get(username=prof)
    permissions = False
    if prof:
        permissions = has_group(prof,"Professor")
    if permissions:
        new_Form = QPForm(prof_user)
        if request.method == 'POST' and permissions:
            form = QPForm(prof_user,request.POST)
            if form.is_valid():
                exam = form.save(commit=False)
                exam.professor = prof_user
                exam.save()
                form.save_m2m()
                return redirect('faculty-add_question_paper')

        exams = Exam_Model.objects.filter(professor=prof)
        return render(request, 'exam/addquestionpaper.html', {
            'exams': exams, 'examform': new_Form, 'prof': prof,
        })
    else:
        return redirect('view_exams_student')

@login_required(login_url='faculty-login')
def add_questions(request):
    prof = request.user
    prof_user = User.objects.get(username=prof)
    permissions = False
    if prof:
        permissions = has_group(prof,"Professor")
    if permissions:
        new_Form = QForm()
        if request.method == 'POST' and permissions:
            form = QForm(request.POST)
            if form.is_valid():
                exam = form.save(commit=False)
                exam.professor = prof_user
                exam.save()
                form.save_m2m()
                return redirect('faculty-addquestions')

        exams = Exam_Model.objects.filter(professor=prof)
        return render(request, 'exam/addquestions.html', {
            'exams': exams, 'examform': new_Form, 'prof': prof,
        })
    else:
        return redirect('view_exams_student')

@login_required(login_url='faculty-login')
def view_previousexams_prof(request):
    prof = request.user
    student = 0
    exams = Exam_Model.objects.filter(professor=prof)
    return render(request, 'exam/previousexam.html', {
        'exams': exams,'prof': prof
    })

@login_required(login_url='login')
def student_view_previous(request):
    exams = Exam_Model.objects.all()
    list_of_completed = []
    list_un = []
    for exam in exams:
        if StuExam_DB.objects.filter(examname=exam.name ,student=request.user).exists():
            if StuExam_DB.objects.get(examname=exam.name,student=request.user).completed == 1:
                list_of_completed.append(exam)
        else:
            list_un.append(exam)

    return render(request,'exam/previousstudent.html',{
        'exams':list_un,
        'completed':list_of_completed
    })

@login_required(login_url='faculty-login')
def view_students_prof(request):
    students = User.objects.filter(groups__name = "Student")
    student_name = []
    student_completed = []
    count = 0
    dicts = {}
    examn = Exam_Model.objects.filter(professor=request.user)
    for student in students:
        student_name.append(student.username)
        count = 0
        for exam in examn:
            if StuExam_DB.objects.filter(student=student,examname=exam.name,completed=1).exists():
                count += 1
            else:
                count += 0
        student_completed.append(count)
    i = 0
    for x in student_name:
        dicts[x] = student_completed[i]
        i+=1
    return render(request, 'exam/viewstudents.html', {
        'students':dicts
    })

@login_required(login_url='faculty-login')
def view_results_prof(request):
    students = User.objects.filter(groups__name = "Student")
    dicts = {}
    prof = request.user
    professor = User.objects.get(username=prof.username)
    examn = Exam_Model.objects.filter(professor=professor)
    for exam in examn:
        if StuExam_DB.objects.filter(examname=exam.name,completed=1).exists():
            students_filter = StuExam_DB.objects.filter(examname=exam.name,completed=1)
            for student in students_filter:
                key = str(student.student) + " " + str(student.examname) + " " + str(student.qpaper.qPaperTitle)
                dicts[key] = student.score
    return render(request, 'exam/resultsstudent.html', {
        'students':dicts
    })

@login_required(login_url='login')
def view_exams_student(request):
    exams = Exam_Model.objects.all()
    list_of_completed = []
    list_un = []
    for exam in exams:
        if StuExam_DB.objects.filter(examname=exam.name ,student=request.user).exists():
            if StuExam_DB.objects.get(examname=exam.name,student=request.user).completed == 1:
                list_of_completed.append(exam)
        else:
            list_un.append(exam)

    return render(request,'exam/mainexamstudent.html',{
        'exams':list_un,
        'completed':list_of_completed
    })

@login_required(login_url='login')
def view_students_attendance(request):
    exams = Exam_Model.objects.all()
    list_of_completed = []
    list_un = []
    for exam in exams:
        if StuExam_DB.objects.filter(examname=exam.name ,student=request.user).exists():
            if StuExam_DB.objects.get(examname=exam.name,student=request.user).completed == 1:
                list_of_completed.append(exam)
        else:
            list_un.append(exam)

    return render(request,'exam/attendance.html',{
        'exams':list_un,
        'completed':list_of_completed
    })

def convert(seconds):
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    min += hour*60
    return "%02d:%02d" % (min, sec)

@login_required(login_url='login')
def appear_exam(request, id):
    student = request.user
    if request.method == 'GET':
        exam = Exam_Model.objects.get(pk=id)
        time_delta = exam.end_time - exam.start_time
        time = convert(time_delta.seconds)
        time = time.split(":")
        mins = time[0]
        secs = time[1]
        '''ques1 = exam.question_paper.questions.all()
        tags = ques1.values('tag').distinct()
        print(tags.values('tag'))
        ques=[]
        for tag in tags:
            que = Question_DB.objects.filter(tag=tag['tag']).annotate(row_num=Window(expression=RowNumber())).order_by('qno')
            que = [q for q in que if q.row_num <= 4]
            que = sample(que, min(len(que), 4))

            ques+=que
        random.shuffle(ques)'''
        ques = generate_paper(request,id)
        context = {
            "exam": exam,
            "question_list": ques,
            "secs": secs,
            "mins": mins
        }
        return render(request, 'exam/giveExam.html', context)
    if request.method == 'POST':
        student = request.user
        paper = request.POST['paper']
        examMain = Exam_Model.objects.get(name=paper)
        stuExam = StuExam_DB.objects.get_or_create(examname=paper,student=student,qpaper_id=examMain.question_paper.id)[0]
        random_questions = RandomQuestion.objects.filter(student=student)
        exam_score = 0

        #print(request.POST)
        for random_question in random_questions:
            choice = request.POST.get(str(random_question.question.question),False)
            print(choice)
            if not choice:
                choice='E'
            if choice.lower() == random_question.question.answer.lower():
                exam_score+=random_question.question.max_marks
            random_question.choice=choice
            random_question.save()
            print(exam_score)

        stuExam.score = exam_score
        stuExam.completed = 1
        stuExam.save()

        return redirect('view_exams_student')




def next_question(request, id, current_question_index):
    exam = get_object_or_404(Exam_Model, pk=id)
    questions = exam.question_paper.questions.all()
    try:
        current_question_index = int(current_question_index)
    except ValueError:
        current_question_index = 0
    if current_question_index < len(questions) - 1:
        current_question_index += 1
    context = {
        "exam": exam,
        "question_list": [questions[current_question_index]],
        "current_question_index": current_question_index,
        "secs": request.POST['secs'],
        "mins": request.POST['mins']
    }
    return render(request, 'exam/giveExam.html', context)
@login_required(login_url='login')
def result(request,id):
    student = request.user
    exam = Exam_Model.objects.get(pk=id)
    score = StuExam_DB.objects.get(student=student,examname=exam.name,qpaper=exam.question_paper).score
    return render(request,'exam/result.html',{'exam':exam,"score":score})
