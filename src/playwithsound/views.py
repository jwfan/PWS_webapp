from django.shortcuts import render,redirect,get_object_or_404
from django.templatetags.static import static

from django.http import Http404, HttpResponse, JsonResponse
from django.conf import settings
from django.urls.base import reverse
from django.db import transaction

from wsgiref.util import FileWrapper

from playwithsound.models import *
from playwithsound.forms import *

# Used to create and manually log in a user
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

import os

# Create your views here.
def home(request):
    context={}
    return render(request, 'index.html', context)


# Action when people click register button.
@transaction.atomic
def register(request):
    context = {}

    if request.method == "GET":
        context['form'] = RegistrationForm()
        return render(request, 'register.html', context)

    form = RegistrationForm(request.POST)

    context['form'] = form
    if not form.is_valid():
        return render(request, 'registration.html', context)
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        first_name=form.cleaned_data['firstname'],
                                        last_name=form.cleaned_data['lastname'],
                                        password=form.cleaned_data['password1'],
                                        email=form.cleaned_data['email'],
                                        is_active=False
                                        )
    new_user.save()
    Album(user=new_user,album_name="Default").save()
    uidb64 = urlsafe_base64_encode(force_bytes(new_user.pk))
    token = default_token_generator.make_token(new_user)
    email_body = """Welcome to PLAY WITH SOUND! Please click the link below to verify you 
    email address and complete the registration of your account:

    http://%s%s
    """ % (request.get_host(),
           reverse('confirm-email', args=(uidb64, token)))

    send_mail(subject="Verify your email address in Grumblr",
              message=email_body,
              from_email="oreoztl@gmail.com",
              recipient_list=[new_user.email])
    context['email'] = form.cleaned_data['email']
    return render(request, 'registration/needemailvalidation.html', context)


@transaction.atomic
def registeration_confirm(request, uidb64, token):
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.filter(pk=uid)[0]
    # Verify if input uidb64 corresponds to a existed user
    if not user:
        return render(request, 'grumblr/templates/registration/needemailvalidation.html', {})
    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect(reverse('index'))
    else:
        return render(request, 'grumblr/templates/registration/needemailvalidation.html', {})


def mode_1(request):
    context={}
    return render(request, 'modes/mode1.html', context)

def mode_2(request):
    context={}
    return render(request, 'modes/mode2.html', context)

def mode_3(request):
    context={}
    return render(request, 'modes/mode3.html', context)

def login(request):
    context={}
    return render(request,'login.html',context)

def logout(request):
    logout(request)
    return redirect(reverse('home'))

# get the static audio file for convolver
def get_conv_audio(request):
    # the url of the file
    file_url=os.path.join(settings.STATIC_ROOT, 'playwithsound', 'audio', 'abernyte_grain_silo_ir_edit.wav')
    f = open(file_url,"rb")
    response = HttpResponse()
    response.write(f.read())
    response['Content-Type'] ='audio/wav'
    response['Content-Length'] = os.path.getsize(file_url)
    print(os.path.getsize(file_url))
    return response

# homepage of gallery
def gallery_home(request):
    context={}
    return render(request, 'gallery/gallery_home.html', context)

def gallery_view(request, page):
    context={}
    return render(request, 'gallery/gallery_view_more.html', context)

def gallery_my_album(request):
    context={}
    return render(request, 'gallery/gallery_my_album.html', context)

def saveimage(request):
    imagefile= request.FILES['ImageData']
    audiofile=request.FILES['AudioData']

    #file=open("/Users/flora/Desktop/mioamiao.wav","wb")
    #file.writelines(audiofile.readlines())
    return HttpResponse()