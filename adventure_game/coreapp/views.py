from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import auth, messages
from django.core.context_processors import csrf #user security
from django.contrib.auth.models import User
from django.template import RequestContext
from .models import Level_num, Game_saved
from .queries import get_logged_in_char, get_all_characters
from .utilities import  get_profile_context
from django.core.exceptions import PermissionDenied
import json

def home(request):
    context = {}
    context.update(csrf(request))
    return render_to_response('coreapp/home.html',
                              context,
                              context_instance=RequestContext(request))

def profile(request):
    user = request.user
    characters = get_all_characters(user)
    if get_logged_in_char(characters):
        context = get_profile_context(user, characters)
        return render(request, 'coreapp/individual.html', context)
    else:
        family_members = characters
        userlname = user.last_name
        context = {'family_members' : family_members,
                   'lastname' : userlname,
                  }
        return render(request, 'coreapp/profile.html', context)

def story(request):
    """
    Renders the story.html template when users access this route.
    """
    return render(request, 'coreapp/story.html')

def auth_view(request):
    """
    The user is sent to this page after they login for authentication.
    They are then redirected to the home page.
    """
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            messages.success(request, 'Hi %s, you have successfully logged in.' %(user.last_name))
            return HttpResponseRedirect('/')
        else:
            messages.success(request, 'Your account has been banned,' \
                             ' please contact us to re-activate your account!')
            return HttpResponseRedirect('/')
    else:
        messages.success(request, 'The account you entered is invalid, please try again!')
        return HttpResponseRedirect('/')

def logout(request):
    """
    The user is sent here when they logout. They are then redirected to the home page.
    """
    auth.logout(request)
    messages.success(request, 'You have successfully logged out.')
    return HttpResponseRedirect('/')

def registration_submission(request):
    """
    A visitor is sent to this page when they submit their registration.
    After being registered they are redirected to the home page.
    """
    username = request.POST.get('username', '')
    firstname = request.POST.get('firstname', '')
    lastname = request.POST.get('lastname', '')
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    if len(User.objects.filter(username=username)) != 0: #pylint: disable=E1101
        return registration(request, "Try again, the username %s %s."
                            % (username, "is already taken"))
    if len(User.objects.filter(email=email)) != 0: #pylint: disable=E1101
        return registration(request, "Try again, %s %s."
                            % ("there is already an account with that email", email))
    user = User.objects.create_user(username=username, email=email, password=password,
                                    first_name=firstname, last_name=lastname) #pylint: disable=E1101
    Level_num.objects.create(user=user, user_point=0, user_level=1)
    Game_saved.objects.create(user=user, adventure_saved="", task_saved="")
    user = auth.authenticate(username=username, password=password)
    auth.login(request, user)
    return HttpResponseRedirect('/')

def registration(request, message=None):
    """
    A visitor can register here and submit the registration form.
    """
    context = {}
    context.update(csrf(request))
    if message is not None:
        context['message'] = message
    return render(request, 'auth/registration.html', context)

def add_family_member(request, message=None):
    """
    The user can add family members to their account here
    """
    context = {}
    context.update(csrf(request))
    if message is not None:
        context['message'] = message
    return render(request, 'auth/addfamily.html', context)

def add_family_member_submission(request):
    full_name = request.POST.get('member-name', '')
    pin = request.POST.get('member-pin', '')
    if len(pin) != 4:
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


def individual(request):
    """
    The user is sent to here after enter thier own pin # for selected member
    """
    user = request.user
    character_name = request.POST.get('character_name', '')
    character_pin = request.POST.get('character_pin', '')
    characters = get_all_characters(user)

    if get_logged_in_char(characters):
        char = get_logged_in_char(characters)[0]
        char.is_logged = False
        char.save()
        return profile(request)

    if user.character_set.filter(character_name=character_name, character_pin=character_pin):
        char = user.character_set.filter(character_name=character_name,
                                         character_pin=character_pin)[0]
        char.is_logged = True
        char.save()
        return HttpResponseRedirect('/profile/')
    else:
        messages.success(request, 'The PIN you entered is incorrect or did not' \
                         ' select your family role, please try again!')
        return HttpResponseRedirect('/profile/')

def getjson(request):
    if request.is_ajax():
        alist = [{"people":"haha", "age":"20"}, {"people":"fsd", "age":"dfsdf"}]
        return JsonResponse(alist, safe=False)
    else:
        raise PermissionDenied()


def usejson(request):

    return render(request, 'coreapp/getjson.html', {"usea":"hahah"})
