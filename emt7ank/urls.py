from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,

)
from django.urls import include, path
from rest_framework import routers
from .views import hello_world, shafeayresetview
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
        path('reset-password/', PasswordResetView.as_view(), name='reset_password'),
        path('reset-password/done/',
                PasswordResetDoneView.as_view(),
                name='password_reset_done'
        ),
        path('reset-password/confirm/<slug:uidb64>-]/<slug:token>/',
                PasswordResetConfirmView.as_view(),
                name='password_reset_confirm'
        ),
        path('reset-password/complete/',
                PasswordResetCompleteView.as_view(),
                name='password_reset_complete'
        ),
    ]

admin.site.site_header = 'Emt7ank' 
admin.site.index_title = 'Dashboard' 
admin.site.site_title = 'Emt7ank'
