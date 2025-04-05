from django.shortcuts import render, HttpResponse

# Create your views here.
def visuals(request):
    return render(request, "visuals/charts.html")