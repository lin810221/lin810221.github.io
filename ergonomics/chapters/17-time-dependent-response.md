# 時間效應：蠕變、鬆弛與任意模型

看懂時間曲線，也知道何時只是教學類比。

## 兩個概念

在理想材料討論中，持續應力下形變隨時間增加可稱蠕變；固定形變下應力隨時間改變可談鬆弛。需說明控制的是什麼，不把兩者或肌肉疲勞混稱同一現象。

## 教材的指數示意

$$
x(t)=x_{\infty}+(x_0-x_{\infty})e^{-t/\tau}
$$

這裡所有係數與時間單位明示任意，僅示範曲線如何依參數改變，不是人體組織校準。

## 不能由曲線開處方

τ不是某人的恢復時間；曲線下降也不代表肌腱治好或可以搬更重。需要人體、病史、任務與測量，不能把材料類比變成固定休息天數。

## 實務提問

持續時間、活動變化、工作強度與可用支持都值得觀察。任務重新設計可以減少某些需求，但效果仍需實際追蹤，不是看模型變漂亮就結案。

## 可選的離線實作

先手算或閱讀案例，再依[範例說明](examples/README.md)在examples目錄執行 `python 09_relaxation_analogy.py`。Python3.15.2，僅標準函式庫；資料為虛構或明示假設。輸出協助核對任務、單位和算術，不代替人體、臨床與工作現場評估。純閱讀不用安裝程式。

<!-- example:09_relaxation_analogy.py -->

## 練習與解答

**先想一想：** 任意模型τ=10，是否就代表每個人休息10分鐘便已恢復？

<details><summary>展開驗算與理由</summary>

不能。τ是教學參數，未校準人體，也沒有建立工作與臨床適用；不能轉成個人恢復處方。

</details>

## 正式來源與進一步閱讀

- [NIH：肌腱、負荷與病變（2025）](https://newsinhealth.nih.gov/2025/12/tendon-trouble)
- [OpenStax：肌肉收縮與放鬆](https://openstax.org/books/anatomy-and-physiology-2e/pages/10-3-muscle-fiber-contraction-and-relaxation)
- [HSE：工作安排與休息的適用條件](https://www.hse.gov.uk/msd/dse/work-routine.htm)
- [NIOSH：人體工學與肌肉骨骼預防](https://www.cdc.gov/niosh/ergonomics/about/index.html)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
