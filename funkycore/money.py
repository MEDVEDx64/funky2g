from django.contrib.auth.models import User

import models

# Returns: Transaction object or None; error_message
def transfer(login_src, login_dst, amount):
    src = User.objects.filter(username=login_src)
    if len(src) == 0:
        return (None, 'Source account does not exist.')
    user_src = src[0]
    
    dst = User.objects.filter(username=login_dst)
    if len(dst) == 0:
        return (None, 'Target account does not exist.')
    user_dst = dst[0]

    if login_src == login_dst:
        return (None, 'Destination and source are the same account')
    if amount < 0:
        return (None, 'Invalid amount specified.')
    if amount > user_src.userprofile.balance:
        return (None, 'Not enough money.')
    
    user_src.userprofile.balance -= amount
    user_dst.userprofile.balance += amount
    user_src.userprofile.save()
    user_dst.userprofile.save()
    
    tn = models.Transaction(
        source = user_src,
        destination = user_dst,
        amount = amount
    )
    tn.save()
    return (tn, 'Success.')
