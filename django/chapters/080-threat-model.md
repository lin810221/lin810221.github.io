# 常見威脅與反例清單

將安全需求變成具體輸入與可觀察結果。

## 依資料與入口列風險

本專題的重點包含跨帳號物件存取、偽造owner、關聯tag越權、CSRF、未跳脫內容、公開私人檔案、開放跳轉及錯誤設定。每一項都要能對應入口、資料與拒絕方式。

使用Django框架可得到多種既有防護，但自訂View、raw SQL、模板safe及外部服務都可能改變邊界。ORM參數化也不是任意拼接raw SQL字串的許可證。

## 防護與驗收配對

owner queryset配跨帳號測試，CSRF配缺token反例，模板跳脫配特殊字元，私人storage配直接URL拒絕，LoginView配外部next拒絕。不要只列一張縮寫清單，卻沒有知道如何證明它存在。

這是教學專題的威脅範圍，不是所有網站的完整安全審查。實際產品需依資料敏感性、服務暴露與組織要求擴充，並在目標環境驗證。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/27.svg" target="_blank" rel="noopener" aria-label="放大常見威脅與反例清單圖解"><img src="assets/figures/27.svg" alt="常見威脅與反例清單：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「常見威脅與反例清單」讀圖：從症狀選最小反例，說明要蒐集什麼證據才能判定原因。再回答：使用Django ORM後，能否把使用者字串任意拼進raw SQL？</p></div>

## 自我檢查與解析

**題目：**使用Django ORM後，能否把使用者字串任意拼進raw SQL？

<details><summary>展開解析</summary><p>不能。raw SQL仍需適當參數化及審查，框架不會自動修復任意字串拼接。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/security/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
