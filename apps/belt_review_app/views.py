from __future__ import unicode_literals
from models import *
from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt



def index(request):
	return render(request, 'belt_review_app/index.html')

def dashboard(request):
	context = {
		###get items from only the logged in user
		'user': User.objects.get(id=request.session['user_id']),
		"your_items": User_item.objects.filter(user__id = request.session['user_id']).all(),
		'other_pplitems': User_item.objects.exclude(user__id = request.session['user_id']).all()
	}
	return render(request, 'belt_review_app/dashboard.html', context)

def additem(request):
	return render(request, 'belt_review_app/additem.html')

def addform(request):
	errors = Item.objects.basic_validator(request.POST)
	if len(errors):
		for tag, error in errors.iteritems():
			messages.error(request, error, extra_tags=tag)
		return redirect('/wish_items/create')
	else:	
		####then we do the form action
		user = User.objects.get(id = request.session['user_id'])
		item = Item.objects.create(name=request.POST['name'])
		user_item = User_item.objects.create(user=user, item=item)
		return redirect('/dashboard')

def deletewish(request, id):
	#get the id of the item we want to remove
	User_item.objects.get(id=id).delete()
	return redirect('/dashboard')

def addwish(request, id):
	###get the user you are
	user = User.objects.get(id = request.session['user_id'])
	##get the item from {{item.id}} that we passed in the url
	item = Item.objects.get(id = id)
	##get everythin from that user in a variable
	user_items = User_item.objects.all()
	####creating one more item
	user_items.create(user = user, item = item)
	###deleting that item from where it originally was
	item.delete()
	##save
	item.save()
	return redirect('/dashboard')






def showuser(request, id):
	context = {
		"users_for_item": User_item.objects.filter(item__id = id).all(),
	}
	return render(request, 'belt_review_app/item.html', context)

def logout(request):
	request.session['user_id'] = 0
	return redirect('/main')
	

################################################################################################################################################
def register(request):
	###below comes from validate_reg in models.Manager
	errors = User.objects.validate_reg(request.POST)
	if errors:
		##for the exact error 
		for tag, error in errors.iteritems():
			messages.error(request, error, extra_tags=tag)
		return redirect('/main')
	else:
		####if the user has entered successfully log them in
		pass
		found_users = User.objects.filter(email=request.POST['email'])
		if found_users.count() > 0:
			##display an error if the email has already been taken
			messages.error(request, "email already taken", extra_tags="email")
			return redirect('/main')
		else:
			#register the user
			hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
			created_user = User.objects.create(name=request.POST['name'], user_name =request.POST['user_name'], email=request.POST['email'], password=hashed_pw)
			request.session['user_id'] = created_user.id
			request.session['user_name'] = created_user.name
			print created_user
			return redirect('/dashboard')
		return redirect('/main')
def login(request):
	###se if email is in the database
	found_users = User.objects.filter(email=request.POST['email'])
	if found_users.count() > 0:
		#check passwords
		found_user = found_users.first()
		if bcrypt.checkpw(request.POST['password'].encode(), found_user.password.encode()) == True:
			#we are logged in
			request.session['user_id'] = found_user.id
			request.session['user_name'] = found_user.name
			print found_user
			return redirect('/dashboard')
		else:
			messages.error(request, "Login Failed", extra_tags="email")
			return redirect('/main')
	else:
		messages.error(request, "Login Failed", extra_tags="email")
		return redirect('/main')
			
			