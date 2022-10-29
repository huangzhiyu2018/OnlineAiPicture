import os
import ast
import datetime
from django.shortcuts import render, HttpResponse, redirect
from django import forms
from picturerec import models
from django.http import JsonResponse
from django.conf import settings
from picturerec.utils.forms import BootrapModelForm, BootrapForm
from picturerec.utils import sklearncompute
from django.db.models import Q
from PIL import Image
import numpy as np

def scrapy_image(request):
    return render(request,"scraperimage.html")