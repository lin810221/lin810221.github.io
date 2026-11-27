# 上傳文字附件：驗證與儲存

限制示範範圍，不把副檔名檢查當成通用檔案安全方案。

## 接收檔案的完整路徑

HTML表單使用multipart編碼，View將request.FILES交給表單。StudyHub只接受有限大小的UTF-8文字檔，重新產生儲存名稱，不用用戶提交的檔名當路徑。這是刻意縮小的教學格式，不是任意PDF或圖片上傳系統。

副檔名、MIME與內容驗證各有侷限；需要處理更多類型時，需按格式建立解析、惡意內容檢查與資源限制。不能把允許清單加長後就宣稱同樣安全。

## 資料庫列與儲存物件不同

FileField保存檔案參照與儲存介面，內容可能在本機或外部儲存。資料庫交易不會自動回復所有檔案操作；儲存成功但DB失敗等情況可能留下孤兒檔，需明確清理與稽核策略。

本課透過伺服器指定Task與owner，大小與內容錯誤回表單提示。使用記憶體storage可在測試中驗證流程，不代表已驗收任何外部物件儲存服務。

## 專案中的實作

以下節錄 `examples/desk/forms.py`。保留完整專案再執行；共用匯入與設定見程式包。

```python
class AttachmentForm(forms.ModelForm):
    class Meta:model=Attachment;fields=['file']
    def clean_file(self):
        upload=self.cleaned_data['file']
        if Path(upload.name).suffix.lower()!='.txt':raise forms.ValidationError('本示範只接受UTF-8文字檔。')
        if upload.size>65536:raise forms.ValidationError('檔案不可超過64 KiB。')
        content=upload.read(65537);upload.seek(0)
        try:content.decode('utf-8')
        except UnicodeDecodeError:raise forms.ValidationError('檔案必須是UTF-8文字。')
        return upload
```

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/15.svg" target="_blank" rel="noopener" aria-label="放大上傳文字附件：驗證與儲存圖解"><img src="assets/figures/15.svg" alt="上傳文字附件：驗證與儲存：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「上傳文字附件：驗證與儲存」讀圖：沿staff、模型權限與資料範圍三道檢查，找出後台可看的資料。再回答：檔名結尾是.txt，是否就能信任內容？</p></div>

## 自我檢查與解析

**題目：**檔名結尾是.txt，是否就能信任內容？

<details><summary>展開解析</summary><p>不能。仍需大小與內容驗證；本課還限制UTF-8且以附件下載，不宣稱適用所有檔案類型。</p></details>

## 離線實作

在下載包 `examples` 目錄執行 `python 17_private_upload.py`。入口使用真實Django、記憶體SQLite與合成資料，不連外部服務；完整網站則由 `manage.py runserver` 啟動。

<!-- example:17_private_upload.py -->

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/files/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
