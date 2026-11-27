# Model欄位、驗證與資料庫型別

Model是資料契約，不只是產生表格的捷徑。

## 先從資料意義選欄位

StudyHub的Task有owner、title、description、status、priority與時間欄位。短標題使用CharField，長說明使用TextField，預計日期可為空，狀態用TextChoices。欄位型別應符合資料意義，不把所有內容都塞進文字欄位再由View猜。

`blank` 影響表單驗證，`null` 表示資料庫是否可存NULL，兩者不是相同開關。字串常以空字串表達未填，日期則可能需要NULL。預設值與自動時間欄位也要說明何時寫入。

## 驗證不會自動覆蓋所有寫入

ModelForm與Serializer可做輸入驗證，但直接 `save()` 不會自動呼叫完整 `full_clean()`。批次更新也可能略過部分Model邏輯，因此真正不可違反的資料條件應考慮資料庫約束。

先用本課Model對照migration產生的schema，理解Python屬性與資料庫欄位的連結。欄位名稱改變不只是改畫面文字，還需明確migration與舊資料處理。

## 專案中的實作

以下節錄 `examples/desk/models.py`。保留完整專案再執行；共用匯入與設定見程式包。

```python
import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator,MaxValueValidator
from django.db import models
from django.db.models import Q
from django.urls import reverse

class User(AbstractUser):
    display_name=models.CharField('顯示名稱',max_length=60,blank=True)

class Tag(models.Model):
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name=models.CharField(max_length=40)
    class Meta:
        constraints=[models.UniqueConstraint(fields=['owner','name'],name='unique_owner_tag')]
        ordering=['name','pk']
    def __str__(self):return self.name

class TaskQuerySet(models.QuerySet):
    def for_user(self,user):return self.filter(owner=user)

class Task(models.Model):
    class Status(models.TextChoices):
        TODO='todo','待開始'
        DOING='doing','進行中'
        DONE='done','已完成'
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='study_tasks')
    title=models.CharField('標題',max_length=120)
    description=models.TextField('說明',blank=True)
    status=models.CharField('狀態',max_length=8,choices=Status.choices,default=Status.TODO)
    priority=models.PositiveSmallIntegerField('優先度',default=2,validators=[MinValueValidator(1),MaxValueValidator(3)])
    due_date=models.DateField('預計日期',null=True,blank=True)
    tags=models.ManyToManyField(Tag,blank=True,related_name='tasks')
    revision=models.PositiveIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=TaskQuerySet.as_manager()
    class Meta:
        ordering=['-created_at','-pk']
        indexes=[models.Index(fields=['owner','status'],name='task_owner_status_idx')]
        constraints=[models.CheckConstraint(condition=Q(priority__gte=1,priority__lte=3),name='valid_task_priority'),
            models.CheckConstraint(condition=Q(status__in=['todo','doing','done']),name='valid_task_status')]
        permissions=[('export_task','Can export own study tasks')]
    def get_absolute_url(self):return reverse('desk:detail',kwargs={'pk':self.pk})
    def __str__(self):return self.title

def private_upload(instance,filename):return f'attachments/{uuid.uuid4().hex}.txt'

class Attachment(models.Model):
    task=models.ForeignKey(Task,on_delete=models.CASCADE,related_name='attachments')
    file=models.FileField(upload_to=private_upload)
    uploaded_at=models.DateTimeField(auto_now_add=True)

class CompletionEvent(models.Model):
    task=models.ForeignKey(Task,on_delete=models.CASCADE,related_name='completion_events')
    key=models.CharField(max_length=64)
    revision=models.PositiveIntegerField()
    class Meta:
        constraints=[models.UniqueConstraint(fields=['task','key'],name='unique_task_command')]
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/07.svg" target="_blank" rel="noopener" aria-label="放大Model欄位、驗證與資料庫型別圖解"><img src="assets/figures/07.svg" alt="Model欄位、驗證與資料庫型別：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Model欄位、驗證與資料庫型別」讀圖：數清楚一對多與多對多的方向，指出外鍵與中介表的角色。再回答：加了MinValueValidator，是否所有直接資料庫寫入都一定被擋下？</p></div>

## 自我檢查與解析

**題目：**加了MinValueValidator，是否所有直接資料庫寫入都一定被擋下？

<details><summary>展開解析</summary><p>不能如此假設。直接save或批次寫入可能不跑完整驗證；重要條件需搭配資料庫約束與測試。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/db/models/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
