# 螢幕位置與視線：幾何參考，不是唯一角度

把水平距離、垂直差與實際視覺需要連起來。

## 明示參考點

眼睛到螢幕哪個點？上緣、中心或常看內容不同。教材以眼與指定點的水平x、垂直z作幾何，z負代表較低：

$$
d=\sqrt{x^2+z^2},\quad \theta=\operatorname{atan2}(z,x)
$$

角度不是診斷或人體唯一理想值。

## 正式參考的背景

OSHA一般說明視距約50–100cm，需配合文字大小和可讀性；上緣在視線附近或稍低是參考。雙焦眼鏡等可能需較低位置，不能把平眼規則硬套每個人。

## 與輸入整體協調

太近、太遠、反光或難讀可能讓人改變姿勢。調整距離時也看桌深、視覺與鍵鼠，避免只動螢幕而讓其他任務更難。

## 實驗的範圍

程式只算指定參考點，沒有頸椎負荷、視力或疼痛預測。可比較幾何如何改變，再用實際可讀與使用回饋確認配置。

## 可選的離線實作

先手算或閱讀案例，再依[範例說明](examples/README.md)在examples目錄執行 `python 17_monitor_geometry.py`。Python3.15.2，僅標準函式庫；資料為虛構或明示假設。輸出協助核對任務、單位和算術，不代替人體、臨床與工作現場評估。純閱讀不用安裝程式。

<!-- example:17_monitor_geometry.py -->

## 練習與解答

**先想一想：** 螢幕上緣永遠必須正好平眼，否則就一定有害，對嗎？

<details><summary>展開驗算與理由</summary>

不對。它是一般參考，眼鏡、視覺需求、任務與整體配置可能不同；需實際調整，不以單一角度宣告健康。

</details>

## 正式來源與進一步閱讀

- [OSHA：螢幕配置與視覺需求](https://www.osha.gov/etools/computer-workstations/components/monitors)
- [OSHA：多種工作參考姿勢與變化](https://www.osha.gov/etools/computer-workstations/positions)
- [HSE：DSE工作站專用檢核表](https://www.hse.gov.uk/pubns/ck1.pdf)
- [OSHA：桌面與下方空間](https://www.osha.gov/etools/computer-workstations/components/desks)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
