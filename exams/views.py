from django.shortcuts import get_object_or_404
from rest_framework.permissions import (IsAuthenticated,
										IsAdminUser,
										BasePermission,
										AllowAny,
)
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from .models import Exam, MCQ, FinishedExams, TakeLaterExams
from .serializers import ExamSerializer, MCQSerializer, UserSerializer
from django.contrib.auth.models import User

# for api version 1
class ListCreateExam(generics.ListCreateAPIView):
	queryset = Exam.objects.all()
	serializer_class = ExamSerializer
 
class RetrieveUpdateDestroyExam(generics.RetrieveUpdateDestroyAPIView):
	queryset = Exam.objects.all()
	serializer_class = ExamSerializer


class ListCreateMCQ(generics.ListCreateAPIView):
	queryset = MCQ.objects.all()
	serializer_class = MCQSerializer

	def get_queryset(self):
		if self.kwargs.get('exam_pk'):
			return self.queryset.filter(exam=self.kwargs.get('exam_pk'))
		return self.queryset.all()

class RetrieveUpdateDestroyMCQ(generics.RetrieveUpdateDestroyAPIView):
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
	permission_classes = (IsAuthenticated,)
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
			viewsets.GenericViewSet
):
	permission_classes = (IsAuthenticated,)
	queryset = MCQ.objects.all()
	serializer_class = MCQSerializer



class UserViewSet(viewsets.ModelViewSet):
	permission_classes = (AllowAny,)
	queryset = User.objects.all()
	serializer_class = UserSerializer