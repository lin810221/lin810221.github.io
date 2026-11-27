# Form、is_valid與cleaned_data

先驗證再使用輸入，錯誤也是正常流程的一部分。

## Bound與unbound表單

第一次顯示通常是未綁定表單，提交後以request資料建立bound form。呼叫 `is_valid()` 後，通過的值放在 `cleaned_data`，錯誤則留給畫面呈現。不要跳過驗證直接使用request原始字串。

欄位轉型、單欄位clean與跨欄位clean有不同責任。輸入日期、數值或選項都可能不合法，應回到同一張表單顯示錯誤並保留可用內容，不將使用者輸入錯誤一律變成500。

## 驗證與授權一起考慮

合法的資料型別仍可能是不允許的物件ID。tag是ModelChoice類欄位時，要將queryset限制到目前使用者，不能讓選單隱藏別人的tag，但提交ID仍被接受。

用不存在、格式錯誤與屬於別人的ID分別測試，能區分資料存在性和權限。表單的輸入白名單也應明寫，不讓owner或revision等欄位由使用者控制。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/11.svg" target="_blank" rel="noopener" aria-label="放大Form、is_valid與cleaned_data圖解"><img src="assets/figures/11.svg" alt="Form、is_valid與cleaned_data：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Form、is_valid與cleaned_data」讀圖：追蹤輸入到cleaned_data，指出資料擁有權與欄位白名單在哪裡確認。再回答：只限制前端下拉選單，是否就能防止提交別人的tag ID？</p></div>

## 自我檢查與解析

**題目：**只限制前端下拉選單，是否就能防止提交別人的tag ID？

<details><summary>展開解析</summary><p>不能。用戶可自行修改請求，伺服器表單必須限制可接受的queryset並驗證。</p></details>

## 離線實作

在下載包 `examples` 目錄執行 `python 11_form_scope.py`。入口使用真實Django、記憶體SQLite與合成資料，不連外部服務；完整網站則由 `manage.py runserver` 啟動。

<!-- example:11_form_scope.py -->

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/forms/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
