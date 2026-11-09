# 資料版本、修訂與前視偏差

實作as-of選取，重現某個決策日當時能知道的資訊。

## 三個時間欄位

觀察期是經濟活動發生時段，發布日是資料公開時間，下載日是你取得版本的時間。初估/再估/基準修訂可能改歷史值；第三次估計也不保證永不再改。決策回測應限制在當時已發布資訊，而非只以period過濾。

## 虛構版本表

synthetic_vintages.csv對同一period保留多個release_date。2025年第一季在5月先公布100，8月改101；第二季到8月才首次公布。若截止6月底，只可用第一季初估，不可看到第二季或後續修訂。

## As-of演算法

先選release_date≤cutoff，再對每個series/period取其中最新發布。檢查重複鍵、單位、季調與方法一致。缺少尚未發布期應保留缺，不補0或拿未來資料倒填。日期格式與時區也需依資料服務定義。

## 預測與政策比較

即時資料與最新修訂資料回答不同問題：前者測當時可用資訊，後者描述事後較完整估計。兩種報告都可有用，但需命名清楚。特徵標準化、季調與模型訓練也不得利用未來資訊，避免只修發布日卻仍洩漏。

## 可執行實驗

依 [範例說明](examples/README.md) 準備 Python 3.15.2，在 `examples` 目錄執行 `python 41_data_vintages.py`。不需第三方套件、金鑰或網路。數字來自明確模型或虛構資料，先檢查單位與假設，再解讀輸出。

<!-- example:41_data_vintages.py -->

## 練習與解答

**先試著回答：** 把period≤決策日的所有最新資料取出，能避免前視嗎？

<details><summary>展開推導與解答</summary>

不能，某period資料可能日後才公布或修訂。必須用release_date/vintage約束，再選當時最新版本；訓練與資料處理也同樣需要時間界限。

</details>

## 參考與跨課閱讀

- [ALFRED：資料版本](https://fred.stlouisfed.org/docs/api/fred/alfred.html)
- [BEA：GDP 估計與修訂](https://bea.gov/news/gdp-release-additional-information)

[課程總覽](#overview) · [完整程式與資料](examples.zip)
