# 查詢數、on_commit與外部副作用

驗證的範圍要和測試工具真正執行的行為一致。

## 查詢成本可成為回歸條件

使用assertNumQueries或CaptureQueriesContext，對固定資料檢查關聯載入。限制應對準具體查詢路徑與版本，不能把所有HTTP總查詢數永久寫死，再把合理新增功能視為錯誤。

串流回應需要讀取內容並關閉；郵件以locmem檢查；storage以記憶體實作隔離。本地替身能驗證資料流程，不代表外部SMTP、物件儲存或CDN已整合完成。

## 提交callback的測試

TestCase包住交易，on_commit不一定像正式請求一樣自然執行。本課使用captureOnCommitCallbacks並明確執行，檢查快取失效與檔案清理。這驗證callback內容，真正提交及競爭仍有另一層測試。

把外部副作用測試分成單元、受控整合與正式驗收，記錄每層條件。失敗時先看是框架行為、替身限制還是實際服務問題，不混成單一「Django錯誤」。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/20.svg" target="_blank" rel="noopener" aria-label="放大查詢數、on_commit與外部副作用圖解"><img src="assets/figures/20.svg" alt="查詢數、on_commit與外部副作用：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「查詢數、on_commit與外部副作用」讀圖：比較正常與越權案例，確認測試真的會攔住錯誤行為。再回答：測試註冊了on_commit但未執行，可以宣稱檔案已清除嗎？</p></div>

## 自我檢查與解析

**題目：**測試註冊了on_commit但未執行，可以宣稱檔案已清除嗎？

<details><summary>展開解析</summary><p>不能。要明確執行並檢查storage；真正提交與外部儲存可靠性仍需另外驗證。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/testing/tools/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
