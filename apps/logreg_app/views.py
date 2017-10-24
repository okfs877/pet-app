# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

# readies and renders the register and login page
def index(request):
    return render(request, "index.html")
# validates a new users information and creates that user
def register(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        else:
            user = User.objects.maker(request.POST)
            request.session["user_id"] = user.id
    return redirect("/pets")
# verifies the users login infromation and adds their information to session
def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        user = User.objects.get(email=request.POST["email"])
        request.session["user_id"] = user.id
    return redirect("/pets")
# removes the current users infromation from session and logs them out
def logout(request):
    request.session.pop("user_id")
    return redirect("/")