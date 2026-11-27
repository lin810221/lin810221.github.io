# 郵件後端與密碼重設流程

本地郵件可測流程，正式寄送仍需服務與設定。

## 本地與測試郵件

本地設定使用console backend，把郵件內容輸出至終端；測試使用locmem，檢查收件人與內容而不外寄。不要把「send_mail回傳成功」寫成真實信箱已收到，後端的責任範圍不同。

正式寄送需配置服務、網域、憑證、寄件者與錯誤處理。API金鑰或SMTP密碼由環境注入，不應放進教材repo。敏感重設token也不應出現在公開日誌。

## 密碼重設的三個階段

先接受申請，再寄送帶有時效與用途限制的連結，最後設定新密碼並測失效行為。本課沿用內建auth views與token流程，使用通用回應避免任意透露帳號存在性。

郵件模板是純文字情境；其中的autoescape設定不應照搬到HTML頁面。開發時終端會顯示本地重設連結，實際使用者網站則需正確的網域、HTTPS與寄送服務。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/16.svg" target="_blank" rel="noopener" aria-label="放大郵件後端與密碼重設流程圖解"><img src="assets/figures/16.svg" alt="郵件後端與密碼重設流程：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「郵件後端與密碼重設流程」讀圖：沿私人檔案的上傳及下載路徑，指出哪裡再次檢查擁有者。再回答：測試的mail.outbox有一封信，能否證明SMTP正式配置正常？</p></div>

## 自我檢查與解析

**題目：**測試的mail.outbox有一封信，能否證明SMTP正式配置正常？

<details><summary>展開解析</summary><p>不能。它證明測試backend收到預期郵件；真實寄送、網域與收信結果需另行整合驗證。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/email/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
