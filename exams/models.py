from django.urls import reverse
from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Exam(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	instructor = models.ForeignKey(User, on_delete=models.CASCADE)
	category = models.CharField(max_length=255)
	subject = models.CharField(default='', max_length=255)
	time = models.IntegerField()
	full_mark = models.IntegerField(default=100)
	


	def __str__(self):
		return self.subject

	def get_absolute_url(self):
		relative = reverse("exam_detail", kwargs={"pk":self.pk})
		return ('http://%s%s'%(Site.objects.get_current().domain, relative))

	# @classmethod
	# def get_ex"blank_avatar.png"am_mcqs(test):
	# 	mcqs = MCQ.objects.filter(exam_pk=test)
	# 	mcqs_list = [mcqs]
	# 	return mcqs_list

	# mcqs = get_exam_mcqs(Exam.pk)


class MCQ(models.Model):
	CHOICES_MCQ = (
					('0', 'choice_a'), 
					('1', 'choice_b'), 
					('2', 'choice_c'),
					('3', 'choice_d'), 
					('4', 'choice_e')
				)
	question = models.TextField(null=False)
	choice_a = models.CharField(max_length=255, null=False)
	choice_b = models.CharField(max_length=255, null=False)
	choice_c = models.CharField(max_length=255,
	 							blank=True, null=True, default=None)
	choice_d = models.CharField(max_length=255,
	 							blank=True, null=True, default=None)
	choice_e = models.CharField(max_length=255,
	 							blank=True, null=True, default=None)
	exam = models.ForeignKey(Exam, related_name='mcqs',
								on_delete=models.CASCADE)
	answer = models.CharField(choices=CHOICES_MCQ, max_length=3, null=False)
	
	class Meta:
		verbose_name = "MCQ"
		verbose_name_plural = "MCQs"

	def __str__(self):
		return self.question



class FinishedExams(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE,
							related_name="finished_exams", null=False)
	exam = models.ForeignKey(Exam, on_delete=models.CASCADE,
									related_name='exam_url', null=False)
	taken_at = models.DateTimeField(auto_now_add=True)
	result = models.IntegerField()
	full_mark = models.IntegerField(default=100)

	class Meta:
		ordering = ['-taken_at']




class TakeLaterExams(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE,
							related_name="take_later_exams")
	exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
	added_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-added_at']


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField(blank=True)
	location = models.CharField(max_length=255, blank=True)
	career = models.CharField(max_length=255, blank=True)
	birth_date = models.DateField(null=True, blank=True)
	is_teacher = models.BooleanField(default=False)
	phone_number = models.CharField(max_length=14, blank=True)
	avatar = models.ImageField(upload_to='personal/%y/%m/', default="blank_avatar.png")