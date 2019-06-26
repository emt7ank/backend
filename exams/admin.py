from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


from .models import Exam, MCQ, FinishedExams, TakeLaterExams

class MCQTabularInline(admin.TabularInline):
	model = MCQ

class ExamAdmin(admin.ModelAdmin):
	inlines = [MCQTabularInline]
	class Meta:
		model = Exam



## adding finished exams and take later exms to the admin page of the use model
class FinishedExamsInline(admin.StackedInline):
	model = FinishedExams

class TakeLaterExamsInline(admin.StackedInline):
	model = TakeLaterExams

class UserAdmin(BaseUserAdmin):
	inlines = [FinishedExamsInline, TakeLaterExamsInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(MCQ)