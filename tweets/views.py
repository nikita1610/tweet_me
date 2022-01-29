import random
from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,JsonResponse
from django.conf import settings
from django.utils.http import is_safe_url

from tweetme.settings import ALLOWED_HOSTS

# Create your views here.

from .models import Tweet
from .forms import TweetForm


def home_view(request,*args,**kwargs):
    return render(request,"pages/home.html",context={},status=200)

def tweet_create_view(request,*args,**kwargs):
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        if request.is_ajax():
            return JsonResponse({},status=201)
        if next_url and is_safe_url(next_url,ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    return render(request,"components/form.html",context={'form':form})

def tweet_list_view(request,*args,**kwargs):
    tweets = Tweet.objects.all()
    tweet_data = [{"id":data.id,"content":data.content,"likes":random.randint(0,1200)} for data in tweets] 
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
