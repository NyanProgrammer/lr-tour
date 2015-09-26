from django.http import HttpResponse


def home(request):
	return HttpResponse('Hello world from django 1.8 on Open Shift')