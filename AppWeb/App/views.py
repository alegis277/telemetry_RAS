from django.shortcuts import render,redirect,render_to_response
from django.http import HttpResponse
from django.http import Http404
import simplejson as json
import time
import threading
import numpy as np


def index(request):
	return render(request, 'index.html')
