from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def login(request):
    return render(request, "template_login.html");

def check_login(request):
    if (request.method == "POST"):
        return HttpResponse("OK");
    else:
        return