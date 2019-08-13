from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
import bcrypt
import random
from .models import *

def index(request):
    if "id" in request.session.keys():
        redirect('/home')
    return render(request, 'lift_final/index.html')

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        date_of_birth = request.POST['date_of_birth']
        user = User.objects.create(first_name=first_name, last_name=last_name, username = username, email=email, password=hashed_password, date_of_birth=date_of_birth)
        user.save()
        print(user)
        request.session['id'] = user.id 
        return redirect("/info")

def info(request):
    user = User.objects.get(id=request.session['id'])
    return render(request, 'lift_final/info.html')

def input(request):
    user = User.objects.get(id=request.session['id'])
    user.weight = request.POST['weight']
    user.num_of_workout_days = request.POST['num_of_workout_days']
    user.workout_choice = request.POST['workout_choice']
    user.save()
    return redirect('/home')

def home(request):
    user = User.objects.get(id=request.session['id'])
    workout = Workout.objects.all()
    my_workout = Workout.objects.filter(workout_user=request.session['id'])
    workout_days = user.num_of_workout_days
    chest = my_workout.filter(workout_region="chest")
    arms = my_workout.filter(workout_region="arms")
    shoulders = my_workout.filter(workout_region="shoulders")
    legs = my_workout.filter(workout_region="legs")
    back = my_workout.filter(workout_region="back")
    leftovers = my_workout.filter(workout_region="")

    weekly_schedule = []
    if chest in my_workout:
        weekly_schedule.append(chest)
    if arms in my_workout:
        weekly_schedule.append(arms)
    if legs in my_workout:
        weekly_schedule.append(legs)
    if shoulders in my_workout:
        weekly_schedule.append(shoulders)
    if back in my_workout:
        weekly_schedule.append(back)
    for leftover in leftovers:
       weekly_schedule.append(leftover)
    random.shuffle(weekly_schedule)
    context = {
        "user" : user,
        "workout" : workout,
        "my_workout" : my_workout,
        "workout_days" : workout_days,
        "weekly_schedule" : weekly_schedule,
        "chest" : chest,
        "arms" : arms,
        "shoulders" : shoulders,
        "legs" : legs,
        "back" : back,
        "leftovers": leftovers,
    }
    return render(request, 'lift_final/home.html', context)

def workout_info(request, workout_id):
    user = User.objects.get(id=request.session['id'])
    workout = Workout.objects.get(id=workout_id)
    user_workouts = Workout.objects.filter(workout_user=request.session['id'])

    context = {
        "workout" : workout,
        "user" : user,
        "user_workouts": user_workouts,
    }
    return render(request, 'lift_final/workout_info.html', context)

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else: 
        user = User.objects.get(username=request.POST['login_username'])
        request.session['id'] = user.id
        return redirect('/home')

def log_out(request):
    del request.session['id']
    return redirect('/')

def workouts(request):
    user = User.objects.get(id=request.session['id'])
    workout = Workout.objects.get(id=request.session['id'])
    user_workouts = Workout.objects.filter(workout_user=request.session['id'])
    weights = Workout.objects.all().filter(workout_type = 'weight')
    cardio = Workout.objects.all().filter(workout_type = 'cardio')
    mixed = Workout.objects.all().filter(workout_type = 'mixed')
    context = {
        "weights" : weights,
        "cardio" : cardio,
        "mixed" : mixed,
        "workout" : workout,
        "user_workouts" : user_workouts,
        "user" : user,
    }
    return render(request, "lift_final/workouts.html", context)

def profile(request, user_id):
    user = User.objects.get(id=user_id)
    context = {
        "user": user,
    }
    return render(request, "lift_final/profile.html", context)

def update (request, user_id):
    user = User.objects.get(id=user_id)
    user.weight = request.POST['weight']
    user.num_of_workout_days = request.POST['num_of_workout_days']
    user.workout_choice = request.POST['workout_choice']
    user.save()
    return redirect("/home")

def my_workout(request, workout_id):
    user_id = request.session['id']
    Workout.objects.add_workout_user(user_id, workout_id)
    return redirect('/home')

def remove_workout(request, workout_id):
    user_id = request.session['id']
    Workout.objects.remove_workout(user_id, workout_id)
    return redirect('/home')