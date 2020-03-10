from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from App.models import Videos_Data,Users,Subscription
from django.conf import settings
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt
import os
import random, string
from time import strftime
from django.contrib import messages

from App import recommend


# Create your views here.

def index(request):
	flag = False
	all_videos = Videos_Data.objects.all()
	if request.session.has_key('is_logged'):
		userPic = Users.objects.filter(UserId=request.session['is_logged'])
		flag = True
		params = {'videos':all_videos,'image':userPic,'flag':flag}
	else:
		params = {'videos':all_videos}
	return render(request,'index.html',params)

def watch(request,vid):
	if request.session.has_key('is_logged'):
		userPic = Users.objects.filter(UserId=request.session['is_logged'])
	watch_video = Videos_Data.objects.filter(Video_Id=vid)
	for v in watch_video:
		vid_name = v.Title
	lt = []
	movie = recommend.recommender(vid_name)
	for movie_name in movie:
		obj = Videos_Data.objects.filter(Title=movie_name)
		lt.append(obj)

	count=''
	for i in watch_video:
		count = str(i.Views)
	view_count = str(int(count)+1)
	datasave = Videos_Data.objects.filter(Video_Id=vid).update(Views=view_count)
	watch_video = Videos_Data.objects.filter(Video_Id=vid)
	if request.session.has_key('is_logged'):
		userPic = Users.objects.filter(UserId=request.session['is_logged'])
		params = {"video":watch_video,'all_videos':lt,'image':userPic}
	else:
		params = {"video":watch_video,'all_videos':lt}
	return render(request,'play.html',params)

def about(request):
	if request.session.has_key('is_logged'):
		userPic = Users.objects.filter(UserId=request.session['is_logged'])
		params = {'image':userPic}
	else:
		params = {}
	return render(request,'about.html',params)


#Uploading Video Using login.html
def upload(request):
	if request.method=="POST":
		thumbnail = request.FILES['tnail']
		video = request.FILES['video']
		title = request.POST.get('title')
		category = request.POST.get('category')
		description = request.POST.get('description')
		
		userChannel = Users.objects.filter(UserId=request.session['is_logged'])
		for e in userChannel:
			channel = e.Channel_Name
		vid = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
		dt = strftime("%d-%m-%Y")
		tm = strftime("%H:%M")

		upload = Videos_Data(Video_Id=vid,Title=title,Channel_Name=channel,Category=category,Description=description,Date=dt,Time=tm,Thumb=thumbnail,Video=video)
		upload.save()
		messages.success(request,'Saved Successfully..!!')
		return HttpResponseRedirect('/')
	else:
		flag = False
		if request.session.has_key('is_logged'):
			flag = True
			userPic = Users.objects.filter(UserId=request.session['is_logged'])
			params = {'image':userPic,'flag':flag}
			return render(request,'uploadfile.html',params)
		else:
			return render(request,'login.html')


def login(request):
	if request.method=="POST":
		email = request.POST.get('email')
		pswd = request.POST.get('password')
		#print(email,pswd)
		login_check = Users.objects.filter(Email=email)
		for e in login_check:
			holdername = e.Name
			userId = e.UserId
			userpass = e.Password
		if check_password(pswd,userpass) == True:
			request.session['is_logged'] = userId
			request.session['name'] = holdername
			return HttpResponseRedirect('/')
		else:
			return HttpResponse("Invalid Password")
	else:
		if request.session.has_key('is_logged'):
			return HttpResponseRedirect('/')
		else:
			return render(request,'login.html')

def registerpage(request):
	return render(request,'register.html')

def register(request):
	if request.method=="POST":
		name = request.POST.get('name')
		channel = request.POST.get('channel')
		email = request.POST.get('email')
		pswd = request.POST.get('password')

		# Generating Random alphanumeric value
		uid = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
		password = make_password(pswd)
		# return HttpResponse(password)
		dt = strftime("%d-%m-%Y")
		tm = strftime("%H:%M")
		register = Users(UserId=uid,Name=name,Channel_Name=channel,Email=email,Password=password,Date=dt,Time=tm)
		register.save()
		return render(request,'index.html')
	else:
		return render(request,'register.html')

def cpasswordpage(request):
	return render(request,'changepassword.html')

def cpasswordsave(request):
	if request.method=="POST":
		email = request.POST.get('email')
		cpass = request.POST.get('cpass')
		npass = request.POST.get('npass')
		vpass = request.POST.get('vpass')
		obj = Users.objects.filter(Email=email)
		if obj:
			for p in obj:
				upass = p.Password
			if check_password(cpass,upass) == True:
				if npass != vpass:
					messages.success(request,'New Password and Verify Password does not match')
					return render(request,'changepassword.html')
				else:
					password = make_password(npass)
					datasave = Users.objects.filter(Email=email).update(Password=password)
					messages.success(request,'Change Password Successfully')
					return render(request,'changepassword.html')
			else:
				messages.success(request,'Invalid Current Password')
				return render(request,'changepassword.html')
		else:
			messages.success(request,'Invalid Email-ID')
			return render(request,'changepassword.html')
	
def search(request):
	flag = False
	
	query = request.GET['search']
	if len(query)>20:
		allposts = Videos_Data.objects.none()
	else:
		allPostTitle = Videos_Data.objects.filter(Title__icontains=query)
		allPostChannel_Name = Videos_Data.objects.filter(Channel_Name__icontains=query)
		allPostCategory = Videos_Data.objects.filter(Category__icontains=query)
		allposts = allPostTitle.union(allPostCategory,allPostChannel_Name)
	if allposts.count() == 0:
		messages.warning(request,'No search results found. Please refine your query')
	if request.session.has_key('is_logged'):
		flag = True
		userPic = Users.objects.filter(UserId=request.session['is_logged'])
		params = {'allposts':allposts,'query':query,'flag':flag,'image':userPic}
	else:
		params = {'allposts':allposts,'query':query,'flag':flag}
	return render(request,'search.html',params)

def logout(request):
	if request.session.has_key('is_logged'):
		del request.session['is_logged']
		return HttpResponseRedirect('/')
	else:
		messages.warning(request,'You are already logout. Please login...')
		return render(request,'login.html')

def post_likes(request,vid):
	posts = Videos_Data.objects.filter(Video_Id=vid)
	count=''
	for i in posts:
		count = str(i.Likes)
	like_count = str(int(count)+1)
	datasave = Videos_Data.objects.filter(Video_Id=vid).update(Likes=like_count)
	post = Videos_Data.objects.filter(Video_Id=vid)
	params = {"video":post}
	return render(request, 'play.html', params)

def post_dislikes(request,vid):
	posts = Videos_Data.objects.filter(Video_Id=vid)
	count=''
	for i in posts:
		count = str(i.Dislikes)
	dislike_count = str(int(count)+1)
	datasave = Videos_Data.objects.filter(Video_Id=vid).update(Dislikes=dislike_count)
	post = Videos_Data.objects.filter(Video_Id=vid)
	params = {"video":post}
	return render(request, 'play.html', params)
 
def post_comments(request,vid):
	c = request.POST.get('comment')
	datasave = Videos_Data.objects.filter(Video_Id=vid).update(Comments=c.capitalize())
	post = Videos_Data.objects.filter(Video_Id=vid)
	params = {"video":post}
	return render(request, 'play.html', params)
 

def subscribe(request):
	if request.method=="POST":
		if request.session.has_key('is_logged'):
			userEmail = Users.objects.filter(UserId=request.session['is_logged'])
			for e in userEmail:
				uemail = e.Email
				em = Subscription.objects.filter(email=uemail)
				if em:
					messages.warning(request,'You are already subscribed !!')
					return HttpResponseRedirect('/')
				else:
					data = Subscription(email=uemail)
					data.save()
					return HttpResponseRedirect('/')
		else:
			messages.warning(request,'Sign in to subscribe to this channel')
			return HttpResponseRedirect('/')



#--------------Categories----------------

def category(request):
	if request.method == "POST":
		cat = request.POST.get('cat')
	all_videos = Videos_Data.objects.filter(Category__icontains=cat)
	if request.session.has_key('is_logged'):
		userPic = Users.objects.filter(UserId=request.session['is_logged'])
		params = {'videos':all_videos,'category':cat,'image':userPic}
	else:
		params = {'videos':all_videos,'category':cat}
	return render(request,'categorywise.html',params)
