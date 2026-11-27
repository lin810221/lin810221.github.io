# Migration：schema演進與資料搬移

makemigrations產生計畫，migrate才會套用。

## 兩個命令的不同作用

```powershell
python manage.py makemigrations desk
python manage.py showmigrations
python manage.py sqlmigrate desk 0001
python manage.py migrate
```

Migration保存模型狀態的演進與相依順序；不是每次啟動就刪表重建。產生後應閱讀內容，再在可回復環境套用。不要為了讓提示消失而任意刪除migration檔或偽造已套用狀態。

## 有舊資料時的變更

新增不可為空欄位、改唯一條件或縮小型別，都要先處理既有資料。較大的變更常拆成可相容的schema擴充、資料搬移與後續收斂。資料migration使用歷史模型，不應直接匯入隨時會變動的現行Model類別。

本課附完整初始migration，可在空SQLite資料庫重建所有表。正式大型資料庫還要評估鎖定、執行時間、回復與多版本程式相容性；SQLite通過不代表PostgreSQL的部署過程已驗收。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/08.svg" target="_blank" rel="noopener" aria-label="放大Migration：schema演進與資料搬移圖解"><img src="assets/figures/08.svg" alt="Migration：schema演進與資料搬移：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「Migration：schema演進與資料搬移」讀圖：沿schema變更與資料搬移的順序，說明哪些舊資料必須先處理。再回答：修改models.py後，資料庫為什麼沒有立刻改變？</p></div>

## 自我檢查與解析

**題目：**修改models.py後，資料庫為什麼沒有立刻改變？

<details><summary>展開解析</summary><p>模型原稿與實際schema是不同狀態，需要產生並套用migration；還要確認命令指向正確設定與資料庫。</p></details>

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/migrations/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
