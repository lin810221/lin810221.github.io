# ViewSet、router與共享服務

使用標準動作，也保留任務特有的行為契約。

## Router組合路由

ModelViewSet提供常見CRUD動作，router依註冊資訊產生路由。明確設定basename與serializer，避免模型推導與命名不清。讀取路由表，確認集合、詳情與額外action對應的方法。

本課get_queryset先依user限制Task，再處理合法狀態篩選。perform_create補owner；complete action則呼叫與HTML相同的服務，讓交易與命令去重不必在兩個入口各寫一套。

## 自動動作也要測試

ViewSet不自動知道你的owner政策，也不表示所有action都應公開。額外動作需指定方法、驗證輸入、檢查物件與設定回應；不要將任意Model方法變成API。

對相同任務用HTML與API標記完成，確認狀態與revision規則一致。API與前端可共用服務，但輸入格式、CSRF、回應與錯誤呈現仍各有責任。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/17.svg" target="_blank" rel="noopener" aria-label="放大ViewSet、router與共享服務圖解"><img src="assets/figures/17.svg" alt="ViewSet、router與共享服務：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「ViewSet、router與共享服務」讀圖：追蹤JSON輸入到Serializer，再檢查哪些欄位由伺服器決定。再回答：額外complete action可直接只憑主鍵取得任務嗎？</p></div>

## 自我檢查與解析

**題目：**額外complete action可直接只憑主鍵取得任務嗎？

<details><summary>展開解析</summary><p>應先使用已限制範圍的get_object或同等授權查詢，再呼叫服務，不能繞過ViewSet既有邊界。</p></details>

## 離線實作

在下載包 `examples` 目錄執行 `python 18_rest_create.py`。入口使用真實Django、記憶體SQLite與合成資料，不連外部服務；完整網站則由 `manage.py runserver` 啟動。

<!-- example:18_rest_create.py -->

## 官方來源

[對應官方文件](https://www.django-rest-framework.org/tutorial/quickstart/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
