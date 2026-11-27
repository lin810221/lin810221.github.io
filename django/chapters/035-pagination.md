# 分頁、穩定排序與篩選

頁碼、總數與篩選條件要一起維持。

## 分頁的正式定義

令篩選後資料數為 $N\ge0$、每頁筆數為正整數 $k$。在允許空第一頁的設定下，頁數為

$$
P=\max\left(1,\left\lceil\frac{N}{k}\right\rceil\right).
$$

例如 $N=12,k=5$ 有 $3$ 頁，最後一頁有 $2$ 筆；$N=0$ 時仍可顯示一個空頁。Django對無效頁碼的處理依使用的Paginator方法與View而定，不能假設所有入口都相同。

## 排序與條件不能丟失

使用穩定排序，必要時加入pk作同分次序；列表變動仍可能讓offset分頁移動，這是資料持續更新時的限制。翻頁連結保留搜尋與狀態條件，只替換page參數。

總數是篩選後QuerySet的數量，不等於當前頁長度。大量資料上count與深頁offset可能昂貴，需依需求研究其他分頁方式，而不是無條件把page size改得很大。

## 先讀這張圖

<figure class="tf-figure"><a href="assets/figures/12.svg" target="_blank" rel="noopener" aria-label="放大分頁、穩定排序與篩選圖解"><img src="assets/figures/12.svg" alt="分頁、穩定排序與篩選：以中文標示請求、資料與檢查邊界，依箭頭追蹤本單元討論的程式行為。" loading="lazy"></a><figcaption>原創教學示意；箭頭意義依圖例，不代表實際執行時間或部署比例。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>「分頁、穩定排序與篩選」讀圖：沿POST、redirect與GET追蹤重新整理，核對分頁與狀態變更。再回答：十二筆資料每頁五筆，最後一頁應有幾筆？</p></div>

## 自我檢查與解析

**題目：**十二筆資料每頁五筆，最後一頁應有幾筆？

<details><summary>展開解析</summary><p>兩筆；總頁數三。測試還要涵蓋空資料、無效頁碼、排序與篩選條件保留。</p></details>

## 離線實作

在下載包 `examples` 目錄執行 `python 19_pagination.py`。入口使用真實Django、記憶體SQLite與合成資料，不連外部服務；完整網站則由 `manage.py runserver` 啟動。

<!-- example:19_pagination.py -->

## 官方來源

[對應官方文件](https://docs.djangoproject.com/en/6.1/topics/pagination/)（查核：2026-11-26；Django 6.1系列，實測套件6.1.3）。跨課連結是獨立教材，本課仍保留必要的完整操作。
