from itertools import chain
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Class

# Create your views here.
def index(request):
    psy329 = Class.objects.filter(name="PSY 329")
    psy305 = Class.objects.filter(name="PSY 305")
    hist354 = Class.objects.filter(name="HIST 354")
    csc484 = Class.objects.filter(name="CSC 484")

    context = {"classes": list(chain(psy329, psy305, hist354, csc484))}
    return render(request, 'pass_app/main.html', context)

def tanner(request):
    psy329 = Class.objects.filter(name="CSC 480")
    psy305 = Class.objects.filter(name="CSC 402")
    hist354 = Class.objects.filter(name="CSC 305")
    csc484 = Class.objects.filter(name="PSY 350")

    context = {"classes": list(chain(psy329, psy305, hist354, csc484))}
    return render(request, 'pass_app/main.html', context)

def eric(request):
    psy329 = Class.objects.filter(name="ART 182")
    psy305 = Class.objects.filter(name="CPE 357")
    hist354 = Class.objects.filter(name="PHYS 132")

    context = {"classes": list(chain(psy329, psy305, hist354))}
    return render(request, 'pass_app/main.html', context)

def amanda(request):
    bus319 = Class.objects.filter(name="BUS 319")
    bus391 = Class.objects.filter(name="BUS 391")
    itp330 = Class.objects.filter(name="ITP 330")
    bus342 = Class.objects.filter(name="BUS 342")
    bus387 = Class.objects.filter(name="BUS 387")
    bus346 = Class.objects.filter(name="BUS 346")

    context = {"classes": list(chain(bus319, bus342, bus346, bus387, bus391, itp330))}
    return render(request, 'pass_app/main.html', context)

def sawyer(request):
    psy350 = Class.objects.filter(name="PSY 350")
    ime223 = Class.objects.filter(name="IME 223")
    ime301 = Class.objects.filter(name="IME 301")
    ime319 = Class.objects.filter(name="IME 319")
    isla303 = Class.objects.filter(name="ISLA 303")

    context = {"classes": list(chain(psy350, ime223, ime301, ime319, isla303))}
    return render(request, 'pass_app/main.html', context)

def class_lookup(request, cls):
    cls_name = []
    found_digit = False
    for char in cls:
        if char.isdigit() and not found_digit:
            found_digit = True
            cls_name.append(' ')
        cls_name.append(char.upper())

    class_name = ''.join(cls_name)
    print(class_name)

    class_object = get_object_or_404(Class, name=class_name) 

    context = {"classes": [class_object]}
    return render(request, 'pass_app/main.html', context)

def list_classes(request):
    classes = Class.objects.all()
    class_list = sorted([cls.name for cls in classes])
    return JsonResponse({"classes": class_list})

