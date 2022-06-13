from django.contrib.auth import authenticate,login as authlogin,logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, StreamingHttpResponse
from django.views.generic import TemplateView
from django.views.decorators import gzip
from django.urls import reverse
from django.contrib.auth.models import User
from proctorweb.models import *

import cv2
import threading


def index(request):
    return render(request, "home/index.html")

@gzip.gzip_page
def camera(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam),content_type="multipart/x-mixed=replace;boundary=frame")
    except:
        pass

def login(request):
    return render(request, "account/login.html")

@login_required
def search(request):
    searchform = SearchForm();
    if request.method == "POST":
         searchform = SearchForm(request.POST)
         tests = Test.objects.filter(name__contains = searchform["search"].value()) 
         return render(request, 
         "test/search.html", 
         {"form": searchform,"search": tests})

    return render(request, "test/search.html", {"form": searchform})

@login_required
def test(request, id):
    """Здесь показываем тест"""
    questions = Question.objects.select_related('test')
    return render(request, "test/test.html", {"questions": questions})

def faq(request):
    '''Здесь страница Фаг'''
    return render(request, "home/faq.html")

def about(request):
    '''Здесь страница О нас'''
    return render(request, "home/about.html")

def instr(request):
    return render(request, "home/instr.html")

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("/")
    else:
        return HttpResponse("неавторизован")

class LoginView(TemplateView):
    template_name = "account/login.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                authlogin(request, user)
                return redirect("/")
            else:
                context['error'] = "Логин или пароль неправильные"
        return render(request, self.template_name, context)
class RegisterView(TemplateView):
    template_name = "account/register.html"
    
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            User.objects.create_user(username, email, password)
            return redirect("/")

        return render(request, self.template_name)


class VideoCamera(object):
     def __init__(self):
         self.video = cv2.VideoCapture(0)
         (self.grabbed, self.frame) = self.video.read()
         threading.Thread(target=self.update, args=()).start()
     def __del__(self):
         self.video.release()
     def get_frame(self):
         image = self.frame
         _, jpeg = cv2.imencode('.jpg', image)
         return jpeg.tobytes()

     def update(self):
         while True:
            (self.grabbed, self.frame) = self.video.read()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
