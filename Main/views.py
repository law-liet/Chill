from django.shortcuts import render
from Main.models import User, Group, Message
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def register(request):
    email = request.POST['email']
    first_name = request.POST['first']
    last_name = request.POST['last']
    fb_token = request.POST['fb']
    data = {}
    try:
        User.objects.get(email = email)
        data['status'] = "Email Already Exist"
        return JsonResponse(data)
    except ObjectDoesNotExist:
        user = User.objects.create(first_name = first_name, last_name = last_name, fb_token= fb_token, email=email)
        user.save()
        data['status'] = "Succeed"
        return JsonResponse(data)

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

def join_chilled(request):
    user = request.POST['email']
    chiller = request.POST['chiller']
    data = {}
    try:
        user = User.objects.get(email=user)
        chiller = User.objects.get(email=chiller)
        group = Group.objects.get(chiller = chiller)
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

def create_chill(request):
    pass

def toggle_chill(request):
    email = request.POST['email']
    user = User.objects.get(email = email)
    user.switch_chilled()

def send_message(request):
    sender = request.POST['sender']
    group = request.POST['group']
    content = request.POST['message']
    data = {}
    try:
        user = User.objects.get(email = sender)
        group = Group.objects.get(chiller = group)
        new_msg = Message.objects.create(sender=user,content=content)
        new_msg.save()
        group.messages.add(new_msg)
        group.save()
        data['status'] = 'Succeed'

    except ObjectDoesNotExist:
        data['status'] = 'The group or user does not exist'

    return JsonResponse(data)


def receive_message(request):
    group = request.POST['group']
    data = {}
    try:
        group = Group.objects.get(email=group)
        data['messages'] = group.messages
        data['status'] = 'Succeed'

    except ObjectDoesNotExist:
        data['status'] = 'Group does not exist'

    return JsonResponse(data)
