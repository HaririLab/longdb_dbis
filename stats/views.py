from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required(login_url="/login/")
def stats(request):
	print("This page is not yet created")
