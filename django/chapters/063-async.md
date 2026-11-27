# Async View、非同步ORM與同步邊界

async是執行模型，不是把所有網站自動變快的關鍵字。

## WSGI與ASGI下的條件

Django可提供async view，但效益依服務入口、middleware及I/O而異。WSGI與同步middleware可能產生轉接成本；CPU密集工作不會因加async就消失。先找等待時間與併發需求，再選執行模式。

在async上下文直接呼叫會阻塞的同步ORM可能觸發保護。使用支援的非同步方法，例如 `await Task.objects.filter(...).acount()`，或把需要同步交易的整段函式透過適當橋接執行，不任意關閉非同步安全檢查。

## 交易仍需清楚邊界

本課async health不讀DB，實測async view路徑；交易服務仍是同步原子函式。這讓已驗證範圍清楚，不把純JSON示例誤稱完成非同步資料庫與外部I/O效能驗收。

正式ASGI服務要檢查同步middleware、連線、取消、timeout及壓力。本地Client成功只能證明限定流程可跑，無法代替實際負載與服務器配置。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/21.svg" target="_blank" rel="noopener" aria-label="放大Async View、非同步ORM與同步邊界圖解"><img src="assets/figures/21.svg" alt="Async View、非同步ORM與同步邊界：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Async View、非同步ORM與同步邊界」讀圖：沿使用者範圍與快取鍵，說明命中、失效與資料隔離。再回答：把View改成async def後，裡面的同步資料庫與CPU工作會自動變成非阻塞嗎？</p></div>

## 自我檢查與解析

**題目：**把View改成async def後，裡面的同步資料庫與CPU工作會自動變成非阻塞嗎？

<details><summary>展開解析</summary><p>不會。需使用支援的非同步介面或適當橋接，CPU工作也可能仍阻塞執行。</p></details>

## 離線實作

在下載包 `examples` 目錄執行 `python 23_async_view.py`。入口使用真實Django、記憶體SQLite與合成資料，不連外部服務；完整網站則由 `manage.py runserver` 啟動。

<!-- example:23_async_view.py -->

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/async/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
