from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First Name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last Name should be at least 2 characters"
        if len(postData['username']) < 3:
            errors["username"] = "Username should be at least 3 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = ('Invalid Email Address')
        if len(postData['email']) < 6:
            errors["email"] = "Email Address must be at least 6 characters"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData['password'] != postData['confirm_password']:
            errors["confirm_password"] = "Passwords do not match"
        if len(postData['date_of_birth']) < 4:
            errors["date_of_birth"] = "Date of Birth required"
        return errors

    def login_validator(self, postData):
        user = User.objects.filter(username=postData['login_username'])
        errors = {}
        if not user:
            errors['username'] = "Please enter a valid username"
        if user and not bcrypt.checkpw(postData['login_password'].encode('utf8'), user[0].password.encode('utf8')):
            errors['password'] = "Incorrect Password"
        return errors

class WorkoutManager(models.Manager):
    def add_workout_user(self, user_id, workout_id):
        workout = Workout.objects.get(id=workout_id)
        current_user = User.objects.get(id=user_id)
        workout.workout_user.add(current_user)

    def remove_workout(self, user_id, workout_id):
        workout = Workout.objects.get(id=workout_id)
        current_user = User.objects.get(id=user_id)
        workout.workout_user.remove(current_user)

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    date_of_birth= models.DateTimeField()
    weight = models.IntegerField(default='0')
    num_of_workout_days = models.IntegerField(default='1')
    WORKOUT_OPTIONS = (
        ('cardio', 'Cardio'),
        ('weights','Weights'),
        ('mixed', 'Mixed'),
    )
    workout_choice = models.CharField(max_length=7, choices=WORKOUT_OPTIONS, default='mixed')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    sets = models.IntegerField()
    reps = models.IntegerField()
    workout_type = models.CharField(max_length=7)
    workout_region = models.CharField(default="", max_length=9)
    workout_user = models.ManyToManyField(User, related_name="user_workout")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WorkoutManager()