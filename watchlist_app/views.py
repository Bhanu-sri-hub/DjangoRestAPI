from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse, JsonResponse

from watchlist_app.models import MonthlyChallenge

# Create your views here.
months = {"January":"This is is the first month to set goals",
          "February": "This is Feb",
          "March":"This is march",
          "April":"This is april",
          "May":"This is May",
          "June":"This is June",
          "July":"This is July",
          "August":"This is august",
          "September":"This is september",
          "October":"This is October",
          "November":"This is November",
          "Decemeber":"This is December"}
def adminView(request,month):
    return render(request,"blog/blog.html",{"text":months[month]})
def index(request):
    return render(request,"blog/index.html",{"months":months})
    
def monthlist(request):
    months = MonthlyChallenge.objects.all()
    data = {
        'monthslist' : list(months.values())
    }
    return JsonResponse(data)
