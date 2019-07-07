from django.shortcuts import get_object_or_404
from rest_framework.permissions import (IsAuthenticated,
										IsAdminUser,
										BasePermission,
										AllowAny,
)
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from django.db.models import Q
from .models import Exam, MCQ, FinishedExams, TakeLaterExams
from .serializers import (
		ExamSerializer,
		MCQSerializer,
		UserSerializer,
		PasswordSerializer,
		FinishedExamsSerializer,
		TakeLaterExamsSerializer,
		AddFininshedExamsSerializer,
		AddTakeLaterExamsSerializer,
)
from django.contrib.auth.models import User
from rest_framework.decorators import list_route


## to fiind out it he is a teacher or not
class IsTeacher(BasePermission):
	def has_permission(self, request, view):
		if request.user.profile.is_teacher:
			return True
		return False


# for api version 1
class ListCreateExam(generics.ListCreateAPIView):
	permission_classes = (
		IsAuthenticated,
		IsTeacher,
	)
	queryset = Exam.objects.all()
	serializer_class = ExamSerializer
 
class RetrieveUpdateDestroyExam(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (
		IsAuthenticated,
	)		
	queryset = Exam.objects.all()
	serializer_class = ExamSerializer


class ListCreateMCQ(generics.ListCreateAPIView):
	permission_classes = (
		IsAuthenticated,
	)
	queryset = MCQ.objects.all()
	serializer_class = MCQSerializer

	def get_queryset(self):
		if self.kwargs.get('exam_pk'):
			return self.queryset.filter(exam=self.kwargs.get('exam_pk'))
		return self.queryset.all()

class RetrieveUpdateDestroyMCQ(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (
		IsAuthenticated,
	)
	queryset = MCQ.objects.all()
	serializer_class = MCQSerializer

	def get_object(self):
		return get_object_or_404(
			self.get_queryset(),
			exam=self.kwargs.get('exam_pk'),
			pk=self.kwargs.get('pk')
		)
	

# for api version 2
class ExamModelViewSet(viewsets.ModelViewSet):
	permission_classes = (
		IsAuthenticated,
	)
	queryset = Exam.objects.all()
	serializer_class = ExamSerializer

	# to access the mcqs from /exams/<pk>/mcqs/
	@detail_route(methods=['get'], url_path='mcqs')
	def mcqs(self, request, pk=None):
		exam = self.get_object()
		serializer = MCQSerializer(MCQ.objects.filter(exam=exam),
														 many=True)
		return Response(serializer.data)

# we used mixins below instead of ModelViewSet because we wanted to adjust which 
# operation should be included in the apiview (we deleted the listModel of mcqs)
# we didn't want just to list all the mcqs of all the exams that exist
# on the website in one page .. it would have been messy

class MCQModelViewSet(
			mixins.CreateModelMixin,
			mixins.RetrieveModelMixin,
			mixins.UpdateModelMixin,
			mixins.DestroyModelMixin,
			viewsets.GenericViewSet,
			):
	permission_classes = (IsAuthenticated,)
	queryset = MCQ.objects.all()
	serializer_class = MCQSerializer



class UserViewSet(viewsets.ModelViewSet):
	permission_classes = (AllowAny,)
	queryset = User.objects.all()
	serializer_class = UserSerializer

	@detail_route(methods=['put'], url_path='change-password')
	def set_password(self, request, pk=None):
		user = self.get_object()
		serializer = PasswordSerializer(data=request.data)
		if serializer.is_valid():
			if not user.check_password(serializer.data.get('old_password')):
				return Response({'old_password': ['Wrong password.']}, 
									status=status.HTTP_400_BAD_REQUEST)
			# set_password also hashes the password that the user will get
			user.set_password(serializer.data.get('new_password'))
			user.save()
			return Response({'status': 'password set'}, status=status.HTTP_200_OK)

		return Response(serializer.errors,
			status=status.HTTP_400_BAD_REQUEST)

	@list_route(methods=['GET'], permission_classes=[IsAuthenticated])
	def me(self, request, *args, **kwargs):
		self.kwargs.update(pk=request.user.id)
		return self.retrieve(request, *args, **kwargs)



	@detail_route(methods=['get', 'post'], url_path='finished-exams')
	def finished_exams(self, request, pk=None):
		user = self.get_object()

		if request.method == 'GET':
			serializer = FinishedExamsSerializer(
				FinishedExams.objects.filter(user=user), many=True)
			return Response(serializer.data)
		
		else:
			serializer = AddFininshedExamsSerializer(data=request.data)
			if serializer.is_valid():
				exam_pk = serializer.data.get('exam_pk')
				c_exam = Exam.objects.get(pk=exam_pk)
				test = FinishedExams.objects.create(
					user=user,
					exam=c_exam,
					result=serializer.data.get('result'),
				)
				test.save()
				return Response(
					{'status': 'the exam has beed added to your finished exams'},
					status=status.HTTP_200_OK
				)

		return Response(serializer.errors,
				status=status.HTTP_400_BAD_REQUEST)


	@detail_route(methods=['get', 'post'], url_path='take-later-exams')
	def take_later_exams(self, request, pk=None):
		user = self.get_object()

		if request.method == 'GET':
			serializer = TakeLaterExamsSerializer(
				TakeLaterExams.objects.filter(user=user), many=True)
			return Response(serializer.data)
		
		else:
			serializer = AddTakeLaterExamsSerializer(data=request.data)
			if serializer.is_valid():
				test = TakeLaterExams.objects.create(
					user=user,
					exam=Exam.objects.get(pk=serializer.data.get('exam_pk')),
				)
				test.save()
				return Response(
					{'status': 'the exam has beed added to your Take Later list'},
					status=status.HTTP_200_OK
				)

		return Response(serializer.errors,
				status=status.HTTP_400_BAD_REQUEST)