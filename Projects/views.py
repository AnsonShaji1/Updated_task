# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from .forms import UserRegForm,UserLoginForm,User,PostForm
from .models import Post,PermissionAdmin
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core import serializers


from django.contrib.auth import(
		authenticate,
		get_user_model,
		login,
		logout,
	)


def common_home(request):
	return render(request, 'home.html', {})


def member_home(request):
	return render(request, 'user_home.html', {})


def register_view(request):
	title = 'Register'
	form = UserRegForm(request.POST or None)

	if form.is_valid():
		user = form.save(commit=False)
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get('password')

		if username != 'admin':
			user.set_password(password)
			user.save()
			PermissionAdmin.objects.create(author=user.username,per_read=True,per_edit=True,per_delete=True,per_create=True)
			
			return redirect('/login/')
		else:
			pass
	return render(request, 'register.html', {'form': form, 'title': title})


def login_view(request):
	title = "User Login"
	form = UserLoginForm(request.POST or None)

	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		
		if username != 'admin':
			user = authenticate(username=username, password=password)
			login(request, user)
			print(request.user.is_authenticated())
			return redirect('/first_page')
		else:
			pass
	return render(request, 'login.html', {'form': form,'title': title})


@login_required
def seperate_view(request):
	post = Post.objects.filter(author=request.user)

	if PermissionAdmin.objects.filter(author=request.user):
		obj = PermissionAdmin.objects.get(author=request.user)
	else:
		obj = PermissionAdmin.objects.create(author=request.user,per_read=True,per_edit=True,per_delete=True,per_create=True)
	return render(request,'seperate.html',{'post': post,'obj': obj})


@login_required
def logout_view(request):
	logout(request)
	return render(request, 'logout.html', {})


@csrf_exempt
def admin_login(request):
	title = "Admin Login"
	form = UserLoginForm(request.POST or None)

	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		if username == 'admin':
			user = authenticate(username=username, password=password)
			login(request, user)
			print(request.user.is_authenticated())		
			return render(request,'first_admin.html',{'admin_user':request.user})
		else:
			return redirect('/controller/login/')
	return render(request,'admin_login.html',{'form': form,'title': title})


@login_required
def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST or None)

		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return redirect('/first_page')
	else:
		form=PostForm()
	return render(request, 'add_new.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST or None, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/first_page')
    else:
        form = PostForm(instance=post)
    return render(request, 'add_new.html', {'form': form})


@login_required
def post_delete(request, pk):
	instance = Post.objects.get(pk=pk)
	instance.delete()
	return redirect('/first_page')


@login_required
def admin_content(request,pk):
	content = get_object_or_404(User, pk=pk)
	if content.username == 'admin':
		members=PermissionAdmin.objects.all()
		if members:	
			if request.method == 'POST':
				for i in request.POST.getlist('author'):
					if i in request.POST.getlist('per_read'):
						per_read = True
					else:
						per_read = False

					if i in request.POST.getlist('per_edit'):
						per_edit = True
					else:
						per_edit = False

					if i in request.POST.getlist('per_delete'):
						per_delete = True
					else:
						per_delete = False

					if i in request.POST.getlist('per_create'):
						per_create = True
					else:
						per_create = False
					t=PermissionAdmin.objects.get(author=i)
					t.per_read=per_read
					t.per_edit=per_edit
					t.per_delete=per_delete
					t.per_create=per_create
					t.save()
				return render(request,'first_admin.html',{'admin_user':User.objects.get(username='admin')})
			else:
				json_data = serializers.serialize("json",PermissionAdmin.objects.all())
				return render(request, 'admin_page1.html', {'members': PermissionAdmin.objects.all(),"json" : json_data })
		else:
			return render(request, 'admin_page1.html',{'members': PermissionAdmin.objects.all()})
	else:
		return HttpResponse("Page not found")




