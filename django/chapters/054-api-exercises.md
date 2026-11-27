# REST API專題練習

同一資料契約，經由另一種介面驗收。

## 建立API測試清單

依序測集合讀取、建立、單筆讀取、局部更新、刪除及complete。對每個操作列出必要認證、CSRF條件、可寫欄位與回應狀態；再讓Bob操作Alice的ID，確認沒有越權與副作用。

將JSON中的owner、revision及外部tag作為反例，確認伺服器決定的欄位沒有被接管。對無效資料檢查回應和DB不變，對正常建立檢查新資源的owner與欄位值。

## 不重複業務邏輯

比較HTML與API共用complete_task的流程，指出輸入層差異與服務層不變的條件。若兩個入口開始產生不同revision或重複事件，先查是否有一條路繞過服務。

本章成果包括API路由、Serializer、ViewSet、權限與可執行測試。這仍是Django完整網站的API章；FastAPI是另一門獨立框架課程，並非本章漏掉的實作。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/18.svg" target="_blank" rel="noopener" aria-label="放大REST API專題練習圖解"><img src="assets/figures/18.svg" alt="REST API專題練習：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「REST API專題練習」讀圖：依API回應狀態與分頁內容，指出驗證、授權及錯誤的差異。再回答：API建立成功後只檢查201，還漏掉什麼？</p></div>

## 自我檢查與解析

**題目：**API建立成功後只檢查201，還漏掉什麼？

<details><summary>展開解析</summary><p>需要核對實際資料、owner、唯讀欄位、關聯及可能的副作用，不能只有狀態碼。</p></details>

## 官方來源

[對應官方文件](https://www.django-rest-framework.org/api-guide/testing/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
