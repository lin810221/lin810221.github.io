# REST API與HTTP資源

API不只是把模板換成JSON，還要定義輸入和錯誤。

## 以資源與方法建立契約

StudyHub提供任務集合與單一任務URL，使用GET讀取、POST建立、PATCH局部更新與DELETE刪除。路徑採版本前綴，回應包含明確欄位及狀態；不是每個操作都改成GET加一個action參數。

Django本身有JsonResponse，適合清楚的小型端點。當需要一致的序列化、驗證、權限、分頁與ViewSet時，本課引入DRF。這是額外套件，不是Django core的另一個名稱。

## 客戶端與伺服器的責任

客戶端送出JSON與適當Content-Type，伺服器解析、驗證並限定可寫欄位。回應先看狀態，再依內容型別處理，不把錯誤HTML當成JSON解析。API文件要說清楚日期、選項、空值與未知欄位政策。

本課使用Session驗證，因此瀏覽器的CSRF責任仍然存在。REST並不代表必須使用JWT，也不表示只要JSON就能略過cookie與來源的安全問題。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/17.svg" target="_blank" rel="noopener" aria-label="放大REST API與HTTP資源圖解"><img src="assets/figures/17.svg" alt="REST API與HTTP資源：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「REST API與HTTP資源」讀圖：追蹤JSON輸入到Serializer，再檢查哪些欄位由伺服器決定。再回答：JsonResponse是否自動提供Serializer、物件權限與分頁？</p></div>

## 自我檢查與解析

**題目：**JsonResponse是否自動提供Serializer、物件權限與分頁？

<details><summary>展開解析</summary><p>不會。它負責JSON回應；完整API流程需要自行實作或使用DRF等工具。</p></details>

## 官方來源

[對應官方文件](https://www.django-rest-framework.org/tutorial/quickstart/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
