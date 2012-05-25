# Create your views here.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from modelagem import models
from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404, redirect

def index(request):
    return render_to_response('index.html')

def origem(request):
    return render_to_response('origem.html')

def ogrupo(request):
    return render_to_response('grupo.html')
