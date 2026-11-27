# ModelForm與安全的欄位白名單

使用Model定義，不代表把所有欄位都開放編輯。

## 明確指定可編輯欄位

TaskForm列出title、description、status、priority、due_date與tags。owner由伺服器依登入身分填入，revision由服務管理。使用明確fields列表，避免日後Model新增敏感欄位時意外出現在表單。

`save(commit=False)` 可先取得尚未寫入的實例，補上必要欄位再存；若含多對多資料，還要在有主鍵後適當保存M2M。不能把 `commit=False` 當成自動完成所有後續動作。

## 表單建立需要使用者範圍

本課在初始化傳入user，限制tags的queryset，並清理空白標題。相同TaskForm可服務建立與編輯，但編輯時必須先以owner範圍取出實例，不能直接相信網址中的pk。

閱讀程式後，嘗試提交owner與外部tag，確認前者不會接管任務，後者會被拒絕。這比只驗證欄位是否看得到，更能支持輸入流程正確。

## 專案中的實作

以下節錄 `examples/desk/forms.py`。保留完整專案再執行；共用匯入與設定見程式包。

```python
class TaskForm(forms.ModelForm):
    class Meta:
        model=Task;fields=['title','description','status','priority','due_date','tags']
        widgets={'due_date':forms.DateInput(attrs={'type':'date'})}
    def __init__(self,*args,user,**kwargs):
        super().__init__(*args,**kwargs);self.fields['tags'].queryset=Tag.objects.filter(owner=user)
    def clean_title(self):
        title=self.cleaned_data['title'].strip()
        if not title:raise forms.ValidationError('請填寫標題。')
        return title
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/11.svg" target="_blank" rel="noopener" aria-label="放大ModelForm與安全的欄位白名單圖解"><img src="assets/figures/11.svg" alt="ModelForm與安全的欄位白名單：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「ModelForm與安全的欄位白名單」讀圖：追蹤輸入到cleaned_data，指出資料擁有權與欄位白名單在哪裡確認。再回答：把所有Model欄位自動放進表單，可能帶來什麼維護風險？</p></div>

## 自我檢查與解析

**題目：**把所有Model欄位自動放進表單，可能帶來什麼維護風險？

<details><summary>展開解析</summary><p>未來新增欄位可能自動變成可編輯輸入，讓原本只應由伺服器管理的值被暴露；明確白名單較容易審查。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/forms/modelforms/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
