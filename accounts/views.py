from django.shortcuts import render, redirect
from django.contrib.auth import(
	authenticate,
	get_user_model,
	login,
	logout,
	)
from .forms import LoginForm, RegisterForm
# Create your views here.
def login_view(request):
	next = request.GET.get('next')
	form = LoginForm(request.POST or None)
	title = 'Login'
	if form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user = authenticate(username=username, password=password)
		login(request,user)
		if next:
			return redirect(next)
		return redirect('/posts')
	return render(request,'form.html',{'form':form, 'title':title})

def register_view(request):
	next = request.GET.get('next')
	form = RegisterForm(request.POST or None)
	title = 'Register'
	if form.is_valid():
		user = form.save(commit=False)
		username = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.save()
		new_user = authenticate(username=username, password=password)
		login(request,new_user)
		if next:
			return redirect(next)
		return redirect('/posts')
	return render(request,'form.html',{'form':form, 'title':title})

def logout_view(request):
	logout(request)
	return render(request,'form.html',{})

