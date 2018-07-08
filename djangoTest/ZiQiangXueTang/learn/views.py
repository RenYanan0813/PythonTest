from django.shortcuts import render

# Create your views here.

def home(request):
    title = "自谦"
    return render(request,'learn/index.html', {"titlestr": title})
