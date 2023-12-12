from django.db.models import Max
from firsttuto.models import UserTask

def get_max_order(user):
    usertask =  UserTask.objects.filter(user=user)
    if usertask.exists():
        return usertask.aggregate(Max('order'))['order__max'] + 1
    else:
        return 1
    
def reorder(user):
    task = UserTask.objects.filter(user=user)
    if not task.exists():
        return
    nbtask = task.count()
    new_order = range(1,nbtask+1)

    for order, usertask in enumerate(task):
        usertask.order = new_order[order]
        usertask.save()