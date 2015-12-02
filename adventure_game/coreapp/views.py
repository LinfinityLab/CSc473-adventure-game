from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf #user security
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from map.models import Level, Adventure
from django.contrib import messages

def home(request,message=None):
    context = {}
    context.update(csrf(request))
    return render_to_response('coreapp/home.html',context,context_instance=RequestContext(request))

@login_required(login_url='/')
def profile(request):
    characters = request.user.character_set.all()
    adventures = Adventure.objects.all()
    adventure_name_list =[]
    adventure_img_url_list = []

    for i in Adventure.objects.all():
        adventure_name_list.append(str(i.adventure_name))
        adventure_img_url_list.append(str(i.adventure_img_url))

    zipped = zip(adventure_img_url_list, adventure_name_list)
    adventure_img = "http://thesource.com/wp-content/uploads/2015/11/Kobe-.jpg"
    adventure_name = "adv_name"
    level = request.user.level_num
    if characters.filter(is_logged=True):
        character_name = characters.filter(is_logged=True)[0].character_name
        context = { 'character_name' : character_name,
                    'level' : level,
                    # 'adventure_img_url_list' : adventure_img_url_list,
                    # 'adventure_name_list' : adventure_name_list,
                    'zipped' : zipped
                  }
        return render(request, 'coreapp/individual.html', context)
    else:
        family_members = request.user.character_set.all()
        user=request.user
        userfname = user.first_name
        userlname = user.last_name
        context = {'family_members' : family_members,
                   'lastname' : userlname,
                   }
        return render(request, 'coreapp/profile.html', context)

@login_required(login_url='/')
def story(request):
    return render(request, 'coreapp/story.html')

def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            messages.success(request, 'Hi %s, you have successfully logged in.' %(user.last_name))
            return HttpResponseRedirect('/')
        else:
            messages.success(request, 'Your account has been banned, please contact us to re-active your account!')
            return HttpResponseRedirect('/')
    else:
        messages.success(request, 'The account you entered is invalid, please try again!')
        return HttpResponseRedirect('/')

@login_required(login_url='/')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You have successfully logged out.')
    return HttpResponseRedirect('/')

def registration_submission(request):
    username = request.POST.get('username', '')
    firstname = request.POST.get('firstname', '')
    lastname = request.POST.get('lastname', '')
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    if len(User.objects.filter(username=username)) != 0: #pylint: disable=E1101
        return registration(request, "Try again, the username %s %s." %(username, "is already taken"))
    if len(User.objects.filter(email=email)) != 0: #pylint: disable=E1101
        return registration(request, "Try again, %s %s." %("there is already an account with that email", email))
    user = User.objects.create_user(username=username, email=email, password=password, first_name=firstname, last_name=lastname) #pylint: disable=E1101
    level=Level.objects.create(user=user,level_number=0)
    user = auth.authenticate(username=username, password=password)
    auth.login(request, user)
    return HttpResponseRedirect('/')

def registration(request, message=None):
    context = {}
    context.update(csrf(request))
    if message is not None:
        context['message'] = message
    return render(request, 'auth/registration.html', context)

@login_required(login_url='/')
def add_family_member(request,message=None):
    context= {}
    context.update(csrf(request))
    if message is not None:
        context['message'] = message
    return render(request, 'auth/addfamily.html', context)

@login_required(login_url='/')
def add_family_member_submission(request):
    full_name = request.POST.get('member-name','')
    pin = request.POST.get('member-pin','')
    if not len(pin) == 4:
        messages.success(request, 'Please enter 4 characters as your PIN number')
        return HttpResponseRedirect('/add-family-member/')
    else:
        current_user = request.user
        if current_user.character_set.filter(character_name=full_name):
            messages.success(request, 'This member has already been added, try another name')
            return HttpResponseRedirect('/add-family-member/')
        else:
            current_user.character_set.create(character_name=full_name, character_pin=pin)
            return HttpResponseRedirect('/profile/')


@login_required(login_url='/')
def individual(request):
    user = request.user
    character_name = request.POST.get('character_name', '')
    character_pin = request.POST.get('character_pin', '')
    level = user.level_num
    characters = request.user.character_set.all()

    if characters.filter(is_logged=True):
        family_members = request.user.character_set.all()
        user=request.user
        userfname = user.first_name
        userlname = user.last_name
        context = {'family_members' : family_members,
                   'lastname' : userlname,
                   }
        char = characters.filter(is_logged=True)[0]
        char.is_logged = False
        char.save()
        return render(request, 'coreapp/profile.html', context)

    if user.character_set.filter(character_name=character_name, character_pin=character_pin):
        character_name = character_name
        context = { 'character_name' : character_name,
                  }
        char = user.character_set.all().filter(character_name=character_name, character_pin=character_pin)[0]
        char.is_logged = True
        char.save();

        return render(request, 'coreapp/individual.html', context)
    else:
        messages.success(request, 'The PIN you entered is incorrect, please try agian!')
        return HttpResponseRedirect('/profile/')
