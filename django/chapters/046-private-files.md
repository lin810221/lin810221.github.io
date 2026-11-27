# 私人下載、回應標頭與刪除

檔案的URL不應繞過資料擁有者。

## 每次下載重新檢查

下載View先用task owner過濾Attachment，再開啟storage檔案，以FileResponse串流回傳。資料夾不直接公開到media URL，因此猜到儲存名稱也不應越過此授權入口。

回應使用attachment處理並提供受控檔名與內容型別，配合nosniff等標頭。這些設定不能代替前面的授權；如果網址能直接從公開儲存取得內容，View保護就沒有覆蓋所有路徑。

## 刪除後的清理

刪除Attachment列時，本課在交易提交後刪儲存物件，避免資料回滾但檔案已消失。外部儲存刪除仍可能失敗，正式系統需可重試與對帳，不能把callback成功註冊當成檔案必然已清掉。

測試正常下載、別人下載、未登入與直接猜公開media路徑，再檢查資料刪除後的storage狀態。串流回應記得在測試中消耗並關閉，避免把未讀取的回應誤當完整下載驗證。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/16.svg" target="_blank" rel="noopener" aria-label="放大私人下載、回應標頭與刪除圖解"><img src="assets/figures/16.svg" alt="私人下載、回應標頭與刪除：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「私人下載、回應標頭與刪除」讀圖：沿私人檔案的上傳及下載路徑，指出哪裡再次檢查擁有者。再回答：FileResponse設為as_attachment，是否就保證只有owner能下載？</p></div>

## 自我檢查與解析

**題目：**FileResponse設為as_attachment，是否就保證只有owner能下載？

<details><summary>展開解析</summary><p>不會。下載授權來自伺服器物件範圍；attachment只影響回應處理方式。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/files/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
