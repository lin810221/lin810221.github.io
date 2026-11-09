# 官方資料、資料品質與可重現分析

把定義、發布與來源放進資料契約，為真實經濟研究建立入口。

## 來源按問題選

台灣可從主計總處、中央銀行與勞動統計入口取得定義及資料；跨國可看各國統計機構、IMF、World Bank、OECD等。使用前確認涵蓋、方法與授權，不因來源官方就假設不同國家完全可比。教材預設不下載，所有CSV為明示虛構。

## 讀檔前的契約

定義唯一鍵series/period/vintage；保留unit、base、adjustment、method、release與source。缺值、保密值、暫估與斷點要不同標記。改基期、年度重估或商品分類變更需有銜接規則，不用一條線掩蓋資料斷裂。

## 檢查順序

先型別與唯一鍵，再可行範圍、期間連續與恆等式，最後抽樣對官方表。通膨率與指數、債務存量與赤字流量不可混欄。恆等式不符時先看範圍、符號、統計差額和連鎖非可加性，不任意改資料到等式成立。

## 原始資料與處理分開

保存不可變原始快照、下載時間、校驗碼與處理程式；衍生表記轉換公式與版本。官方資料會修訂，網址不一定固定內容，僅留URL不足以重現。敏感資料也需限制保存與分享範圍，不能把可下載等同可任意公開。

## 與既有課程銜接

本課著重經濟定義、識別和情境。SQL/資料工程負責規模化管線，應用統計負責估計與推論，未來因果課可深化識別。這些是「跨課閱讀」；本課基本資料檢查、版本與完整專題不因有其他課就省略。

## 練習與解答

**先試著回答：** 官方圖表與自行計算不合，第一步應把哪個數字改掉？

<details><summary>展開推導與解答</summary>

先不改。對照概念、名/實質、季調、頻率、單位、基期、方法、版本和符號；連鎖實質不可加也可能是原因。找到定義或處理差異後再作有紀錄修正。

</details>

## 參考與跨課閱讀

- [主計總處：連鎖值使用注意](https://www.stat.gov.tw/News_Content.aspx?n=2679&s=103006)
- [ALFRED：資料版本](https://fred.stlouisfed.org/docs/api/fred/alfred.html)
- [BEA：GDP 估計與修訂](https://bea.gov/news/gdp-release-additional-information)
- [IMF：2025 SNA 與 BPM7 發布](https://www.imf.org/en/News/Articles/2025/03/20/pr25072-imf-and-statistical-community-release-new-global-standards-for-macroeconomic-stats)

[課程總覽](#overview) · [完整程式與資料](examples.zip)
