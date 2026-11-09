# 國際收支、金融帳與國際投資部位

用一致符號對帳，分清交易流量、資產存量與統計差額。

## 帳的結構

經常帳CA含商品服務與所得/移轉等按版本分類；資本帳KA與日常「資本流入」不是同義；金融帳FA記金融資產淨取得減負債淨發生，需包含準備資產。FA正值在此慣例代表淨貸出，不是直接叫淨資金流入。

$$
CA+KA-FA+SD=0,\qquad SD=FA-CA-KA
$$

## 算一個符號例子

CA=−20、KA=0、FA=−18，統計差額SD=2，才能對帳。BPM7使用statistical discrepancy術語；仍採BPM6的表常見誤差與遺漏。台灣表若將準備資產另列，計算完整FA時要加回，不能拿不含準備的分項直接驗這條恆等式。

## 新標準與舊資料

BPM7與2025 SNA同步更新，但實際資料仍可能採BPM6。所得類別的新舊術語需對照來源方法，不能自行改名後當完全同口徑。檔案附metadata比只存「金融帳」一欄更重要。

## 存量IIP

國際投資部位是對外資產/負債的時點存量。變化還有匯率、價格重估與其他調整，不等於只把CA累加。某國經常帳順差但資產價/匯率變動，可使淨部位變化不同；不能由存量差直接反算完整交易帳。

## 可執行實驗

依 [範例說明](examples/README.md) 準備 Python 3.15.2，在 `examples` 目錄執行 `python 39_exchange_and_bop.py`。不需第三方套件、金鑰或網路。數字來自明確模型或虛構資料，先檢查單位與假設，再解讀輸出。

<!-- example:39_exchange_and_bop.py -->

## 練習與解答

**先試著回答：** 若一張表FA排除準備資產，為何本課公式可能對不起來？

<details><summary>展開推導與解答</summary>

因使用的FA不是完整定義。先依表格符號將準備資產等納入金融帳，再對照CA、KA與差額；不能用改正負號硬湊，也不要把差額全說成資本外逃。

</details>

## 參考與跨課閱讀

- [IMF：BPM7 White Cover](https://data.imf.org/-/media/iData/External-Storage/Documents/5B776E0E552E4881AF24042EAE7D049B/en/1-BPM7-White-Cover.pdf)
- [日本銀行：國際收支符號說明](https://www.boj.or.jp/en/statistics/outline/exp/faqbpsm6.htm)
- [IMF：2025 SNA 與 BPM7 發布](https://www.imf.org/en/News/Articles/2025/03/20/pr25072-imf-and-statistical-community-release-new-global-standards-for-macroeconomic-stats)

[課程總覽](#overview) · [完整程式與資料](examples.zip)
