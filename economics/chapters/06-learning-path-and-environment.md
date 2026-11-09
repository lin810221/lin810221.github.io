# 學習路線、Python 與模型實驗規則

從零安排閱讀與實作，清楚區分理論、虛構情境、官方定義與真實證據。

## 三條閱讀路線

第一次學習依章順序：基礎→個體→總體→政策→國際→證據。有數學基礎可先看公式與實驗，再回文字假設；只想理解新聞可先讀統計口徑與政策圖，但應補供需、選擇與成本。每章六單元，側欄的單元號會重新從01開始。

## 安裝與執行

版本於2026-11-09查核，主要實測為Python3.15.2。範例使用標準函式庫，不需要pip安裝其他套件；網頁閱讀則連Python都不需要。若電腦尚未安裝，從Python官方網站選正式穩定版，安裝後在終端機確認版本。

```powershell
py -3.15 --version
cd economics/examples
py -3.15 04_supply_and_demand.py
py -3.15 -m unittest discover -s . -p test_examples.py -v
py -3.15 42_policy_report.py --output my-policy-report
```

macOS／Linux可用自己的python3.15命令。報告目的地需不存在，以免覆蓋既有成果；未提供輸出位置時，程式使用暫存目錄。完整壓縮包包含資料、共用模組與測試，解壓後不需要本網站才能執行。

## 實驗不等於預測

每個模型固定可辨識的假設；輸出可能是精確算術，卻沒有校準成任何真實國家。圖上移動滑桿不是估計政策效果，單一均衡也沒有自動涵蓋過渡成本、政治可行性或所有市場互動。最後專題會把設定、資料hash與限制寫入JSON，避免只留一張看似有說服力的圖。

## 公式與筆記

網站內公式離線渲染，進度與筆記依課程分開存在瀏覽器。要改教材，編輯chapters與course.json，再執行tools/build.py economics和validate.py。每個單元提供練習與可展開解答，先嘗試再看解析，較能發現自己混淆的是數學還是經濟假設。

## 練習與解答

**先試著回答：** 執行程式得到精確數字，就表示已預測台灣明年的結果嗎？

<details><summary>展開推導與解答</summary>

不是。必須有適用的結構、參數、資料、識別與預測驗證；本課虛構模型只證明其假設下的算術。官方數列需另記單位、期間、季調、基期、方法與資料版本。

</details>

## 參考與跨課閱讀

- [Python 3.15.2 官方發布](https://www.python.org/downloads/release/python-3152/)
- [OpenStax：Principles of Economics 3e](https://openstax.org/details/books/principles-economics-3e)

[課程總覽](#overview) · [完整程式與資料](examples.zip)
