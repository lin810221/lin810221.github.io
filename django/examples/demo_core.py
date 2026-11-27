"""24 offline experiments against the REAL Django application, using in-memory SQLite."""
import os,json,asyncio
os.environ.setdefault('DJANGO_SETTINGS_MODULE','studyhub.testing')
import django
django.setup()
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.test import Client,AsyncClient
from django.db import connection,transaction,IntegrityError
from django.db.models import Count,Q
from django.test.utils import CaptureQueriesContext
from django.core.cache import cache
from django.template import Template,Context
from django.urls import reverse,resolve
from django.core.files.uploadedfile import SimpleUploadedFile
from desk.models import Task,Tag,Attachment
from desk.forms import TaskForm,AttachmentForm
from desk.services import complete_task,owner_summary
from desk.tasks import send_study_reminder

_ready=False
def initialize():
    global _ready
    if not _ready:
        if 'desk_task' not in connection.introspection.table_names():
            call_command('migrate',verbosity=0,interactive=False)
        _ready=True

def sample():
    initialize();cache.clear()
    user,_=get_user_model().objects.get_or_create(username='demo-alice',defaults={'email':'alice@example.invalid'})
    other,_=get_user_model().objects.get_or_create(username='demo-bob')
    task,_=Task.objects.get_or_create(owner=user,title='Understand Django')
    return user,other,task

def run(number):
    user,other,task=sample();client=Client();client.force_login(user)
    if number==1:return {'django':django.get_version(),'status':client.get('/health/').json(),'database':'in-memory SQLite'}
    if number==2:
        url=reverse('desk:detail',kwargs={'pk':task.pk});match=resolve(url)
        return {'url':url,'name':match.view_name,'parameters':match.kwargs}
    if number==3:
        r=client.get(task.get_absolute_url());return {'status':r.status_code,'request_id_length':len(r['X-Request-ID'])}
    if number==4:return {'rendered':Template('{{ text }}').render(Context({'text':'<script>demo</script>'}))}
    if number==5:
        tag,_=Tag.objects.get_or_create(owner=user,name='Django');task.tags.add(tag)
        return {'owner':task.owner.username,'tags':list(task.tags.values_list('name',flat=True))}
    if number==6:
        try:
            with transaction.atomic():Task.objects.create(owner=user,title='bad',priority=9)
        except IntegrityError:return {'database_constraint_rejected':True}
        raise AssertionError('database failed to enforce priority')
    if number==7:return {'sql':str(Task.objects.for_user(user).filter(status='todo').query),'count':Task.objects.for_user(user).count()}
    if number==8:
        for i in range(4):Task.objects.get_or_create(owner=user,title=f'query-example-{i}')
        with CaptureQueriesContext(connection) as naive:list(x.owner.username for x in Task.objects.for_user(user))
        with CaptureQueriesContext(connection) as optimized:list(x.owner.username for x in Task.objects.for_user(user).select_related('owner'))
        return {'naive_queries':len(naive),'optimized_queries':len(optimized),'rows':Task.objects.for_user(user).count()}
    if number==9:return Task.objects.for_user(user).aggregate(total=Count('pk'),done=Count('pk',filter=Q(status='done')))
    if number==10:
        before=Task.objects.count()
        try:
            with transaction.atomic():Task.objects.create(owner=user,title='rolled-back');raise RuntimeError('demo rollback')
        except RuntimeError:pass
        return {'before':before,'after':Task.objects.count()}
    if number==11:
        foreign=Tag.objects.create(owner=other,name=f'foreign-{Tag.objects.count()}')
        form=TaskForm({'title':'test','priority':2,'status':'todo','tags':[foreign.pk]},user=user)
        return {'valid':form.is_valid(),'errors':list(form.errors)}
    if number==12:
        r=client.post(reverse('desk:create'),{'title':'From form','priority':2,'status':'todo'})
        return {'status':r.status_code,'location':r['Location'],'owner':Task.objects.get(title='From form',owner=user).owner.username}
    if number==13:return {'anonymous':Client().get('/tasks/').status_code,'owner':client.get(task.get_absolute_url()).status_code}
    if number==14:
        client.force_login(other);return {'foreign_detail':client.get(task.get_absolute_url()).status_code,
            'foreign_api':client.get(f'/api/v1/tasks/{task.pk}/').status_code}
    if number==15:
        guarded=Client(enforce_csrf_checks=True);guarded.force_login(user)
        return {'post_without_csrf':guarded.post(reverse('desk:create'),{'title':'unsafe'}).status_code}
    if number==16:
        c=Client(enforce_csrf_checks=True);c.force_login(user);c.get('/tasks/new/')
        token=c.cookies['csrftoken'].value
        return {'status':c.post('/tasks/new/',{'title':'CSRF-safe','priority':2,'status':'todo'},HTTP_X_CSRFTOKEN=token).status_code}
    if number==17:
        form=AttachmentForm(files={'file':SimpleUploadedFile('note.txt','學習筆記'.encode())})
        if not form.is_valid():raise AssertionError(form.errors)
        item=form.save(commit=False);item.task=task;item.save();r=client.get(reverse('desk:download',args=[item.pk]))
        body=b''.join(r.streaming_content);r.close();return {'status':r.status_code,'body':body.decode(),'attachment':r['Content-Disposition']}
    if number==18:
        r=client.post('/api/v1/tasks/',data=json.dumps({'title':'From API','priority':2}),content_type='application/json')
        return {'status':r.status_code,'data':r.json()}
    if number==19:return {'status':client.get('/api/v1/tasks/').status_code,'keys':list(client.get('/api/v1/tasks/').json())}
    if number==20:
        a=owner_summary(user);b=owner_summary(other);return {'owner':a,'other':b,'cache_keys_include_owner':True}
    if number==21:
        result=send_study_reminder.enqueue('learner@example.invalid','local task')
        return {'status':str(result.status),'sent':result.return_value,'backend':'ImmediateBackend: inline, not background worker'}
    if number==22:
        a,created=complete_task(user=user,pk=task.pk,key='same-request');b,repeated=complete_task(user=user,pk=task.pk,key='same-request')
        return {'first':created,'repeated':repeated,'same_revision':a.revision==b.revision}
    if number==23:
        r=asyncio.run(AsyncClient().get('/async-health/'));return {'status':r.status_code,'data':r.json()}
    if number==24:
        # Django 6.1 fetch modes: inspect installed API before changing this example.
        from django.db.models import FETCH_RAISE
        from django.core.exceptions import FieldFetchBlocked
        item=Task.objects.only('pk').fetch_mode(FETCH_RAISE).get(pk=task.pk)
        try:item.title
        except FieldFetchBlocked:return {'deferred_access_blocked':True}
        raise AssertionError('fetch mode did not block deferred access')
    raise ValueError('example number must be 1..24')

def cli(number):print(json.dumps(run(number),ensure_ascii=False,indent=2))
