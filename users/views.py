from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout

import base64 
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from Crypto.Random import get_random_bytes #only for AES CBC mode

from .models import Results
from django.contrib.auth.models import User

#encryption functions
def decrypt(key, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
        return unpad(cipher.decrypt(enc),16)

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "users/user.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "users/login.html", {
                "message": "Invalid credentials."
            })

    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {
        "message": "Log out."
    })

def play_game(request):
    return render(request, "users/play.html", {

    })

def results(request):
     if request.method == "POST":
         csrf_token = request.POST["csrfmiddlewaretoken"]
         data = request.POST["data"]
         
         key_text = csrf_token[:16]
         key = key_text.upper()
         
         decrypted = decrypt(key, data)
         json_object = json.loads(decrypted.decode("utf-8", "ignore"))

         timing = json_object['time']
         score = json_object['score']

         if (score == '10'):
            user = User.objects.get(username=request.user.username)
            result = Results.objects.create(nickname=user, time=timing,score=score)
            result.save()
            return render(request, "users/results.html", {
                "results": Results.objects.all()
            })
         else:
            return render(request, "users/results.html", {
                 "results": Results.objects.all()
            })
     else: 
        return render(request, "users/results.html", {
            "results": Results.objects.all()
        })