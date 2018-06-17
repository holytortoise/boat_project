from django.shortcuts import render
from django.http import HttpResponse
from calendar import HTMLCalendar

# Create your views here.
def index(request):
    calendar = HTMLCalendar().formatyear(2018)
    context_dict={'calendar':calendar}
    return render(request, 'index.html',context_dict)
