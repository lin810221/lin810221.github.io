# 測試資料、fixtures與可讀性

每筆資料應讓被測條件更清楚，而不是堆數量。

## 小型明確資料優先

本課用兩個帳號、各自tag與Task建立權限反例，再按測試增加需要的資料。若每項測試都載入巨大fixture，容易不知道哪個隱藏關聯讓測試通過，也會使schema變動難以維護。

fixtures適合固定參考資料或明確的匯入情境；工廠與helper適合變化的測試需求。不要使用脆弱的固定主鍵推測資料順序，除非該識別就是被測契約。

## 資料生成要可重現

隨機資料需固定種子並控制條件，但不能只因固定種子就認為代表性足夠。日期、時區、空值、長度與罕見選項應有刻意設計的案例，不期待隨機生成恰好撞到。

StudyHub的seed_demo用於人工操作，測試資料則由測試隔離建立；兩者不要共用真實帳號密碼。資料可讀性讓未來失敗訊息能直接指出哪個邊界退步。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/20.svg" target="_blank" rel="noopener" aria-label="放大測試資料、fixtures與可讀性圖解"><img src="assets/figures/20.svg" alt="測試資料、fixtures與可讀性：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「測試資料、fixtures與可讀性」讀圖：比較正常與越權案例，確認測試真的會攔住錯誤行為。再回答：測試資料越多，越能證明正確嗎？</p></div>

## 自我檢查與解析

**題目：**測試資料越多，越能證明正確嗎？

<details><summary>展開解析</summary><p>不一定。資料需覆蓋具體邊界與反例，大量相似資料可能只增加時間而未增加檢查能力。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/testing/overview/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
