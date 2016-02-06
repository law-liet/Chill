from django.shortcuts import render
from Main.models import User, Group, Message
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
import requests
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def register(request):
    email = request.POST['email']
    first_name = request.POST['firstName']
    last_name = request.POST['lastName']
    fb_token = request.POST['facebookAccessToken']
    params = {'access_token': fb_token} 
    r = requests.get('https://graph.facebook.com/me/', params= params)
    fb_id = r['id']

    data = {}
    try:
        User.objects.get(email = email)
        data['status'] = "Email Already Exist"
        return JsonResponse(data)
    except ObjectDoesNotExist:
        user = User.objects.create(first_name = first_name, last_name = last_name, fb_id = fb_id, fb_token= fb_token, email=email)
     
        r = requests.get("https://graph.facebook.com/me/friends", params=params)
        result = r.json()
        for friend in result['data']: 
            try:
                f = User.objects.get(fb_id = friend['id'])
                user.friends.add(f)
            except ObjectDoesNotExist:
                pass 
        user.save()
        data['status'] = "Succeed"
        return JsonResponse(data)

@csrf_exempt
def get_all_chilled(request):
    email = request.POST['email']
    data = {}
    try:
        user = User.objects.get(email = email)
        chilled_friends = user.friends.filter(is_chilled=True)
        data['all_chilled'] = chilled_friends
        data['status'] = "Succeed"

    except ObjectDoesNotExist:
        data['status'] = "Cannot find User"

    return JsonResponse(data)

@csrf_exempt
def join_chilled(request):
    user = request.POST['email']
    ##chiller = request.POST['chiller']
    data = {}
    try:
        user = User.objects.get(email=user)
        ##chiller = User.objects.get(email=chiller)
        group = Group.objects.get(chiller = "chill")
        if group.size < group.max_size:
            group.members.add(user)
            group.size += 1
            group.save()
            data['status'] = 'Succeed'

        else:
            data['status'] = 'No more chilled positions.'

    except ObjectDoesNotExist:
        data['status'] = 'The group or user does not exist'

    return JsonResponse(data)

@csrf_exempt
def create_chill(request):
    pass

@csrf_exempt
def toggle_chill(request):
    email = request.POST['email']
    type = request.POST['type']
    is_chilled = request.POST['isChill']
    data = {}
    try:
        user = User.objects.get(email = email)
        user.Type = type
        user.is_chilled = is_chilled
        user.save()
        data['status'] = "Succeed"
    except ObjectDoesNotExist:
        data['status'] = "No such user"

    return JsonResponse(data)


@csrf_exempt
def send_message(request):
    sender = request.POST['sender']
    group = request.POST['group']
    content = request.POST['message']
    data = {}
    try:
        user = User.objects.get(email = sender)
        group = Group.objects.get(chiller = group)
        new_msg = Message.objects.create(sender=user, name=user.first_name, content=content)
        new_msg.save()
        group.messages.add(new_msg)
        group.save()
        data['status'] = 'Succeed'

    except ObjectDoesNotExist:
        data['status'] = 'The group or user does not exist'

    return JsonResponse(data)

@csrf_exempt
def receive_message(request):
    group = request.POST.get('group', "chill")
    data = {}
    try:
        group = Group.objects.get(name=group)
        data['messages'] = group.messages.all().order_by('time')
        data['status'] = 'Succeed'

    except ObjectDoesNotExist:
        data['status'] = 'Group does not exist'

    return JsonResponse(data)
