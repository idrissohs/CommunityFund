from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from .forms import UserForm, ProjectForm, MatchForm
from accounts.views import RegisterProfile
from accounts.models import UserProfile
from .models import Project, Match
#from django.contrib.auth.decorators import login_required
# Create your views here.

#view to go to index page
def index(request):
	#return index page
	return render(request, 'project/index.html', {})

#view to logout
def logout (request):
    #log user out and return to index
    logout(request,'project/index.html')
    return render(request, 'project/index.html',{})

#view to login user
def login_user(request):
    #TODO fix login error messages
    login_error = False 
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            # the password verified for the user
            if user.is_active:		            	
                login(request, user)
                #get user profile and redirect based on account type
                profile = UserProfile.objects.get(user=request.user)
                if profile.account == 'F':
                    return redirect('project.views.funder')
                elif profile.account == 'I':
                    return redirect('project.views.initiator')
            else:
                login_error = False
        else:
            login_error = True
    
    return render(request, 'project/index.html', {'login_error':login_error})


#meant for testing purposes returns html that prins hello world
def blank(request):

		return render(request, 'project/blank.html', {})

#view to register user
def register(request):

    #boolean to check if user is registered
    registered = False

    if request.method == 'POST':
        #obtain user's info after they fill in their data
        user_form = UserForm(data=request.POST)
        #check if user enter valid data
        if user_form.is_valid():
            #save user data
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
            #authenticate after signup
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, user)
            return redirect (RegisterProfile)	
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render(request,'project/registration.html', {'user_form': user_form , 'registered': registered} )

#view to go funder homepage
def funder(request):
    #get all projects - TODO filter base on interest
	projects = Project.objects.all()
	for p in projects:
		total = 0
        #get all funders that funded this project
		matches = Match.objects.filter(project=p)
        #get total fundings for this project
		for m in matches:
			total = total + m.funding
		p.total_fund = total
		p.save()

	return render(request, 'project/funder.html', {'projects':projects})

#view to go to initiator homepage
def initiator(request):
	status = ""
	if request.method == "POST":
		form = ProjectForm(request.POST)
		if form.is_valid():
            #create and save project
			project = form.save(commit=False)
			project.author = request.user
			project.save()
			status = "Project created"
	else:
		form = ProjectForm()

	return render(request, 'project/initiator.html',{'form':form,'status':status})

#view to go to invidual project
def fund_project(request,pk):
    #get project
	project = get_object_or_404(Project, pk=pk)
	if request.method == "POST":
		form = MatchForm(request.POST)
		if form.is_valid():
            #collect funding for the project
			Match = form.save(commit=False)
			Match.funder = request.user
			Match.project = project
			Match.save()
			return redirect(funder)
	else:
		form = MatchForm()
        
	return render(request, 'project/fundproject.html', {'project':project,'form':form})
