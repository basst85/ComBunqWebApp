from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from . import master
import json
from .forms import GetNewData
# Create your views here.


def Manager(request):
    # # NOTE: Colecting user input to match againts catagory in db
    if request.method == 'POST':
        print 'post'
        form = GetNewData(request.POST)
        inputData = json.loads(request.POST['json'])
        return HttpResponse(json.dumps(master.sortInfo(inputData)))
    else:
        form = GetNewData()
        print 'get'
    # # NOTE: endNote
    return render(request,'Manager/index.html',{ 'from': form  })
