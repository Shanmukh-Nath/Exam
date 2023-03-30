from django.contrib import admin
from .models import *



class ContactAdmin(admin.ModelAdmin):
    pass

admin.site.register(StudentInfo)
admin.site.register(Stu_Question)
admin.site.register(StuExam_DB)
admin.site.register(StuResults_DB)
admin.site.register(Contact,ContactAdmin)
admin.site.register(Gallery)