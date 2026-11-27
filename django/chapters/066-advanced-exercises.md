# 進階工程練習：速度與可靠性一起檢查

新增快取或背景工作時，原本的資料邊界仍需成立。

## 三組對照實驗

先比較有無摘要快取的查詢，再分兩帳號讀取並更新，確認失效與隔離。接著以相同key重送complete，確認事件與revision不重複。最後執行ImmediateBackend並指出它在哪個程序完成。

將async health與同步health比較功能結果，但不要只用單次耗時宣稱整個網站更快。若需要研究吞吐，先定義服務入口、負載、工作內容與量測方法。

## 規劃正式支線

寫出多worker快取、外部Task backend、PostgreSQL並行與ASGI服務各需哪些環境。清楚標示本機已跑、只完成設定及仍需真實基礎設施驗收的部分。

本章交付不是一組「全部開啟」設定，而是能解釋新鮮度、隔離、提交、重試與執行位置的工程方案。遇到問題時，能回到先前通過測試的最小系統。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/22.svg" target="_blank" rel="noopener" aria-label="放大進階工程練習：速度與可靠性一起檢查圖解"><img src="assets/figures/22.svg" alt="進階工程練習：速度與可靠性一起檢查：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「進階工程練習：速度與可靠性一起檢查」讀圖：區分request、佇列與worker，指出ImmediateBackend的執行位置。再回答：快取、async與queue一次全開後出錯，應如何縮小範圍？</p></div>

## 自我檢查與解析

**題目：**快取、async與queue一次全開後出錯，應如何縮小範圍？

<details><summary>展開解析</summary><p>回到已通過的設定，逐項加入並量測資料、權限與行為差異，保留最小反例。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/tasks/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
