# 群組、模型permission與Admin身分

一組權限名稱，仍需要入口真正使用它。

## 框架提供的權限層

Django會建立常見模型權限，也可自訂permission並指派給使用者或Group。is_staff主要關係到Admin登入資格，不代表能修改全部資料；superuser則是更高管理權限，應依實際需要使用。

StudyHub的匯出功能要求 `desk.export_task`，仍限制輸出屬於目前使用者的任務。權限回答「可做這類動作」，owner範圍回答「可對哪些資料做」，兩者共同構成授權。

## 權限設定與快取

不要假設新增一個permission名稱就會自動保護View；要在入口呼叫或套用相應Mixin。權限查詢可能有快取，測試修改權限後應理解目前使用的User物件與請求是否重新取得狀態。

用無權限、取得權限及跨帳號資料三種情境測匯出。API使用的DRF權限類別也需另外設定，不能因Django Model有權限記錄，就宣稱所有API會自動執行它。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/14.svg" target="_blank" rel="noopener" aria-label="放大群組、模型permission與Admin身分圖解"><img src="assets/figures/14.svg" alt="群組、模型permission與Admin身分：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「群組、模型permission與Admin身分」讀圖：追蹤cookie、CSRF token及來源，說明哪些防護不能互相取代。再回答：使用者有export_task，是否代表能匯出所有帳號資料？</p></div>

## 自我檢查與解析

**題目：**使用者有export_task，是否代表能匯出所有帳號資料？

<details><summary>展開解析</summary><p>不代表。本課仍依owner限制資料；操作類型權限與物件範圍是兩個條件。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/auth/default/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
