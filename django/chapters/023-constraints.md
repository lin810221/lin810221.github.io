# Unique、CheckConstraint與索引

正確性與查詢速度是不同的設計問題。

## 資料庫守住不可違反條件

Task的priority只能在指定範圍，status只能是合法選項；Tag在同一owner下名稱唯一。這些條件除了表單提示，也由CheckConstraint或UniqueConstraint保護，讓其他寫入路徑不能輕易破壞資料。

驗證先查是否存在，再寫入，仍可能在併發時遇到競爭；資料庫唯一條件是最後一道一致性保護。捕捉IntegrityError時要注意交易狀態，在可回復的atomic邊界處理，不能忽略錯誤後繼續使用已失敗的交易。

## 索引不是越多越好

本課為owner與status組合建立索引，對齊常見篩選。索引會增加儲存與寫入成本；是否使用仍由資料庫規劃器決定。應以實際查詢與資料量檢查，而非每個欄位都加索引。

用獨立算例直接寫入非法priority，確認資料庫拒絕，並對照表單提前提示的差異。這能看見使用者體驗與資料一致性如何互相補足。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/08.svg" target="_blank" rel="noopener" aria-label="放大Unique、CheckConstraint與索引圖解"><img src="assets/figures/08.svg" alt="Unique、CheckConstraint與索引：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Unique、CheckConstraint與索引」讀圖：沿schema變更與資料搬移的順序，說明哪些舊資料必須先處理。再回答：UniqueConstraint能不能代替所有表單驗證？</p></div>

## 自我檢查與解析

**題目：**UniqueConstraint能不能代替所有表單驗證？

<details><summary>展開解析</summary><p>不能。它保障資料條件，但使用者仍需要清楚錯誤；跨欄位規則、權限與業務流程還需應用層處理。</p></details>

## 離線實作

在下載包 `examples` 目錄執行 `python 06_constraints.py`。入口使用真實Django、記憶體SQLite與合成資料，不連外部服務；完整網站則由 `manage.py runserver` 啟動。

<!-- example:06_constraints.py -->

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/db/models/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
