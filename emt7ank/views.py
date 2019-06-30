from django.shortcuts import render
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordChangeView,
    PasswordChangeDoneView
)
class shafeayresetview(PasswordResetView):
	template_name="registration/shaf3y.html"



def hello_world(request):
	return render(request, 'hello_world.html')