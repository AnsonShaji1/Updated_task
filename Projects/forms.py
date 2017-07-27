from django import forms
from .models import Post,PermissionAdmin

from django.contrib.auth import(
		authenticate,
		get_user_model,
		login,
		logout,
	)

User=get_user_model()


class UserRegForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput, label="Password")
	password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
	
	class Meta:
		model = User
		fields = [
			'username',
			'password',
			'password1',
		]

	def clean_password1(self):
		password = self.cleaned_data.get('password')
		password1 = self.cleaned_data.get('password1')

		if password != password1:
			raise forms.ValidationError("Password must match")
		return password

	def clean_username(self):
		username = self.cleaned_data.get('username')
		user_qs = User.objects.filter(username=username)

		if user_qs.exists():
			raise forms.ValidationError("This username already registered")
		return username


class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')

		if username and password:
			user = authenticate(username=username, password=password)
			
			if not user:
				raise forms.ValidationError("This user does not exist.Please check username or password")
		return super(UserLoginForm,self).clean(*args,**kwargs)


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title','text')


class PermissionForm(forms.ModelForm):
	per_read = forms.BooleanField(initial=False, required=False,label="Read")
	per_edit = forms.BooleanField(initial=False, required=False,label="Edit")
	per_delete = forms.BooleanField(initial=False, required=False,label="Delete")
	per_create = forms.BooleanField(initial=False, required=False,label="Create")

	class Meta:
		model = PermissionAdmin
		fields = [
					'per_read',
					'per_edit',
					'per_delete',
					'per_create',
				]
