# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from .forms import UserRegForm,UserLoginForm,User,PostForm,PermissionForm
from .models import Post,PermissionAdmin
from django.views.decorators.csrf import csrf_exempt

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
	#import pdb;pdb.set_trace()
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
			#return redirect('/users')
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


def seperate_view(request):
	post = Post.objects.filter(author=request.user)

	if PermissionAdmin.objects.filter(author=request.user):
		obj = PermissionAdmin.objects.get(author=request.user)
	else:
		obj = PermissionAdmin.objects.create(author=request.user,per_read=True,per_edit=True,per_delete=True,per_create=True)
	return render(request,'seperate.html',{'post': post,'obj': obj})


def logout_view(request):
	logout(request)
	return render(request, 'logout.html', {})

@csrf_exempt
def admin_login(request):
	#import pdb;pdb.set_trace()
	title = "Admin Login"
	form = UserLoginForm(request.POST or None)

	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		if username == 'admin':
			user = authenticate(username=username, password=password)
			login(request, user)
			print(request.user.is_authenticated())		
			return render(request, 'admin_page.html', {'members': User.objects.all()})
		else:
			redirect('/controller/login/')
	return render(request,'admin_login.html',{'form': form,'title': title})


def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST or None)

		if form.is_valid():
			post = form.save(commit=False)
			#print type(request.user)
			post.author = request.user
			post.save()
			return redirect('/first_page')
	else:
		form=PostForm()
	return render(request, 'add_new.html', {'form': form})


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


def post_delete(request, pk):
	instance = Post.objects.get(pk=pk)
	instance.delete()
	return redirect('/first_page')


def permission_member(request, pk):
	#import pdb;pdb.set_trace()
	post = get_object_or_404(User, pk=pk)
	object1 = get_object_or_404(PermissionAdmin, author=post.username)

	if request.method == "POST":
		form = PermissionForm(request.POST or None,instance=object1)

		if form.is_valid():
			temp = form.save(commit=False)

			temp.author = post.username
			temp.save()
			return render(request, 'admin_page.html', {'members': User.objects.all()})
	else:
		form = PermissionForm(instance=object1)
	return render(request, 'permission.html',{'form': form})



