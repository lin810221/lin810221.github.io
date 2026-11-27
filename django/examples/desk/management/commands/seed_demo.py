from django.core.management.base import BaseCommand,CommandError
from django.contrib.auth import get_user_model
from desk.models import Task,Tag

class Command(BaseCommand):
    help='Add deterministic example tasks to an EXISTING user; never creates credentials.'
    def add_arguments(self,parser):parser.add_argument('--username',required=True)
    def handle(self,*args,**options):
        try:user=get_user_model().objects.get(username=options['username'])
        except get_user_model().DoesNotExist:raise CommandError('Create the user first with createsuperuser or signup')
        tag,_=Tag.objects.get_or_create(owner=user,name='Django')
        for title in ['理解請求流程','完成第一個表單','驗證資料擁有權']:
            task,_=Task.objects.get_or_create(owner=user,title=title,defaults={'description':'原創合成練習資料'})
            task.tags.add(tag)
        self.stdout.write(self.style.SUCCESS('Seed complete; safe to run again.'))
