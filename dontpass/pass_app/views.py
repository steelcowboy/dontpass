from django.shortcuts import render
from .models import Class

# Create your views here.
def index(request):
    context = {"classes": Class.objects.all()}
    return render(request, 'pass_app/main.html', context)
