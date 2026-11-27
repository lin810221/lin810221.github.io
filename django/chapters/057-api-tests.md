# API測試與越權回歸

把使用者、資料與輸入矩陣一起建立。

## 正常功能與拒絕條件

測試JSON解析、Serializer欄位、唯讀值、分頁與狀態；另外測匿名、外部owner、其他人的tag與物件ID。使用force_authenticate等工具時，需理解哪些認證步驟被跳過，不能把便利工具當成整個登入流程驗收。

本課使用真實Session登入條件與CSRF Client，讓HTML與API的cookie情境保持明確。若未來加入token方案，另增加token有效、過期、撤銷與錯誤授權測試。

## 拒絕之後資料不變

跨帳號PATCH或DELETE應拒絕，且任務內容或存在性不變。建立回應的owner必須來自伺服器；資料庫完整性與回應欄位一起檢查。不能因API回404就假設它完全沒有先寫入。

對同一條測試故意移除owner篩選，確認測試會失敗，能幫你判斷測試是否真正驗證授權。這比大量只確認200的測試更能預防回歸。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/19.svg" target="_blank" rel="noopener" aria-label="放大API測試與越權回歸圖解"><img src="assets/figures/19.svg" alt="API測試與越權回歸：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「API測試與越權回歸」讀圖：由資料模型到HTTP層讀測試範圍，指出這個單元能驗證的責任。再回答：用戶提交另一個owner，API忽略它並建立自己的資料，測試應檢查什麼？</p></div>

## 自我檢查與解析

**題目：**用戶提交另一個owner，API忽略它並建立自己的資料，測試應檢查什麼？

<details><summary>展開解析</summary><p>檢查實際DB與回應owner是登入者，並確認沒有對外部帳號產生關聯或副作用。</p></details>

## 官方來源

[對應官方文件](https://www.django-rest-framework.org/api-guide/testing/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
