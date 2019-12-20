from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from .models import Keywords
from django.contrib.auth.decorators import login_required
import json
from django.views import View


class LoginView(View):

	def get(self, request):

		if request.user.is_authenticated:
			return redirect('/users/home/')

		return render(request, 'users/auth_login.html')

	def post(self, request):
		username = request.POST.get('username')
		password = request.POST.get('password')
		ip = request.META['REMOTE_ADDR']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			if ip in settings.ALLOWED_IP_BLOCKS:
				login(request, user)
				return redirect('/users/add/')
		else:
			return render(request, 'users/auth_login.html', {'message': "Invalid Username or Password."})


@login_required
def logout_view(request):
	logout(request)
	return redirect('/users/login/')


def index(request):
	client_ip = request.META['REMOTE_ADDR']
	print(client_ip)
	return render(request, 'users/index.html')


@login_required
def add_keyword(request):
	group = request.user.groups.values_list('id', flat=True).first()
	keywords = Keywords.objects.filter(group_id=group).values('keyword', 'group_id')
	test_all = json.dumps({"data": list(keywords)})
	data = {'test_data': test_all, }
	return render(request, 'users/group_keywords.html', data)
