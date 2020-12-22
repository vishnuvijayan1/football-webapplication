from django.shortcuts import render
from .models import Teams, TeamMatches
from .forms import TeamRegisterForm
from .forms import LoginForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.shortcuts import redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
import datetime
import math
import random
from django.db.models import Q
from django.http import JsonResponse



""" function of admin login."""
def admin_login(request):
	if request.method == 'POST':
		form=LoginForm(request.POST)
		if form.is_valid():
			username=form.cleaned_data['username']
			password=form.cleaned_data['password']
			user = authenticate(request, username=username, password=password)
			if user is not None:
				if user.is_superuser:
					auth_login(request,user)
					return redirect('/admin/list-all-teams')
				else:
					form=LoginForm()
					context={'form':form }
					message=messages.add_message(request, messages.ERROR, 'Incorrect Username or Password')
					return render(request,'login.html',context)

			else:
				form=LoginForm()
				context={'form':form }
				message=messages.add_message(request, messages.ERROR, 'Incorrect Username or Password')
				return render(request,'login.html',context)
		else:
			form=LoginForm()
			context={'form':form }
			message=messages.add_message(request, messages.ERROR, 'Username or password is not valid')
			return render(request,'login.html',context)

	else:
		form=LoginForm()
		context={'form':form }
		return render(request,'login.html',context)



""" function to list all the registered teams. """
@login_required(login_url='/admin-login')
def list_all_teams(request):
    teams=Teams.objects.all()
    teams_count=Teams.objects.all().count()
    paginator = Paginator(teams, 10)
    page = request.GET.get('page')
    paginated_list = paginator.get_page(page)
    context={'teams':paginated_list,'teams_count':teams_count}
    return render(request,'list-teams.html',context)



""" function to list the team details and matchs(if the registration closed. """
@login_required(login_url='/admin-login')
def team_details(request,team_id):
	team_details = Teams.objects.get(id=team_id)
	team_matches = None
	team_count = Teams.objects.all().count()
	if(team_count == 10):
		match_fixture = TeamMatches.objects.filter(
		    Q(team_a=team_id) | Q(team_b=team_id))
		paginator = Paginator(match_fixture, 10)
		page = request.GET.get('page')
		paginated_list = paginator.get_page(page)
		context={'match_fixture':paginated_list,'team_details':team_details}
		return render(request,'team-details.html',context)
	else:
		context={'team_details':team_details}
		return render(request,'team-details.html',context)



""" function to render home page """
def home_page(request):
	teams_count = Teams.objects.all().count()
	context={'teams_count':teams_count}
	if(teams_count == 10):
		return redirect('/match-fixture')
	return render(request,'home-page.html',context)



""" function to register new team """
def team_registration(request):
	if request.method == 'POST':
		form=TeamRegisterForm(request.POST)
		if form.is_valid():
			team_name=form.cleaned_data['team_name']
			team_players=form.cleaned_data['team_members']
			team_manager=form.cleaned_data['team_manager']
			team_coach=form.cleaned_data['team_coach']
			if team_name is None or team_players is None or team_coach is None or team_manager is None:
				form=TeamRegisterForm()
				context={'form':form}
				return render(request,'register-team.html',context)
			else:
				team_instance = Teams(
				    team_name=team_name,
				    team_players=team_players,
				    team_coach=team_coach,
				    team_manager=team_manager
				)
				x = team_instance.save()
				team_count = Teams.objects.all().count()
				if(team_count == 10):
				    generate_match_fixture()
				message=messages.add_message(request, messages.SUCCESS, 'Registration Successfull')
				return redirect('/registeration-completed')
		else:
			teams_count = Teams.objects.all().count()
			if(teams_count == 10):
				return render(request,'registeration-complete.html',context)
			else:
				form=TeamRegisterForm()
				context={'form':form}
				return render(request,'register-team.html',context)
	else:
		teams_count = Teams.objects.all().count()
		print(teams_count)
		if(teams_count == 10):
			return redirect('/')
		else:
			form=TeamRegisterForm()
			context={'form':form }
			return render(request,'register-team.html',context)


"""function to render the submission page of registration"""
def completed_registration(request):
	return render(request,'registeration-complete.html')



"""function to create the match fixture"""
def generate_match_fixture():
	start_date = date(2021, 3, 1)
	end_date = date(2021, 3, 23)

	delta = end_date - start_date

	match_teams = list(Teams.objects.all())  # [1,2,3,4,5,6,7,8,9,10]
	print(match_teams)

	middle_index = int(len(match_teams)/2)

	temp_list = []

	matches = []

	temp_list.append(match_teams[:middle_index])  # [[1,2,3,4,5]]
	secondhalf = match_teams[middle_index:]  # [6,7,8,9,10]
	secondhalf.reverse()  # [10,9,8,7,6]
	temp_list.append(secondhalf)  # [[1,2,3,4,5],[10,9,8,7,6]]

	for i in range(0, 9):
		for j in range(0, 5):
			matches.append([temp_list[0][j], temp_list[1][j]])

		left_jumper = temp_list[1][0]
		right_jumper = temp_list[0][4]

		temp_list[0][4] = temp_list[0][3]
		temp_list[0][3] = temp_list[0][2]
		temp_list[0][2] = temp_list[0][1]
		temp_list[0][1] = left_jumper

		temp_list[1][0] = temp_list[1][1]
		temp_list[1][1] = temp_list[1][2]
		temp_list[1][2] = temp_list[1][3]
		temp_list[1][3] = temp_list[1][4]
		temp_list[1][4] = right_jumper

	scheduled = []
	venue = ['Trivandrum', 'Mumbai', 'Banglore', 'Goa', 'Cochin']

	match_objects = []
	day = datetime.date(2021, 3, 1)
	time = datetime.time(8)
	date_tracker = 1
	for match in matches:
		scheduled.append([day, match, random.choice(venue)])
		match_instance = TeamMatches(
			date=day, team_a=match[0], team_b=match[1], venue=random.choice(venue), time=time)
		match_objects.append(match_instance)
		time = datetime.time(16)
		if(date_tracker % 2 == 0):
			time = datetime.time(8)
			day += timedelta(days=1)
		date_tracker = date_tracker + 1

	TeamMatches.objects.bulk_create(match_objects)



"""function used to list the match fixture for admin and user"""
def get_match_fixture(request):
	match_fixture = TeamMatches.objects.all()
	paginator = Paginator(match_fixture, 10)
	page = request.GET.get('page')
	paginated_list = paginator.get_page(page)
	context={'match_fixture':paginated_list}
	return render(request,'match-fixture.html',context)




"""function used to list the match fixture"""
@login_required(login_url='/admin-login')
def get_match_details(request):
	match_id=request.POST.get('matchId')
	match_details = TeamMatches.objects.get(id=match_id)
	data={'team_a_score':match_details.team_a_points, 'team_b_score':match_details.team_b_points, 
	'team_a_name':match_details.team_a.team_name, 'team_b_name':match_details.team_b.team_name, 
	'match_id':match_details.id}
	return JsonResponse(data)



"""function to update the match points"""
@login_required(login_url='/admin-login')
def update_match_points(request):
	match_id = request.POST.get("matchId")
	team_a_points=request.POST.get('team_a_points')
	team_b_points=request.POST.get('team_b_points')
	print(team_a_points,team_b_points)
	match_instance = TeamMatches.objects.get(id=match_id)
	match_instance.team_a_points = team_a_points
	match_instance.team_b_points = team_b_points
	match_instance.save()
	return JsonResponse("successfull updated",safe=False)


"""function used to loggout admin"""
def admin_logout(request):
	logout(request)
	return redirect('/admin-login')