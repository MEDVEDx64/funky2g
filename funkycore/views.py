from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, Http404
from django.conf import settings

from threading import Thread
from money import transfer

import models
import forms
import rcon

def index(request):
    msg = None
    if 'm' in request.GET:
        msg = request.GET['m']
    context = {
        'login_form': forms.LoginForm(),
        'buy_form': forms.BuyForm(),
        'message': msg,
        'items': models.Item.objects.all()
    }
    return render(request, 'funkycore/index.html', context)

def login_view(request):
    if not request.method == 'POST':
        raise Http404

    user = authenticate(username=request.POST['login'], password=request.POST['password'])
    if user and user.is_active:
        login(request, user)
        return redirect('/')
    return render_message(request, 'Invalid login.')

def logout_view(request):
    logout(request)
    return redirect('/')

def message(request):
    text = 'No message'
    if 'm' in request.GET:
        text = request.GET['m']
    return render_message(request, text)

def render_message(request, text):
    return render(request, 'funkycore/message.html', {'message': text})
    
def transfer_view(request):
    if not request.user.is_authenticated:
        raise Http404

    if request.method == 'POST':
        tn, msg = transfer(request.user.username, request.POST['target'], float(request.POST['amount']))
        ctx = {
            'form': forms.TransferForm(initial={'target': request.POST['target']}),
            'message': msg
        }
        return render(request, 'funkycore/transfer.html', ctx)
        
    else:
        return render(request, 'funkycore/transfer.html', {'form': forms.TransferForm()})

def buy(request):
    if not request.user.is_authenticated or request.method != 'POST':
        raise Http404
    
    context = {
        'buy_form': forms.BuyForm(),
        'items': models.Item.objects.all()
    }
    
    item = models.Item.objects.get(id=request.GET['item'])
    
    # Validating items amount
    amount = int(request.POST['amount']);
    if amount < 1 or amount > settings.MAX_ORDER_AMOUNT:
        context['message'] = 'Invalid amount.'
        return render(request, 'funkycore/index.html', context)
    if item.left == 0:
        context['message'] = 'Out of stock!'
        return render(request, 'funkycore/index.html', context)
    elif item.left > 0:
        if amount > item.left:
            amount = item.left
    
    # Parsing data string
    spl = item.item_string.split(' ')
    data = '0'
    if len(spl) > 1:
        data = spl[1]
        
    # Transaction
    tn, msg = transfer(request.user.username, '_bank', amount * item.price)
    if not tn:
        context['message'] = msg
        return render(request, 'funkycore/index.html', context)
    
    # Delivery
    class _sender(Thread):
        def run(self):
            rcon.ItemSender(request.user.userprofile.nickname, spl[0], amount, data).run()
            models.Order(item=item, transaction=tn).save()
    _sender().start()
    
    if item.left > 0:
        item.left -= amount
        item.save()
    context['message'] = 'You have bought: ' + item.text + ' x' + str(amount) + '.'
    return render(request, 'funkycore/index.html', context)

def settings_view(request):
    if not request.user.is_authenticated:
        raise Http404
    
    u = request.user
    if request.method == 'POST':
        form = forms.SettingsForm(request.POST)
        if len(request.POST['password_new']) > 0:
            if not u.check_password(request.POST['password_old']):
                return render(request, 'funkycore/settings.html', {'form': form, 'message': 'Wrong current password.'})
            u.set_password(request.POST['password_new'])
            u.save()
        
        if len(request.POST['nickname']) > 0:
            u.userprofile.nickname = request.POST['nickname']
        u.userprofile.hide_sold = 'hide_sold' in request.POST
        u.userprofile.save()
        return render(request, 'funkycore/settings.html', {'form': form, 'message': 'Your profile has been updated.'})
    
    form = forms.SettingsForm(initial={'nickname': u.userprofile.nickname, 'hide_sold': u.userprofile.hide_sold})
    return render(request, 'funkycore/settings.html', {'form': form})
