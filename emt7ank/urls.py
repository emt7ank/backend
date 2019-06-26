"""emt7ank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from .views import hello_world
from exams import views
from rest_framework.authtoken.views import obtain_auth_token

router = routers.SimpleRouter()
router.register('exams', views.ExamModelViewSet)
router.register('mcqs', views.MCQModelViewSet)
router.register('users', views.UserViewSet)

urlpatterns = [
    	path('admin/', admin.site.urls),
    	path('', hello_world),
        path('api-auth/', include('rest_framework.urls')),
        path('api/v1/exams/', include('exams.urls')),
        path('api/v2/', include(router.urls)),
        path('api-token-auth/', obtain_auth_token),
        path('api/password_reset/', include('django_rest_passwordreset.urls')),
    ]

admin.site.site_header = 'Emt7ank' 
admin.site.index_title = 'Dashboard' 
admin.site.site_title = 'Emt7ank'
