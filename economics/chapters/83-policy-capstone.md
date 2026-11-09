# 完整專題：一份可檢查的政策情境報告

輸出設定、敏感度CSV、獨立SVG與JSON，讓假設、算術和限制一起交付。

## 問題與範圍

以虛構競爭商品市場評估每件稅的量、買賣價、稅收、剩餘與DWL。主模型P=100−Q、P=20+Q，不含外部性、動態、逃漏、一般均衡或政府支出效益。它回答指定模型的情境算術，不預測任何國家政策。

## 實際輸出

42_policy_report產出15組scenarios.csv、market.svg與report.json。SVG有標題/說明，可獨立開啟或分享；JSON包含Python版本、資料hash、模型假設與驗收。目的地必須不存在，避免覆蓋，未指定時用暫存目錄。

## 敏感度不是識別

改需求斜率時也改原均衡，這是不同結構情境，不是只改局部彈性且其他都固定的實證比較。將情境標清，不用「高/低彈性」直接當研究分組。若要校準真實資料，需估參數、處理內生性與不確定性。

## 驗收什麼

每組都驗證數量非負、CS+PS+收入等於總剩餘、總剩餘+DWL回無稅基準；禁止性稅不回假成交價。資料檔與報告可對hash，SVG可解析。測試通過證明程式與定義一致，不等於模型假設已被真實資料證明。

## 最後交一頁政策解釋

列誰受益受損、尚未納入效果、估計所需證據與可行替代工具。加上外部性或獨占時需另建模型，不在舊報告偷偷改標籤。好的交付把已知和未知一起呈現，不只留一個最大福利數字。

## 可執行實驗

依 [範例說明](examples/README.md) 準備 Python 3.15.2，在 `examples` 目錄執行 `python 42_policy_report.py`。不需第三方套件、金鑰或網路。數字來自明確模型或虛構資料，先檢查單位與假設，再解讀輸出。

<!-- example:42_policy_report.py -->

## 練習與解答

**先試著回答：** 可以把此報告的DWL直接當某項現實稅改的損失嗎？

<details><summary>展開推導與解答</summary>

不可。還需適用市場結構、真實參數、外部性、其他稅制與政策用途等。這份報告是可重現教具；若用真實資料需重新識別、估計與驗證。

</details>

## 參考與跨課閱讀

- [CORE Econ 2.0：個體目錄](https://books.core-econ.org/the-economy/microeconomics/0-3-contents.html)
- [CORE Econ 2.0：總體目錄](https://books.core-econ.org/the-economy/macroeconomics/0-3-contents.html)
- [Python 3.15.2 官方發布](https://www.python.org/downloads/release/python-3152/)

[課程總覽](#overview) · [完整程式與資料](examples.zip)
