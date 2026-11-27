# Serializer的輸入驗證與唯讀欄位

序列化、驗證及建立更新具有不同責任。

## 明確定義API欄位

TaskSerializer列出id、owner、title、狀態等欄位，並將id、owner、revision設為唯讀。ModelSerializer可利用Model資訊建立欄位，但仍需核對暴露範圍，不用全部欄位作為公開API契約。

建立時先驗證，再由View的perform_create設定owner。用戶提交別人的owner不應接管資料，其他伺服器管理欄位也不能因為在JSON中出現就被採用。

## 關聯ID的範圍

tags欄位的可選queryset依request.user限制，拒絕其他帳號的tag。這與主物件的object permission不同，兩個層次都需要。序列化時也要避免多值關聯造成每列額外查詢。

本課測試正常建立、非法priority、偽造owner及外部tag。若日後加入巢狀寫入，要明確定義新增、更新、刪除及交易邊界，不能假設ModelSerializer會自動猜出全部語意。

## 專案中的實作

以下節錄 `examples/desk/api.py`。保留完整專案再執行；共用匯入與設定見程式包。

```python
from rest_framework import serializers,viewsets,permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task,Tag
from .services import complete_task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model=Task;fields=['id','owner','title','description','status','priority','due_date','tags','revision']
        read_only_fields=['id','owner','revision']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        user=self.context['request'].user
        self.fields['tags'].child_relation.queryset=Tag.objects.filter(owner=user) if user.is_authenticated else Tag.objects.none()

class IsOwner(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):return obj.owner_id==request.user.pk

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class=TaskSerializer;permission_classes=[permissions.IsAuthenticated,IsOwner]
    def get_queryset(self):
        qs=Task.objects.for_user(self.request.user).select_related('owner').prefetch_related('tags')
        status=self.request.query_params.get('status')
        if status:
            if status not in Task.Status.values:raise serializers.ValidationError({'status':'Unknown choice'})
            qs=qs.filter(status=status)
        return qs
    def perform_create(self,serializer):serializer.save(owner=self.request.user)
    @action(detail=True,methods=['post'])
    def complete(self,request,pk=None):
        self.get_object()
        try:task,created=complete_task(user=request.user,pk=pk,key=request.data.get('key',''))
        except ValueError as exc:raise serializers.ValidationError({'key':str(exc)})
        return Response({'id':task.pk,'status':task.status,'revision':task.revision,'created':created})
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/17.svg" target="_blank" rel="noopener" aria-label="放大Serializer的輸入驗證與唯讀欄位圖解"><img src="assets/figures/17.svg" alt="Serializer的輸入驗證與唯讀欄位：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Serializer的輸入驗證與唯讀欄位」讀圖：追蹤JSON輸入到Serializer，再檢查哪些欄位由伺服器決定。再回答：把owner設成唯讀後，建立時應由誰填入？</p></div>

## 自我檢查與解析

**題目：**把owner設成唯讀後，建立時應由誰填入？

<details><summary>展開解析</summary><p>由伺服器根據已驗證使用者設定；不能重新從request原始字典取回可偽造值。</p></details>

## 官方來源

[對應官方文件](https://www.django-rest-framework.org/api-guide/serializers/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
