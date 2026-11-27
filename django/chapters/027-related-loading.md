# 關聯載入、額外查詢與6.1 fetch modes

用查詢數驗證，避免只靠直覺優化。

## 查詢次數的算例

假設列表有 $N$ 筆任務，取得列表一次，且每筆owner尚未快取。逐列讀owner會有

$$
Q_{naive}=1+N,\qquad Q_{select}=1.
$$

後式假設用一次join載入單值關聯；若 $N=20$，教學算例為 $21$ 次與 $1$ 次。多值關聯常改用prefetch，查詢次數與關聯層數、批次及篩選有關，不能把所有場景都套成一次。

## 現有預載與新擷取策略

`select_related` 適合外鍵等單值關聯，`prefetch_related` 可處理多值關聯。Django 6.1另提供 `FETCH_ONE`、`FETCH_PEERS` 與 `FETCH_RAISE`，讓未載入欄位的取值行為可控制；最後一種可讓意外查詢直接拋出FieldFetchBlocked。

```python
from django.db.models import FETCH_RAISE
from django.core.exceptions import FieldFetchBlocked
item = Task.objects.only('pk').fetch_mode(FETCH_RAISE).get(pk=pk)
```

新功能不等於可以不理解查詢。先說明哪些欄位被延後、哪些物件是同批peers，再以測試驗證；預載過多內容也會增加記憶體與傳輸成本。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/09.svg" target="_blank" rel="noopener" aria-label="放大關聯載入、額外查詢與6.1 fetch modes圖解"><img src="assets/figures/09.svg" alt="關聯載入、額外查詢與6.1 fetch modes：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「關聯載入、額外查詢與6.1 fetch modes」讀圖：比較逐列關聯查詢與批次載入，核對查詢次數及欄位範圍。再回答：select_related與prefetch_related可以不分關係全部互換嗎？</p></div>

## 自我檢查與解析

**題目：**select_related與prefetch_related可以不分關係全部互換嗎？

<details><summary>展開解析</summary><p>不能。單值join與多值批次載入有不同策略與成本，應根據關係和實際查詢驗證。</p></details>

## 離線實作

在下載包 `examples` 目錄執行 `python 08_n_plus_one.py`。入口使用真實Django、記憶體SQLite與合成資料，不連外部服務；完整網站則由 `manage.py runserver` 啟動。

<!-- example:08_n_plus_one.py -->

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/db/fetch-modes/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
