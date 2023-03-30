from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .forms import StudentForm, StudentInfoForm
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from .utils import account_activation_token
from django.core.mail import EmailMessage
import threading
import datetime
from django import template
from django.contrib.auth.models import User
from studentPreferences.models import StudentPreferenceModel
from django.contrib.auth.models import Group
from student.models import Contact, Gallery
from django.core.mail import EmailMultiAlternatives,BadHeaderError
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@login_required(login_url='login')
def index(request):
    return render(request, 'student/index.html')


def con(request):
    cont = Contact.objects.all()
    return render(request, 'student/contact.html', {'con': cont})


def gall(request):
    data = Gallery.objects.all()
    return render(request, 'student/gal.html', {'data': data})


class Register(View):
    def get(self, request):
        student_form = StudentForm()
        student_info_form = StudentInfoForm()
        return render(request, 'student/register.html',
                      {'student_form': student_form, 'student_info_form': student_info_form})

    def post(self, request):
        student_form = StudentForm(data=request.POST)
        student_info_form = StudentInfoForm(data=request.POST)
        email = request.POST['email']

        if student_form.is_valid() and student_info_form.is_valid():
            student = student_form.save()
            student.set_password(student.password)
            student.is_active = False
            my_group = Group.objects.get_or_create(name='Student')
            my_group[0].user_set.add(student)
            student.save()
            uidb64 = urlsafe_base64_encode(force_bytes(student.pk))
            domain = get_current_site(request).domain
            link = reverse('activate', kwargs={'uidb64': uidb64, 'token': account_activation_token.make_token(student)})
            activate_url = 'http://' + domain + link
            email_subject = 'Activate your Exam Portal account'
            html_content = render_to_string('email_activation.html',
                                            {'activate': activate_url, 'username': student.username})
            text_content = strip_tags(html_content)
            fromEmail = 'noreply@exam.com'
            email1 = EmailMultiAlternatives(
                email_subject,
                text_content,
                fromEmail,
                [email]
            )
            email1.attach_alternative(html_content, 'text/html')
            email1.send()
            # email_body = 'Hi '+student.username +'.Please use this link to verify your account\n' + activate_url + ".\n\n You are receiving this message because you registered on " + domain +". If you didn't register please contact support team on " + domain

            # email = EmailMessage(
            #	email_subject,
            #	email_body,
            #	fromEmail,
            #	[email],
            # )
            student_info = student_info_form.save(commit=False)
            student_info.user = student
            if 'picture' in request.FILES:
                student_info.picture = request.FILES['picture']
            student_info.save()
            messages.success(request, "Registered Succesfully. Check Email for confirmation")
            #EmailThread(email).start()
            return redirect('login')
        else:
            print(student_form.errors, student_info_form.errors)
            return render(request, 'student/register.html',
                          {'student_form': student_form, 'student_info_form': student_info_form})


class LoginView(View):
    def get(self, request):
        return render(request, 'student/login.html',{'form':PasswordResetForm})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)

        if username and password:
            exis = User.objects.filter(username=username).exists()
            if exis:
                user_ch = User.objects.get(username=username)
                if user_ch.is_staff:
                    messages.error(request,
                                   "You are trying to login as student, but you have registered as faculty. We are redirecting you to faculty login. If you are having problem in logging in please reset password or contact admin")
                    return redirect('faculty-login')
            user = auth.authenticate(username=username, password=password)
            print(user)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    student_pref = StudentPreferenceModel.objects.filter(user=request.user).exists()
                    email = User.objects.get(username=username).email
                    dt=datetime.datetime.now()
                    now=dt.strftime("%d-%m-%Y %H:%M:%S")
                    email_subject = 'You Logged into your Portal account'
                    html_content = render_to_string('logged_in.html',
                                                    {'username': username,'time':now})
                    text_content = strip_tags(html_content)
                    fromEmail = 'noreply@exam.com'
                    email1 = EmailMultiAlternatives(
                        email_subject,
                        text_content,
                        fromEmail,
                        [email]
                    )
                    email1.attach_alternative(html_content, 'text/html')
                    email1.send()
                    if student_pref:
                        student = StudentPreferenceModel.objects.get(user=request.user)
                        sendEmail = student.sendEmailOnLogin
                    if not student_pref:
                        EmailThread(email).start()
                    #elif sendEmail:
                     #   EmailThread(email).start()
                    messages.success(request, "Welcome, " + user.username + ". You are now logged in.")

                    return redirect('index')

            else:
                user_n = User.objects.filter(username=username).exists()
                if user_n:
                    user_v = User.objects.get(username=username)
                    if user_v.is_active:
                        messages.error(request, 'Invalid credentials')
                        return render(request, 'student/login.html')
                    else:
                        messages.error(request,
                                       'Account not Activated, Please Activate the account through the activation link sent to your registered mailid.')
                        return render(request, 'student/login.html')

        messages.error(request, 'Please fill all fields')
        return render(request, 'student/login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'Logged Out')
        return redirect('login')


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            if not account_activation_token.check_token(user, token):
                messages.error(request, "User already Activated. Please Proceed With Login")
                return redirect("login")
            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()
            messages.success(request, 'Account activated Sucessfully')
            return redirect('login')
        except Exception as e:
            raise e
        return redirect('login')


class Password_reset(View):
    def get(self,request):
        password_reset_form=PasswordResetForm()
        return render(request,'student/resetPassword.html',{'form':password_reset_form})

    def post(self,request):
        if request.method=="POST":
            password_reset_form=PasswordResetForm(request.POST)
            if password_reset_form.is_valid():
                data=password_reset_form.cleaned_data['email']
                associated_users=User.objects.filter(Q(email=data)|Q(username=data))
                if associated_users.exists():
                    for user in associated_users:
                        subject="Password Reset Requested"
                        plaintext=template.loader.get_template('forgot.txt')
                        htmltemp=template.loader.get_template('forgot.html')
                        domain=get_current_site(request).domain
                        from_email="noreply@exam.in"
                        c={
                            'email':user.email,
                            'domain':domain,
                            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                            'user':user,
                            'token':default_token_generator.make_token(user),
                            'protocol':'http',
                        }
                        text_content=plaintext.render(c)
                        html_content=htmltemp.render(c)
                        try:
                            msg=EmailMultiAlternatives(subject,text_content,from_email,[user.email])
                            msg.attach_alternative(html_content,'text/html')
                            msg.send()
                        except BadHeaderError:
                            return HttpResponse('Invalid header found.')
                        messages.info(request,"Password reset instructions have been sent successfully.")
                        return redirect('login')
        password_reset_form=PasswordResetForm()
        return render(request,template_name='student/resetPassword.html',context={"password_reset_form":password_reset_form})

