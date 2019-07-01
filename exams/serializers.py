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
		instance.question = validated_data['question']
		instance.choice_a= validated_data['choice_a']
		instance.choice_b = validated_data['choice_b']
		instance.choice_c = validated_data['choice_c']
		instance.choice_d = validated_data['choice_d']
		instance.choice_e = validated_data['choice_e']
		instance.answer = validated_data['answer']
		instance.exam = Exam.objects.get(pk=validated_data['exam'])
		instance.save()

		return instance
	
	def create(self, validated_data):

		mcq = MCQ.objects.create(
			question = validated_data['question'],
			choice_a = validated_data['choice_a'],
			choice_b = validated_data['choice_b'],
			choice_c = validated_data['choice_c'],
			choice_d = validated_data['choice_d'],
			choice_e = validated_data['choice_e'],
			answer = validated_data['answer'],
			exam = Exam.objects.get(pk=validated_data['exam'])
		)
		return mcq

	## making a list of the choices for frontend purposes
	def get_choices(self, obj):
		if (obj.choice_e):
			queryset = (obj.choice_a, obj.choice_b,
					obj.choice_c, obj.choice_d, obj.choice_e )
		elif (obj.choice_d):
			queryset = queryset = (obj.choice_a, obj.choice_b,
					obj.choice_c, obj.choice_d )
		elif (obj.choice_c):
			queryset = queryset = (obj.choice_a, obj.choice_b,
					obj.choice_c )
		else:
			queryset = queryset = (obj.choice_a, obj.choice_b)

		return queryset

	## api v1 delete
	def delete(self, request, pk):
		mcq = MCQ.objects.get(pk=pk)
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
		instructor = User.objects.get(id=obj.instructor.pk)
		return instructor.username

	def get_created_at(self, obj):
		return obj.created_at.strftime("%d/%m/%Y %H:%M")

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

	## v1 create or update (put) / (post)
	def update(self, instance, validated_data):
		instance.subject = validated_data.get('subject', instance.subject)
		instance.time = validated_data.get('time', instance.time)
		instance.category = validated_data.get('category', instance.category)
		mcqs = validated_data.get('mcqs')
		for mcq in mcqs:
			print(mcq)
			try:
				mcq_id = mcq.get('id') 
				item = MCQ.objects.get(exam=instance, pk=mcq_id)
				item.choice_a=mcq["choice_a"]
				item.choice_b=mcq["choice_b"]
				item.choice_c=mcq["choice_c"]
				item.choice_d=mcq["choice_d"]
				item.choice_e=mcq["choice_e"]
				item.question=mcq["question"]	
				item.answer=mcq["answer"]
			except:
				item = MCQ.objects.create(
					choice_a=mcq["choice_a"],
					choice_b=mcq["choice_b"],
					choice_c=mcq["choice_c"],
					choice_d=mcq["choice_d"],
					choice_e=mcq["choice_e"],
					question=mcq["question"],	
					answer=mcq["answer"],
					exam=instance,
				)
			print(item)
			item.save()
		instance.save() 
		return instance

	## api v1 delete
	def delete(self, request, pk):
		exam = Exam.objects.get(pk=pk)
		mcqs = MCQ.objects.filter(exam=exam)
		for mcq in mcqs:
			mcq.delete()
		mcq.delete()

class FinishedExamsSerializer(ModelSerializer):
	exam_url = SerializerMethodField()
	exam = SerializerMethodField()
	taken_at = SerializerMethodField()

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

	def get_taken_at(self, obj):
		return obj.taken_at.strftime("%d/%m/%Y %H:%M")

class TakeLaterExamsSerializer(ModelSerializer):
	exam = SerializerMethodField()
	added_at = SerializerMethodField()
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

	def get_added_at(self, obj):
		return obj.added_at.strftime("%d/%m/%Y %H:%M")	

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
		profile_data = validated_data['profile']

		## conditions to complete the empty fields
		if profile_data.get('bio'):
			p_bio = profile_data['bio']
		else:
			p_bio = ""
		
		if profile_data.get('career'):
			p_career = profile_data['career']
		else:
			p_career = ""
		
		if profile_data.get('location'):
			p_location = profile_data['location']
		else:
			p_location = ""
		
		if profile_data.get('birth_date'):
			p_birth_date = profile_data['birth_date']
		else:
			p_birth_date = None
		
		if profile_data.get('phone_number'):
			p_phone_number = profile_data['phone_number']
		else:
			p_phone_number = ""
		
		if profile_data.get('avatar'):
			p_avatar = profile_data['avatar']
		else:
			p_avatar = "blank_avatar.png"


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
			is_teacher = profile_data['is_teacher'],
			bio = p_bio,
			career = p_career,
			location = p_location,
			birth_date = p_birth_date,
			phone_number = p_phone_number,
			avatar = p_avatar,
		)
		profile.save()
		token = Token.objects.create(user=user)
		return user
		# finished_exams = FinishedExams.objects.get(user=user)
		# profile.is_teacher = profile_data.is_teacher
		# profile.bio = profile_data.bio
			# location=profile_data.location,
			# career=profile_data.career,
			# birth_date=profile_data.birth_date,
			# phone_number=profile_data.phone_number,
			# avatar=profile_data.avatar,


	def update(self, instance, validated_data):
		instance.email = validated_data.get('email', instance.email)
		instance.first_name = validated_data.get('first_name', instance.first_name)
		instance.last_name = validated_data.get('last_name', instance.last_name)
		profile_data = validated_data['profile']

	 # conditions to complete the empty fields
		if profile_data.get('bio'):
			p_bio = profile_data['bio']
		else:
			p_bio = ""
		
		if profile_data.get('career'):
			p_career = profile_data['career']
		else:
			p_career = ""
		
		if profile_data.get('location'):
			p_location = profile_data['location']
		else:
			p_location = ""
		
		if profile_data.get('birth_date'):
			p_birth_date = profile_data['birth_date']
		else:
			p_birth_date = None
		
		if profile_data.get('phone_number'):
			p_phone_number = profile_data['phone_number']
		else:
			p_phone_number = ""
		
		if profile_data.get('avatar'):
			p_avatar = profile_data['avatar']
		else:
			p_avatar = "blank_avatar.png"
	 #
		instance.profile.bio = p_bio
		instance.profile.location = p_location
		instance.profile.career = p_career
		instance.profile.birth_date = p_birth_date
		instance.profile.phone_number = p_phone_number
		instance.profile.avatar = p_avatar
		instance.save()
		# finished_exams = FinishedExams.objects.get(user=user)
		return instance

class PasswordSerializer(Serializer):
	old_password = CharField(required=True)
	new_password = CharField(required=True)


	# def update(self, instance, validated_data):
	# 	instance.set_password(validated_data['password'])
	# 	instance.save()
	# 	return instance
