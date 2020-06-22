from rest_framework.serializers	import (
	ModelSerializer,
	SerializerMethodField,
	HyperlinkedRelatedField,
	IntegerField,
	CharField,
	Serializer,
	)
from .models import Exam, MCQ, FinishedExams, TakeLaterExams, Profile
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404


class MCQSerializer(ModelSerializer):
	choices = SerializerMethodField()
	id = IntegerField(required=False)
	exam = CharField(required=False)
	class Meta:
		fields =(
			'question',
			'id',
			'choice_a',
			'choice_b',
			'choice_c',
			'choice_d',
			'choice_e',
			'choices',
			'answer',
			'exam'
		)
		model = MCQ 
	
	def update(self, instance, validated_data):
		for attr, value in validated_data.items():
			setattr(instance, attr, value)
		instance.exam = Exam.objects.get(pk=validated_data['exam'])
		instance.save()
		return instance
	
	def create(self, validated_data):
		exam_id = validated_data.pop('exam')
		mcq = MCQ.objects.create(
			**validated_data,
			exam_id = exam_id
		)
		return mcq

	## making a list of the choices for frontend purposes
	def get_choices(self, obj):
		if (obj.choice_e):
			queryset = [
				obj.choice_a,
				obj.choice_b,
				obj.choice_c or None,
				obj.choice_d or None,
				obj.choice_e or None
			]
		return list(filter(lambda choice: choice, queryset))

	## api v1 delete
	def delete(self, request, pk):
		mcq = get_object_or_404(MCQ, pk=pk)
		mcq.delete()


class ExamSerializer(ModelSerializer):
	instructor = SerializerMethodField()
	mcqs = MCQSerializer(many=True,)
	created_at = SerializerMethodField()

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
		return obj.instructor.username

	def get_created_at(self, obj):
		return obj.created_at.strftime("%d/%m/%Y %H:%M")

	def create(self, validated_data):
		mcqs = validated_data.pop('mcqs')
		exam = Exam.objects.create(
			instructor=self.context['request'].user,
			**validated_data
		)
		for mcq in mcqs:
			MCQ.objects.create(exam=exam, **mcq)
		return exam

	## v1 create or update (put) / (post)
	def update(self, instance, validated_data):
		mcqs = validated_data.pop('mcqs')
		for mcq in mcqs:
			MCQ.objects.update_or_create(
				exam=instance,
				pk=mcq.get('id'),
				defaults=mcq
			)
		for attr, value in validated_data.items():
			setattr(instance, attr, value)
		instance.save()
		return instance

	## api v1 delete
	def delete(self, request, pk):
		exam = get_object_or_404(Exam, pk=pk)
		exam.mcq_set.all().delete()
		exam.delete()


class FinishedExamsSerializer(ModelSerializer):
	exam_url = SerializerMethodField()
	exam = SerializerMethodField()
	taken_at = SerializerMethodField()
	exam_pk = IntegerField(required=False)
	
	class Meta:
		fields = (
			'exam',
			'exam_url',
			'taken_at',
			'result',
			'exam_pk'
		)
		model = FinishedExams
	
	def get_exam(self, obj):
		try:
			test = Exam.objects.get(pk=obj.exam.pk)
			res = test.subject
		except Exam.DoesNotExist:
			res = None
		return res

	def get_exam_url(self, obj):
		try:
			test = Exam.objects.get(pk=obj.exam.pk)
			res = test.get_absolute_url()
		except Exam.DoesNotExist:
			res = None
		return res

	def get_taken_at(self, obj):
		return obj.taken_at.strftime("%d/%m/%Y %H:%M")


class TakeLaterExamsSerializer(ModelSerializer):
	exam = SerializerMethodField()
	exam_url = SerializerMethodField()
	added_at = SerializerMethodField()
	
	class Meta:
		fields = (
			'exam',
			'exam_url',
			'added_at',
		)
		model = TakeLaterExams
	def get_exam(self, obj):
		try:
			test = Exam.objects.get(pk=obj.exam.pk)
			res = test.subject
		except Exam.DoesNotExist:
			res = None
		return res

	def get_exam_url(self, obj):
		try:
			test = Exam.objects.get(pk=obj.exam.pk)
			res = test.get_absolute_url()
		except Exam.DoesNotExist:
			res = None
		return res


	def get_added_at(self, obj):
		return obj.added_at.strftime("%d/%m/%Y %H:%M")	


class AddFininshedExamsSerializer(Serializer):
	result = IntegerField(required=True)
	exam_pk = IntegerField(required=True)


class AddTakeLaterExamsSerializer(Serializer):
	exam_pk = IntegerField(required=True)


class ProfileSerializer(ModelSerializer):
	bio = CharField(required=False)
	class Meta:
		exclude = ['id']
		read_only_fields = ('user',)
		model = Profile


class UserSerializer(ModelSerializer):
	latest_result = SerializerMethodField()
	finished_exams = FinishedExamsSerializer(many=True, default=None)
	take_later_exams = TakeLaterExamsSerializer(many=True, read_only=True)
	profile = ProfileSerializer()
	password=CharField(required=False)
	username=CharField(required=False)	
	class Meta:
		fields = (	'id',
					'username',
					'email',
					'password',
					'first_name',
					'last_name',
					'profile',
					'finished_exams',
					'take_later_exams',
					'latest_result',
		)
		model = User
		read_only_fields = ('id', 'finished_exams', 'latest_result',)
		write_only_fields = ('password')

	def get_latest_result(self, obj):
		try:
			queryset = FinishedExams.objects.filter(user=obj).latest('taken_at')
			res = queryset.result
			string = str(res) + str('%')
		
		except FinishedExams.DoesNotExist:
			string = None
		return string


	def create(self, validated_data):
		profile_data = validated_data['profile']

		user = User.objects.create(
			username=validated_data['username'],
			email=validated_data['email'],
			first_name=validated_data['first_name'],
			last_name=validated_data['last_name']
		)
		user.set_password(validated_data['password'])
		user.save()
		profile = Profile.objects.create(
			user=user,
			**profile_data
		)
		profile.save()
		token = Token.objects.create(user=user)
		return user


	def update(self, instance, validated_data):
		instance.email = validated_data.get('email', instance.email)
		instance.first_name = validated_data.get('first_name', instance.first_name)
		instance.last_name = validated_data.get('last_name', instance.last_name)
		instance.save()
		profile_data = validated_data['profile']
		Profile.objects.filter(user=instance).update(**profile_data)
		return instance


class PasswordSerializer(Serializer):
	old_password = CharField(required=True)
	new_password = CharField(required=True)