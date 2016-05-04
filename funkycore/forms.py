from django import forms

class LoginForm(forms.Form):
    login = forms.CharField(label='Login', max_length=50)
    password = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput)

class TransferForm(forms.Form):
    target = forms.CharField(label='Target account', max_length=50)
    amount = forms.FloatField(label='Amount', initial=0.0)

class BuyForm(forms.Form):
    amount = forms.IntegerField(label='Amount', initial=1, widget=forms.NumberInput(attrs={'style': 'width: 48px'}))
    
class SettingsForm(forms.Form):
    nickname = forms.CharField(label='Nickname', max_length=50, required=False)
    password_old = forms.CharField(label='Current password', max_length=50, widget=forms.PasswordInput, required=False)
    password_new = forms.CharField(label='New password', max_length=50, widget=forms.PasswordInput, required=False)
    hide_sold = forms.BooleanField(label='Hide sold items', required=False)
