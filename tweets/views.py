import stat
from django.shortcuts import render
from django.http import HttpResponse,Http404,JsonResponse
# Create your views here.

from .models import Tweet

def home_view(request,*args,**kwargs):
    return render(request,"pages/home.html",context={},status=200)

def tweet_list_view(request,*args,**kwargs):
    tweets = Tweet.objects.all()
    tweet_data = [{"id":data.id,"content":data.content} for data in tweets] 
    response = {
        "response":tweet_data
    } 
    return JsonResponse(response,status=200) 

def tweet_detail_view(request,tweet_id,*args,**kwargs):
    try:
        data = {
            "id" : tweet_id
        }
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
        status=200
    except Exception as e:
        data["message"] = "Not Found"
        status=404
    return JsonResponse(data,status=status)
