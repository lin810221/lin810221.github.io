# 建立、更新、刪除與驗證邊界

模型實例與批次QuerySet操作有不同生命週期。

## 選擇符合需求的寫入方式

`create` 建立物件，實例 `save` 更新狀態，QuerySet `update` 在資料庫直接批次更新。批次更新不會像逐一呼叫save那樣執行相同的Model與signal流程，適合的使用情境與副作用要明確設計。

`get_or_create` 可處理依唯一條件重複建立的情況，但仍依賴正確資料庫約束。查詢條件沒有唯一保護時，不應把它當成任意併發去重工具。`update_or_create` 也不能替代所有業務交易設計。

## 寫入還包括授權

資料庫接受一筆更新，不代表目前使用者有權發起它。先以使用者範圍取得物件，再修改白名單欄位。不能直接將整個POST字典傳給Model，讓owner、revision或管理欄位被客戶端任意改動。

本課使用表單、Serializer與服務層區分輸入驗證、呈現及共享動作。若改採批次更新，重新檢查快取失效、updated_at與signals是否仍符合需求，並記錄與原流程的差異。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/09.svg" target="_blank" rel="noopener" aria-label="放大建立、更新、刪除與驗證邊界圖解"><img src="assets/figures/09.svg" alt="建立、更新、刪除與驗證邊界：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「建立、更新、刪除與驗證邊界」讀圖：比較逐列關聯查詢與批次載入，核對查詢次數及欄位範圍。再回答：QuerySet.update後post_save沒有觸發，是Django壞了嗎？</p></div>

## 自我檢查與解析

**題目：**QuerySet.update後post_save沒有觸發，是Django壞了嗎？

<details><summary>展開解析</summary><p>不是同一個生命週期。批次更新不逐一呼叫Model.save；需要明確處理副作用或選擇不同寫入路徑。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/db/queries/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
