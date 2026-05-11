from django.http import HttpResponse

def home(request):
    return HttpResponse("Diet app is working!")
