from django.core.cache import cache
from django.db import transaction
from .models import Task,CompletionEvent

def owner_summary(user):
    key=f'desk:summary:{user.pk}'
    result=cache.get(key)
    if result is None:
        qs=Task.objects.for_user(user)
        result={'total':qs.count(),'done':qs.filter(status=Task.Status.DONE).count()}
        cache.set(key,result,30)
    return result

def invalidate_after_commit(owner_id):
    transaction.on_commit(lambda:cache.delete(f'desk:summary:{owner_id}'))

@transaction.atomic
def complete_task(*,user,pk,key):
    if not isinstance(key,str) or not key or len(key)>64:raise ValueError('key must contain 1..64 characters')
    task=Task.objects.select_for_update().for_user(user).get(pk=pk)
    event,created=CompletionEvent.objects.get_or_create(task=task,key=key,defaults={'revision':task.revision+1})
    if created:
        task.status=Task.Status.DONE;task.revision=event.revision
        task.save(update_fields=['status','revision','updated_at']);invalidate_after_commit(user.pk)
    return task,created
