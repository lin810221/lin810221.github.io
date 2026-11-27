# View、狀態碼與回應內容

HTTP狀態描述結果，不能所有情況都回200。

## View的最小契約

View接收request，讀取已確認的輸入，再回傳HttpResponse類型。HTML可用 `render`，JSON可用 `JsonResponse`，跳轉可用 `redirect`。內容型別、狀態與標頭都會影響瀏覽器或API客戶端如何解讀。

GET應以讀取為主，資料修改使用適當的POST等方法並加驗證。不要讓「點開連結」就刪資料；瀏覽器預抓、搜尋引擎與使用者重新整理都可能觸發GET。

## 常見狀態的用途

成功讀取常為200，建立API資源常為201，重新導向常為302，輸入錯誤可能是400，未允許的方法是405。找不到物件或不屬於使用者時，本課常以404避免洩漏存在性；API身分錯誤的401或403還取決於認證方案。

先檢查回應再決定是否解析JSON，不能對登入跳轉回來的HTML直接呼叫JSON解析。以健康端點與任務建立對照，能理解狀態、本文與Location各自提供什麼資訊。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/04.svg" target="_blank" rel="noopener" aria-label="放大View、狀態碼與回應內容圖解"><img src="assets/figures/04.svg" alt="View、狀態碼與回應內容：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「View、狀態碼與回應內容」讀圖：依序讀middleware進入與返回路徑，指出本單元的檢查點。再回答：API回傳登入頁HTML，客戶端JSON解析失敗，應先查哪裡？</p></div>

## 自我檢查與解析

**題目：**API回傳登入頁HTML，客戶端JSON解析失敗，應先查哪裡？

<details><summary>展開解析</summary><p>檢查原始狀態、跳轉鏈與Content-Type，再查登入與認證設定；不能只將解析錯誤歸因於JSON格式。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/ref/request-response/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
