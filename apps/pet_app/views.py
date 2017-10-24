# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from ..logreg_app.models import User
from .models import Pet, Kind

# readies and renders the landing page that shows all the users and their pet count if the user is logged in
def index(request):
    if "user_id" not in request.session:
        return redirect("/")
    context = {
        "user" : User.objects.get(id=request.session["user_id"]),
        "users" : User.objects.exclude(id=request.session["user_id"]),
    }
    return render(request, "dashboard.html", context)

# readies and renders the page where a user can add a new pet to their profile
def new(request):
    if "user_id" not in request.session:
        return redirect("/")
    return render(request, "add.html")

# processes the from from add.html for adding a pet to a users profile
def create(request):
    if "user_id" not in request.session:
        return redirect("/")
    errors = Pet.objects.pet_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/pets/add')
    Pet.objects.create(name = request.POST["name"], kind= Kind.objects.get(id=int(request.POST["kind"])), user = User.objects.get(id=request.session["user_id"]))
    return redirect("/pets")

# shows a specific user and all of their pets
def showUser(request, id):
    if "user_id" not in request.session:
        return redirect("/")
    context = {
        "user" : User.objects.get(id=id)
    }
    return render(request, "show.html", context)

# euthanizes a pet from the database
def destroy(request, id):
    if "user_id" not in request.session:
        return redirect("/")
    if Pet.objects.get(id=id).user.id != request.session["user_id"]:
        return redirect("/pets")
    Pet.objects.get(id=id).delete()
    return redirect("/pets")

# alters an existing pets information
def edit(request, id):
    if "user_id" not in request.session:
        return redirect("/")
    context = {
        "pet" : Pet.objects.get(id=id),
        "kinds" : Kind.objects.all()
    }
    return render(request, "edit.html", context)

# processes the from from edit.html for changing a pet on a users profile
def update(request):
    if "user_id" not in request.session:
        return redirect("/")
    if Pet.objects.get(id=int(request.POST["pet_id"])).user.id != request.session["user_id"]:
        return redirect("/pets")
    errors = Pet.objects.pet_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/pets/edit/' + request.POST["pet_id"])
    pet = Pet.objects.get(id = int(request.POST["pet_id"]))
    pet.name = request.POST["name"]
    pet.kind = Kind.objects.get(id = int(request.POST["kind"]))
    pet.save()
    return redirect("/pets")