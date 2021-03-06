from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import User
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import random
import json
import string
from django.http import JsonResponse
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import tweepy
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, ValidationError

# Decorators function to prohibit illegal access to the urls directly


def prohibit_url_access(func):
    def wrap(request, *args, **kwargs):
        if "user" in request.session:
            return func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap


API_KEY="tdgvUp2IBZY1I9z1Qw8u7uiLB"
API_SECRET="TLFE0ZJa0ua3iEMMt3XSMVPPbLhJQi4xIEHSG05K2zrrUXlBzl"
ACCESS_TOKEN="1088087472121102336-Q08jjVCsimX4FHY8UiooiluceE34VI"
ACCESS_TOKEN_SECRET="8kFdQ6CH52N08V3WnbMfQA62RALesZDKDudYm21W5GCc6"

def test(request):
    print("hel")
    return False


def testAuthPassword(request):
    hashed_pwd = make_password("Chitti@123")
    print(hashed_pwd)
    result = check_password("Chitti@123", hashed_pwd)
    print(result)
    return HttpResponse("hi")

# Create your views here.


def index(request):
    # del request.session["user"]
    # return render(request, "login.html", {'current': 'home'})
    if "user" not in request.session:
        return render(request, "login.html", {'current': 'home'})
    else:
        return render(request, "dashboard.html")


def registerUser(request):
    return render(request, "index.html")


def forgotPassword(request):
    return render(request, "forgot_password.html")


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def emailAlreadyExists(email_id):
    user = User.objects.filter(email=email_id).first()
    return user


def send_email(request):
    email_id = request.POST['email']
    user = emailAlreadyExists(email_id)
    verification_string = randomString(10)

    try:
        if user:
            to_be_updated_user = User.objects.get(email=email_id)
            to_be_updated_user.verification_string = verification_string
            to_be_updated_user.save()
            html_content = render_to_string(
                'mail_sample.html', {'verification_string': verification_string})
            email = EmailMessage("my subject", html_content,
                                 "sunilthakur123chor@gmail.com", [email_id])
            email.content_subtype = "html"
            res = email.send()
        else:
            return render(request, 'forgot_password.html', {'already_exists': True})
    except:
        print("error")
        return redirect('/forgot_password')
    return redirect('/')


def reset(request):
    user = User.objects.get(email=request.POST['email'])
    user.password = request.POST['password']
    user.save()
    return redirect("/dashboard")


def createUser(request):
    user = User()
    print("email")
    print(request.POST['email'])
    flag = emailAlreadyExists(request.POST['email'])
    print(flag)
    if not flag:
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.password = make_password(request.POST['password'])
        print(not user.save())
        if not user.save():
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': "failure"})
    else:
        return JsonResponse({'status': "Email already exists!"})


def userDashboard(request):
    url = ('https://newsapi.org/v2/top-headlines?'
           'sources=bbc-news&'
           'apiKey=662aeb83e8594969932a697595cead13')
    response = requests.get(url)
    result = response.json()
    articles = result['articles']
    analyser = SentimentIntensityAnalyzer()
    sentiments = []
    for source in articles:
        score = analyser.polarity_scores(source['description'])
        sentiments.append(score)
    length = list(range(len(articles) + 1))
    indexes = list(range(11))
    context = zip(articles, sentiments, indexes)
    return render(request, "dashboard.html", {"news": context, "length": length, "sentiments": sentiments})


def userLogin(request):
    try:
        user = User.objects.get(email=request.POST["email"])
        matched = check_password(request.POST["password"], user.password)
        if matched:
            request.session["user"] = request.POST["email"]
            return redirect('/dashboard')
        else:
            return render(request, "login.html", {'state': 1})

    except:
        return render(request, "login.html", {'state': 1})


def verifyEmail(request, verification_string_through_email):
    flag = User.objects.filter(
        verification_string=verification_string_through_email).first()
    if flag:
        flag.verification_string = 0
        email_id = flag.email
        flag.save()
        return render(request, 'verify_email_success.html', {"email": email_id})
    else:
        return render(request, 'verify_email_failure.html')


@prohibit_url_access
def showKeyword(request):
    return render(request, "keyword.html", {'current': 'key'})


no = 0
tweets = ""
def fetchKeyword(request):
	auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	obj = tweepy.API(auth)
	class MyStreamListener(tweepy.StreamListener):
	   def on_data(self, data):
	       global no, tweets
	       no += 1
	       data = json.loads(data)
	       print(len(data))
	       print(data)
	       if 'text' in data:
		       tweets += data['text'] + " "
	       if no == 100:
	           no = 0
	           return False
	   def on_status(self, status):
	       myStreamListener = MyStreamListener()
	       myStream = tweepy.Stream(auth = obj.auth, listener = myStreamListener)
	       myStream.filter(track = request.POST['keyword'])
	   def on_error(self, status_code):
	       if status_code == 420:
	           return False

	global tweets, no
	streamListener = MyStreamListener()
	streamListener.on_status("success")
	analyser = SentimentIntensityAnalyzer()
	score = analyser.polarity_scores(tweets)
	no = 0
	tweets = ""
	return render(request, 'keyword.html', {"score": score})



def fetchKeyword(request):
    API_KEY = "BB8uhuyrMzHesokpE7RqcYemc"
    API_SECRET = "7YhL2UOSVoUyquuImiT1uOag0gS5HR3mrt7mmXrNZbwNHOVklF"
    ACCESS_TOKEN = "2330384770-kx4jr7mfUsCJod2MNuff3VzCh6tbGCvdymwp3ND"
    ACCESS_TOKEN_SECRET = "IMEYoDK2gZITSztqKQvHohTMOPkmEjsA0w6AOoECIdCqu"
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    obj = tweepy.API(auth)

    class MyStreamListener(tweepy.StreamListener):
        def on_data(self, data):
            global no, tweets
            no += 1
            data = json.loads(data)
            tweets += data['text'] + " "
            if no == 50:
                no = 0
                return False

        def on_status(self, status):
            myStreamListener = MyStreamListener()
            myStream = tweepy.Stream(auth=obj.auth, listener=myStreamListener)
            myStream.filter(track=request.POST['keyword'])

        def on_error(self, status_code):
            if status_code == 420:
                return False

    global tweets, no
    streamListener = MyStreamListener()
    streamListener.on_status("success")
    analyser = SentimentIntensityAnalyzer()
    score = analyser.polarity_scores(tweets)
    no = 0
    tweets = ""
    return render(request, 'keyword.html', {"score": score})


@prohibit_url_access
def showText(request):
    return render(request, 'text_sentiment.html', {'current': 'show'})


def fetchTextSentiments(request):
    analyser = SentimentIntensityAnalyzer()
    score = analyser.polarity_scores(request.POST['text'])
    return render(request, 'text_sentiment.html', {"score": score, "text": request.POST['text']})


@prohibit_url_access
def showCompare(request):
	return render(request, "compare.html")

def compare(request):
	key1 = request.POST['keyword1']
	key2 = request.POST['keyword2']
	auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	obj = tweepy.API(auth)
	class MyStreamListener(tweepy.StreamListener):
	   def setData(self, data):
	       self.search_data = data
	   def on_data(self, data):
	       global no, tweets
	       no += 1
	       data = json.loads(data)
	       if 'text' in data:
		       tweets += data['text'] + " "
	       if no == 100:
	           no = 0
	           return False
	   def on_status(self, status):
	       myStreamListener = MyStreamListener()
	       myStream = tweepy.Stream(auth = obj.auth, listener = myStreamListener)
	       myStream.filter(track = self.search_data)
	   def on_error(self, status_code):
	       if status_code == 420:
	           return False

	streamListener1 = MyStreamListener()
	streamListener1.setData(request.POST['keyword1'])
	streamListener1.on_status("success")
	analyser1 = SentimentIntensityAnalyzer()
	score1 = analyser1.polarity_scores(streamListener1.search_data)

	streamListener2 = MyStreamListener()
	streamListener2.setData(request.POST['keyword2'])
	streamListener2.on_status("success")
	analyser2 = SentimentIntensityAnalyzer()
	score2 = analyser2.polarity_scores(streamListener2.search_data)

	return render(request, "compare_result.html", {"keyword1": request.POST['keyword1'], "keyword2": request.POST['keyword2'], "score1": score1, "score2": score2})
