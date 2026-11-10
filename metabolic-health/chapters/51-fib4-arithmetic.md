# FIB-4：公式、單位與用途限制

學會計算，但不讓一個數字自動診斷纖維化。

## 公式需要四個輸入

FIB-4使用年齡（歲）、AST與ALT（U/L）以及血小板（10^9/L）：

$$
\mathrm{FIB4}=\frac{\mathrm{age}\times\mathrm{AST}}{\mathrm{platelets}\sqrt{\mathrm{ALT}}}
$$

若報告寫血小板每微升，必須先確認數量級；不能把200000直接當成200。ALT與血小板不得為零或負值。

## 不是纖維化分期

它在特定臨床路徑作初步風險分層，可能引導後續彈性或其他檢查。結果不直接等於組織學分期；單獨高值也不是確診肝硬化。年齡本身在分子，不能忽略年齡影響。

## 年齡與情境

EASL2024的一般低界線1.3，在大於65歲（>65）使用較高的2.0低界線；35歲以下表現較差，急性疾病也不宜直接使用。不同路徑仍需核對。本課工具僅算成人穩定情境公式，不自動套風險色帶或安排追蹤。

## 手算驗證

50歲、AST30、ALT25、血小板200時，分子1500，分母1000，算術結果1.5。這只能驗證公式與單位，不能從這四項得知所有病因、目前症狀或是否適合套用某條路徑。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 26_fib4_arithmetic.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:26_fib4_arithmetic.py -->

## 練習與解答

**先自己判斷：** 把血小板200×10^9/L誤輸入200000，結果會如何？

<details><summary>展開驗算與理由</summary>

分母變大1000倍，FIB-4會變成原來的1/1000，造成嚴重錯誤。需核對數量級；算對也仍不是診斷。

</details>

## 官方來源與研究

- [EASL2024 MASLD正式指南](https://pmc.ncbi.nlm.nih.gov/articles/PMC11299976/)
- [EASL官方完整PDF：年齡與分層條件](https://easlcampus.eu/sites/default/files/2024-06/EASL_CPGs_on_MASLD.pdf)
- [AGA2026 MASLD正式路徑原文](https://pubmed.ncbi.nlm.nih.gov/41812830/)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
