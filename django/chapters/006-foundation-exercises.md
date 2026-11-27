# 起步練習：畫出你正在執行的系統

先用最小可用網站建立可驗證的操作習慣。

## 四個起步成果

寫下Python路徑與套件版本，畫出瀏覽器、Python程序及資料庫的位置，列出project與app的檔案責任，最後完成一次登入與新增任務。每一步都要有可觀察的結果，而不是只說安裝完成。

故意打錯一個路徑、停止後端、以及在未登入時開任務頁，比較瀏覽器收到的情況。網址錯誤、程序未啟動與登入要求是不同問題，不該都用重新安裝Django處理。

## 建立第一份開發紀錄

記錄啟動目錄、設定模組、資料庫位置、執行指令及完整錯誤。對密碼與密鑰只記錄取得方式，不能直接貼進公開repo。將可重現步驟留下，之後換電腦或交給同事時才能快速接手。

本章先不加入前端建置工具與外部服務。下一章沿相同專案理解設定、路由與View；每個新功能都能回到這份已跑通的基準，而不必一次猜測整套系統。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/02.svg" target="_blank" rel="noopener" aria-label="放大起步練習：畫出你正在執行的系統圖解"><img src="assets/figures/02.svg" alt="起步練習：畫出你正在執行的系統：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「起步練習：畫出你正在執行的系統」讀圖：區分project、app與設定，沿管理命令走到第一個頁面。再回答：看到ModuleNotFoundError與404，應採取相同排錯方式嗎？</p></div>

## 自我檢查與解析

**題目：**看到ModuleNotFoundError與404，應採取相同排錯方式嗎？

<details><summary>展開解析</summary><p>前者先查Python環境與模組匯入，後者查路由、參數與物件查詢；先辨識失敗層次。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/intro/overview/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
