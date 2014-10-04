from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from babysittingapp.forms import UserForm,UserProfileForm,ActivityForm
from babysittingapp.models import UserProfile, Sits
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required


def index(request):
	if request.user.is_authenticated():
		context = RequestContext(request)
		userprofile = UserProfile.objects.get(user = request.user)
		context_dict = {"userprofile":userprofile}
		context_dict["user"] = request.user
		allProfiles = UserProfile.objects.all()
		totalbalance = 0
		for profile in allProfiles:
			totalbalance += profile.balance
		context_dict["total"] = totalbalance
		context_dict["allprofiles"] = allProfiles
		return render_to_response('babysittingapp/index.html',context_dict,context)
	else:
		context = RequestContext(request)
		return render_to_response('babysittingapp/indexplain.html',{},context)

def register(request):
	context = RequestContext(request)
	registered = False
	if request.method == 'POST':
		user_form = UserForm(data = request.POST)
		profile_form = UserProfileForm(data = request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False)
			profile.user = user
			profile.save()

			registered = True

		else:
			print user_form.errors,profile_form.errors

	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render_to_response('babysittingapp/register.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered},context)


def user_login(request):

	context = RequestContext(request)
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username = username,password = password)
		if user:
			if user.is_active:
				login(request,user)
				return HttpResponseRedirect('/babysittingapp/')
			else:
				return HttpResponse('Your account is disabled')
		else:
			print "Invalid login details: {0}, {1}".format(username,password)
			return HttpResponse("Invalid login details supplied")
	else:
		return render_to_response('babysittingapp/login.html',{},context)

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/babysittingapp/')

@login_required
def add_activity(request):
	context = RequestContext(request)
	added = False

	if request.method == 'POST':
		activity_form = ActivityForm(data = request.POST)
		
		if activity_form.is_valid():
		
			activity = activity_form.save()
			print activity.sitting.username
			activity.goingout = request.user
			activity.save()

			# update the balance
			sitprofile = UserProfile.objects.get(user = activity.sitting)
			outprofile = UserProfile.objects.get(user = activity.goingout)
			cost = activity.cost
			sitprofile.balance = sitprofile.balance + cost
			outprofile.balance = outprofile.balance - cost

			sitprofile.save()
			outprofile.save()
			added = True
		else:
			print activity_form.errors
	else:
		activity_form = ActivityForm()

	return render_to_response("babysittingapp/addactivity.html",{"activity_form":activity_form,"added":added},context)

@login_required
def edit_activity(request,activity_id):
	context = RequestContext(request)
	added = False
	activity = Sits.objects.get(id=activity_id)

	

	if request.method == 'POST':
		activity_form = ActivityForm(data = request.POST,instance = activity)
		
		if activity_form.is_valid():
		
			activity = activity_form.save()
			print activity.sitting.username
			activity.goingout = request.user
			activity.save()

			# update the balance
			sitprofile = UserProfile.objects.get(user = activity.sitting)
			outprofile = UserProfile.objects.get(user = activity.goingout)
			cost = activity.cost
			sitprofile.balance = sitprofile.balance + cost
			outprofile.balance = outprofile.balance - cost

			sitprofile.save()
			outprofile.save()
			added = True
		else:
			print activity_form.errors
	else:
		sitprofile = UserProfile.objects.get(user = activity.sitting)
		outprofile = UserProfile.objects.get(user = activity.goingout)
		cost = activity.cost
		sitprofile.balance = sitprofile.balance - cost
		outprofile.balance = outprofile.balance + cost

		sitprofile.save()
		outprofile.save()

		activity_form = ActivityForm(instance = activity)

	return render_to_response("babysittingapp/editactivity.html",{"activity_form":activity_form,"added":added,'activity_id':activity.id},context)


@login_required
def view_activity(request):
	context = RequestContext(request)
	sitactivities = Sits.objects.filter(sitting = request.user).order_by('date')
	outactivities = Sits.objects.filter(goingout = request.user).order_by('date')
	profile = UserProfile.objects.get(user = request.user)
	context_dict = {"sitactivities":sitactivities}
	context_dict["outactivities"] = outactivities
	context_dict["balance"] = profile.balance
	context_dict["username"] = request.user.username
	return render_to_response("babysittingapp/viewactivity.html",context_dict,context)

@login_required
def delete_activity(request,activity_id):
	context = RequestContext(request)
	activity = Sits.objects.get(id=activity_id)
	sitprofile = UserProfile.objects.get(user = activity.sitting)
	outprofile = UserProfile.objects.get(user = activity.goingout)
	cost = activity.cost
	sitprofile.balance -= cost
	outprofile.balance += cost
	outprofile.save()
	sitprofile.save()
	activity.delete()
	return HttpResponseRedirect("/babysittingapp/viewactivity")



