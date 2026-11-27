import json
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError,transaction,connection
from django.test import TestCase,Client,AsyncClient,override_settings
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from .models import Task,Tag,Attachment,CompletionEvent
from .forms import TaskForm,AttachmentForm,SignupForm
from .services import complete_task,owner_summary
from .tasks import send_study_reminder

class StudyHubTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.alice=get_user_model().objects.create_user('alice',email='alice@example.invalid',password='Strong-learn-613')
        cls.bob=get_user_model().objects.create_user('bob',password='Strong-learn-613')
        cls.task=Task.objects.create(owner=cls.alice,title='Learn Django',description='<script>alert(1)</script>')
        cls.tag=Tag.objects.create(owner=cls.alice,name='Web')
        cls.foreign_tag=Tag.objects.create(owner=cls.bob,name='Private')
    def setUp(self):cache.clear();self.client.force_login(self.alice)
    def data(self,**kw):return {'title':'New task','priority':2,'status':'todo',**kw}
    def post_api(self,url,data,client=None):return (client or self.client).post(url,json.dumps(data),content_type='application/json')

    def test_health_and_request_id(self):
        r=self.client.get('/health/');self.assertEqual(r.status_code,200);self.assertEqual(len(r['X-Request-ID']),32)
        self.assertIn("default-src 'self'",r['Content-Security-Policy'])
    def test_anonymous_redirect(self):self.assertEqual(Client().get('/tasks/').status_code,302)
    def test_login_and_post_logout(self):
        c=Client();self.assertTrue(c.login(username='alice',password='Strong-learn-613'))
        self.assertEqual(c.get('/accounts/logout/').status_code,405)
        self.assertEqual(c.post('/accounts/logout/').status_code,302)
        self.assertEqual(c.get('/tasks/').status_code,302)
    def test_login_next_does_not_redirect_external(self):
        r=Client().post('/accounts/login/?next=https://outside.invalid/',{'username':'alice','password':'Strong-learn-613'})
        self.assertEqual(r['Location'],'/tasks/')
    def test_signup_hashes_password(self):
        f=SignupForm({'username':'newlearner','password1':'Study!9-local-ABC','password2':'Study!9-local-ABC'})
        self.assertTrue(f.is_valid(),f.errors);u=f.save()
        self.assertNotEqual(u.password,'Study!9-local-ABC');self.assertTrue(u.check_password('Study!9-local-ABC'))
    def test_weak_password_rejected(self):
        f=SignupForm({'username':'newlearner','password1':'123','password2':'123'});self.assertFalse(f.is_valid())
    def test_password_reset_email_and_single_use_flow(self):
        import re
        from django.core import mail
        c=Client();r=c.post('/accounts/password_reset/',{'email':'alice@example.invalid'})
        self.assertEqual(r.status_code,302);self.assertEqual(len(mail.outbox),1)
        link=re.search(r'http://testserver(/accounts/reset/[^\s]+)',mail.outbox[0].body).group(1)
        first=c.get(link);self.assertEqual(first.status_code,302)
        form_url=first['Location'];self.assertContains(c.get(form_url),'設定新密碼')
        r=c.post(form_url,{'new_password1':'New-study!9-XYZ','new_password2':'New-study!9-XYZ'})
        self.assertEqual(r.status_code,302)
        self.assertTrue(Client().login(username='alice',password='New-study!9-XYZ'))
        self.assertFalse(c.get(link).context['validlink'])
    def test_create_owner_not_from_input(self):
        r=self.client.post('/tasks/new/',self.data(owner=self.bob.pk));self.assertEqual(r.status_code,302)
        self.assertEqual(Task.objects.get(title='New task').owner,self.alice)
    def test_invalid_form_does_not_write(self):
        before=Task.objects.count();r=self.client.post('/tasks/new/',self.data(priority=9))
        self.assertEqual(r.status_code,200);self.assertEqual(Task.objects.count(),before)
    def test_tags_are_owner_scoped(self):
        f=TaskForm(self.data(tags=[self.foreign_tag.pk]),user=self.alice);self.assertFalse(f.is_valid());self.assertIn('tags',f.errors)
    def test_tag_create_sets_owner_and_rejects_duplicate(self):
        self.assertEqual(self.client.post('/tasks/tags/',{'name':'New tag','owner':self.bob.pk}).status_code,302)
        self.assertEqual(Tag.objects.get(name='New tag').owner,self.alice)
        r=self.client.post('/tasks/tags/',{'name':'New tag'});self.assertEqual(r.status_code,200)
        self.assertContains(r,'相同名稱');self.assertEqual(Tag.objects.filter(name='New tag').count(),1)
    def test_foreign_tag_update_and_delete_denied(self):
        for action in ['edit','delete']:
            url=f'/tasks/tags/{self.foreign_tag.pk}/{action}/'
            self.assertEqual(self.client.get(url).status_code,404)
            self.assertEqual(self.client.post(url,{'name':'stolen'}).status_code,404)
        self.foreign_tag.refresh_from_db();self.assertEqual(self.foreign_tag.name,'Private')
    def test_tag_update_and_delete_preserve_task(self):
        self.task.tags.add(self.tag)
        self.assertEqual(self.client.post(f'/tasks/tags/{self.tag.pk}/edit/',{'name':'Renamed'}).status_code,302)
        self.tag.refresh_from_db();self.assertEqual(self.tag.name,'Renamed')
        self.client.post(f'/tasks/tags/{self.tag.pk}/delete/')
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists());self.assertEqual(self.task.tags.count(),0)
    def test_tag_post_requires_csrf(self):
        c=Client(enforce_csrf_checks=True);c.force_login(self.alice)
        self.assertEqual(c.post('/tasks/tags/',{'name':'CSRF missing'}).status_code,403)
    def test_foreign_detail_update_delete_and_upload_denied(self):
        self.client.force_login(self.bob)
        for suffix in ['', 'edit/','delete/']:
            with self.subTest(suffix=suffix):self.assertEqual(self.client.get(f'/tasks/{self.task.pk}/{suffix}').status_code,404)
        self.assertEqual(self.client.post(f'/tasks/{self.task.pk}/edit/',self.data()).status_code,404)
        self.assertEqual(self.client.post(f'/tasks/{self.task.pk}/delete/').status_code,404)
        self.assertEqual(self.client.post(f'/tasks/{self.task.pk}/upload/').status_code,404)
    def test_list_does_not_expose_other_owner(self):
        Task.objects.create(owner=self.bob,title='Bob secret')
        body=self.client.get('/tasks/').content.decode();self.assertNotIn('Bob secret',body)
    def test_title_and_description_are_escaped(self):
        r=self.client.get(self.task.get_absolute_url());self.assertNotContains(r,'<script>alert(1)</script>')
        self.assertContains(r,'&lt;script&gt;')
    def test_delete_get_only_confirms_post_deletes(self):
        url=reverse('desk:delete',args=[self.task.pk]);self.assertEqual(self.client.get(url).status_code,200)
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists());self.client.post(url)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
    def test_csrf_missing_rejected_and_valid_accepted(self):
        c=Client(enforce_csrf_checks=True);c.force_login(self.alice)
        self.assertEqual(c.post('/tasks/new/',self.data()).status_code,403)
        c.get('/tasks/new/');token=c.cookies['csrftoken'].value
        self.assertEqual(c.post('/tasks/new/',self.data(),HTTP_X_CSRFTOKEN=token).status_code,302)
    def test_priority_and_status_database_constraints(self):
        for values in [{'priority':8},{'status':'unknown'}]:
            with self.subTest(values=values),self.assertRaises(IntegrityError),transaction.atomic():
                Task.objects.create(owner=self.alice,title='bad',**values)
    def test_unique_tag_per_owner(self):
        with self.assertRaises(IntegrityError),transaction.atomic():Tag.objects.create(owner=self.alice,name='Web')
        Tag.objects.create(owner=self.bob,name='Web')
    def test_filter_and_pagination(self):
        for i in range(8):Task.objects.create(owner=self.alice,title=f'entry-{i}')
        r=self.client.get('/tasks/?q=entry&page=2');self.assertEqual(r.status_code,200)
        self.assertEqual(len(r.context['tasks']),3)
        self.assertEqual(self.client.get('/tasks/?status=bad').status_code,400)
    def test_select_related_removes_n_plus_one(self):
        for i in range(3):Task.objects.create(owner=self.alice,title=f'query-{i}')
        with self.assertNumQueries(1):list(t.owner.username for t in Task.objects.for_user(self.alice).select_related('owner'))
    def test_rollback_preserves_count(self):
        before=Task.objects.count()
        with self.assertRaises(RuntimeError):
            with transaction.atomic():Task.objects.create(owner=self.alice,title='rollback');raise RuntimeError()
        self.assertEqual(Task.objects.count(),before)
    def test_on_commit_invalidation(self):
        self.assertEqual(owner_summary(self.alice)['total'],1)
        with self.captureOnCommitCallbacks(execute=True):Task.objects.create(owner=self.alice,title='new')
        self.assertEqual(owner_summary(self.alice)['total'],2)
    def test_cache_does_not_mix_users(self):
        self.assertEqual(owner_summary(self.alice)['total'],1);self.assertEqual(owner_summary(self.bob)['total'],0)
    def test_repeated_command_is_idempotent(self):
        a,first=complete_task(user=self.alice,pk=self.task.pk,key='test-command')
        b,second=complete_task(user=self.alice,pk=self.task.pk,key='test-command')
        self.assertTrue(first);self.assertFalse(second);self.assertEqual(a.revision,b.revision)
        self.assertEqual(CompletionEvent.objects.count(),1)
    def test_invalid_command_key_rejected(self):
        for key in ['',None,'x'*65]:
            with self.assertRaises(ValueError):complete_task(user=self.alice,pk=self.task.pk,key=key)
    def test_upload_validation(self):
        for name,content in [('x.html',b'html'),('x.txt',b'\xff'),('x.txt',b'x'*65537)]:
            f=AttachmentForm(files={'file':SimpleUploadedFile(name,content)});self.assertFalse(f.is_valid())
    def test_private_download_requires_owner(self):
        r=self.client.post(reverse('desk:upload',args=[self.task.pk]),{'file':SimpleUploadedFile('note.txt',b'private')})
        self.assertEqual(r.status_code,302);item=Attachment.objects.get()
        url=reverse('desk:download',args=[item.pk]);r=self.client.get(url)
        self.assertEqual(b''.join(r.streaming_content),b'private');r.close()
        self.assertIn('attachment;',r['Content-Disposition']);self.assertEqual(r['X-Content-Type-Options'],'nosniff')
        self.client.force_login(self.bob);self.assertEqual(self.client.get(url).status_code,404)
        self.assertEqual(Client().get('/private-media/'+item.file.name).status_code,404)
    def test_delete_removes_file_after_commit(self):
        item=Attachment.objects.create(task=self.task,file=SimpleUploadedFile('n.txt',b'abc'))
        storage=item.file.storage;name=item.file.name
        self.assertTrue(storage.exists(name))
        with self.captureOnCommitCallbacks(execute=True):item.delete()
        self.assertFalse(storage.exists(name))
    def test_api_requires_authentication(self):self.assertEqual(Client().get('/api/v1/tasks/').status_code,403)
    def test_api_creates_and_validates(self):
        r=self.post_api('/api/v1/tasks/',{'title':'API task','priority':2,'owner':self.bob.pk})
        self.assertEqual(r.status_code,201);self.assertEqual(r.json()['owner'],self.alice.pk)
        self.assertEqual(self.post_api('/api/v1/tasks/',{'title':'bad','priority':9}).status_code,400)
    def test_api_foreign_read_update_delete_denied(self):
        self.client.force_login(self.bob);url=f'/api/v1/tasks/{self.task.pk}/'
        self.assertEqual(self.client.get(url).status_code,404)
        self.assertEqual(self.client.patch(url,json.dumps({'title':'stolen'}),content_type='application/json').status_code,404)
        self.assertEqual(self.client.delete(url).status_code,404)
    def test_api_foreign_tags_rejected(self):
        self.assertEqual(self.post_api('/api/v1/tasks/',{'title':'bad','tags':[self.foreign_tag.pk]}).status_code,400)
    def test_api_session_csrf_enforced(self):
        c=Client(enforce_csrf_checks=True);c.force_login(self.alice)
        self.assertEqual(self.post_api('/api/v1/tasks/',{'title':'bad'},c).status_code,403)
    def test_api_pagination_contract(self):
        r=self.client.get('/api/v1/tasks/');self.assertEqual(set(r.json()),{'count','next','previous','results'})
    def test_permission_export(self):
        self.assertEqual(self.client.get('/tasks/export/').status_code,403)
        self.alice.user_permissions.add(Permission.objects.get(codename='export_task'))
        self.assertEqual(self.client.get('/tasks/export/').status_code,200)
    def test_admin_staff_sees_only_own_rows(self):
        self.alice.is_staff=True;self.alice.save()
        for code in ['view_task','change_task']:
            self.alice.user_permissions.add(Permission.objects.get(codename=code))
        Task.objects.create(owner=self.bob,title='admin-foreign-secret')
        r=self.client.get('/admin/desk/task/');self.assertEqual(r.status_code,200);self.assertNotContains(r,'admin-foreign-secret')
    def test_immediate_task_is_inline(self):
        from django.core import mail
        r=send_study_reminder.enqueue('local@example.invalid','Learn')
        self.assertEqual(r.return_value,1);self.assertEqual(len(mail.outbox),1)
    def test_seed_command_is_repeatable(self):
        from django.core.management import call_command
        from io import StringIO
        call_command('seed_demo',username='alice',stdout=StringIO());n=Task.objects.count()
        call_command('seed_demo',username='alice',stdout=StringIO());self.assertEqual(Task.objects.count(),n)
    def test_fetch_raise_new_api(self):
        from demo_core import run
        self.assertTrue(run(24)['deferred_access_blocked'])
    def test_all_24_real_examples(self):
        from demo_core import run
        for i in range(1,25):
            with self.subTest(example=i):self.assertIsInstance(run(i),dict)
