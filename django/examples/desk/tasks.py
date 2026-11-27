from django.tasks import task
from django.core.mail import send_mail

@task
def send_study_reminder(address,title):
    return send_mail('學習提醒',f'記得安排時間完成：{title}',None,[address])
