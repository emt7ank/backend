from rest_framework.serializers	import (
	ModelSerializer,
	SerializerMethodField,
	HyperlinkedRelatedField,
	)
from django.core import serializers
from .models import Exam, MCQ, FinishedExams, TakeLaterExams
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token



class MCQSerializer(ModelSerializer):
	# choices = SerializerMethodField()
	class Meta:
		fields =(
			'question',
			# 'choices',
			'answer',
		)
		model = MCQ 
	# def get_choices(self, obj):
	# 	if (obj.choice_e):
	# 		queryset = (obj.choice_a, obj.choice_b,
	# 				obj.choice_c, obj.choice_d, obj.choice_e )
	# 	elif (obj.choice_d):
	# 		queryset = queryset = (obj.choice_a, obj.choice_b,
	# 				obj.choice_c, obj.choice_d )
	# 	elif (obj.choice_c):
	# 		queryset = queryset = (obj.choice_a, obj.choice_b,
	# 				obj.choice_c )
	# 	else:
	# 		queryset = queryset = (obj.choice_a, obj.choice_b)

	# 	return queryset



class ExamSerializer(ModelSerializer):
	instructor = SerializerMethodField()
	mcqs = MCQSerializer(many=True,)


	class Meta:
		fields = (
			'pk',
			'created_at',
			'instructor',
			'category',
			'subject',
			'time' ,
			'mcqs',
		)
		read_only_fields = ("instructor",'created_at',)
		model = Exam
	def get_instructor(self, obj):
		instructor = User.objects.get(id=obj.instructor.pk)
		return instructor.username

	def create(self, validated_data):
		mcqs = validated_data.pop('mcqs')
		exam = Exam.objects.create(
			instructor=self.context['request'].user,
			category=validated_data['category'],
			subject=validated_data['subject'],
			time=validated_data['time']
		)
		for mcq in mcqs:
			MCQ.objects.create(exam=exam,**mcq)
		exam.save()	
		return exam


class FinishedExamsSerializer(ModelSerializer):
	exam_url = SerializerMethodField()
	exam = SerializerMethodField()

	class Meta:
		fields = (
			'exam',
			'exam_url',
			'taken_at',
			'result',
			'full_mark',
		)
		model = FinishedExams

	def get_exam(self, obj):
		try:
			test = Exam.objects.get(pk=obj.pk)
			res = test.subject
		except Exam.DoesNotExist:
			res = None
		return res

	def get_exam_url(self, obj):
		try:
			test = Exam.objects.get(pk=obj.pk)
			res = test.subject
		except Exam.DoesNotExist:
			res = None
		return res


class TakeLaterExamsSerializer(ModelSerializer):
	exam = SerializerMethodField()
	class Meta:
		fields = (
			'exam',
			'added_at',
		)
		model = TakeLaterExams
	def get_exam(self, obj):
		try:
			test = Exam.objects.get(pk=obj.pk)
			res = test.subject
		except Exam.DoesNotExist:
			res = None
		return res


class UserSerializer(ModelSerializer):
	latest_result = SerializerMethodField()
	finished_exams = FinishedExamsSerializer(many=True, default=None)
	take_later_exams = TakeLaterExamsSerializer(many=True, read_only=True)

	class Meta:
		fields = (	'id',
					'username',
					'email',
					'password',
					'first_name',
					'last_name',
					'finished_exams',
					'take_later_exams',
					'latest_result',

		)
		model = User
		read_only_fields = ('id', 'finished_exams', 'latest_result')
		write_only_fields = ('password',)


	def get_latest_result(self, obj):
		try:
			queryset = FinishedExams.objects.filter(
				user=obj).latest('taken_at')
			res = queryset.result
			ful = queryset.full_mark
			percent = int((res/ful)*100)
			string = str(percent) + str('%')
		
		except FinishedExams.DoesNotExist:
			string = None
		return string


	def create(self, validated_data):
		user = User.objects.create(
			username=validated_data['username'],
			email=validated_data['email'],
			first_name=validated_data['first_name'],
			last_name=validated_data['last_name']
		)

		user.set_password(validated_data['password'])
		user.save()
		token = Token.objects.create(user=user)
		# finished_exams = FinishedExams.objects.get(user=user)
		return user