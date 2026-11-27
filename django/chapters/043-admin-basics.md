# Admin的模型管理與操作體驗

快速得到後台，仍需規劃可見欄位與編輯範圍。

## 註冊模型與調整列表

ModelAdmin可指定list_display、list_filter、search_fields及readonly_fields。StudyHub顯示title、owner、status與時間，讓管理者不用逐筆打開。關聯欄位會影響查詢，列表也可使用list_select_related改善單值關聯載入。

後台不是網站所有產品流程的替代。一般使用者的任務建立與附件頁仍由獨立View與Template提供，避免讓所有人直接進Admin，只為了省掉前台介面。

## 先限制能改什麼

revision與建立時間等伺服器管理欄位應只讀；非superuser的owner也不應自由切換。管理動作涉及批次更新時，重新確認驗證、signals、快取與授權，不能假設每個action都等同逐筆save。

先使用自己建立的superuser查看，再建立只具必要模型權限的staff帳號比較。後台能登入、能看到模型、能看到哪些列、能改哪些欄位，是不同的驗收項目。

## 專案中的實作

以下節錄 `examples/desk/admin.py`。保留完整專案再執行；共用匯入與設定見程式包。

```python
class TaskAdmin(admin.ModelAdmin):
    list_display=['title','owner','status','priority','updated_at']
    list_filter=['status','priority'];search_fields=['title','owner__username'];list_select_related=['owner']
    readonly_fields=['revision','created_at','updated_at'];filter_horizontal=['tags']
    def get_queryset(self,request):
        qs=super().get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(owner=request.user)
    def get_readonly_fields(self,request,obj=None):
        return self.readonly_fields if request.user.is_superuser else [*self.readonly_fields,'owner']
    def save_model(self,request,obj,form,change):
        if not request.user.is_superuser:obj.owner=request.user
        super().save_model(request,obj,form,change)
    def formfield_for_manytomany(self,db_field,request,**kwargs):
        if db_field.name=='tags' and not request.user.is_superuser:kwargs['queryset']=Tag.objects.filter(owner=request.user)
        return super().formfield_for_manytomany(db_field,request,**kwargs)
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/15.svg" target="_blank" rel="noopener" aria-label="放大Admin的模型管理與操作體驗圖解"><img src="assets/figures/15.svg" alt="Admin的模型管理與操作體驗：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Admin的模型管理與操作體驗」讀圖：沿staff、模型權限與資料範圍三道檢查，找出後台可看的資料。再回答：啟用staff旗標，是否就自動取得所有模型修改權限？</p></div>

## 自我檢查與解析

**題目：**啟用staff旗標，是否就自動取得所有模型修改權限？

<details><summary>展開解析</summary><p>不是。staff資格、模型權限與資料範圍都要分別設計；superuser則具有不同的管理能力。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/ref/contrib/admin/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
