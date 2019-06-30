from django.urls import include, path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns =[
	path('<int:pk>/', views.RetrieveUpdateDestroyExam.as_view(), name='exam_detail'),
	path('<int:exam_pk>/mcqs/<int:pk>/', views.RetrieveUpdateDestroyMCQ.as_view(), name='mcq_detail'),
	path('<int:exam_pk>/mcqs/', views.ListCreateMCQ.as_view(), name='mcq_list'),
]
