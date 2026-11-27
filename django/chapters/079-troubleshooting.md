# 排錯指南：環境、路由、資料與資產

先定位症狀，再使用最小可重現案例。

## 常見問題的第一步

找不到模組先查Python環境；NoReverseMatch查名稱與參數；找不到資料表查設定、migration與實際DB；TemplateDoesNotExist查app註冊與命名空間；CSRF 403查token、cookie、來源與設定。

靜態404查模板產生URL、來源目錄、collectstatic與服務層。不要以關閉CSRF、開DEBUG或公開media作為永久修正；先確認原因與正確責任。

## 保存能重現的資訊

記錄版本、指令、工作目錄、設定模組、request ID及必要資料ID。遮蔽密碼、token與私人原文，保留最小輸入。將已證實原因與猜測分開，避免下一個人照著未證實結論修改系統。

縮成單一URL、單筆物件或單段查詢，再逐步加回功能。若問題只在多worker或PostgreSQL出現，本機SQLite無法重現時應說明限制，不能直接判定框架版本有問題。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/27.svg" target="_blank" rel="noopener" aria-label="放大排錯指南：環境、路由、資料與資產圖解"><img src="assets/figures/27.svg" alt="排錯指南：環境、路由、資料與資產：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「排錯指南：環境、路由、資料與資產」讀圖：從症狀選最小反例，說明要蒐集什麼證據才能判定原因。再回答：CSRF失敗後直接加csrf_exempt，是否算找出原因？</p></div>

## 自我檢查與解析

**題目：**CSRF失敗後直接加csrf_exempt，是否算找出原因？

<details><summary>展開解析</summary><p>不是。它移除了一道保護，仍需定位token、cookie、來源或代理條件，並保留拒絕與成功測試。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/logging/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
