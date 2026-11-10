# RR、ARR與NNT：用整數人數驗算

讓每個百分比都有分母，並處理零事件與傷害。

## 固定期限的計算

對照與介入需有共同結果、可比較族群與期限。令對照風險p0、介入p1：

$$
\mathrm{RR}=\frac{p_1}{p_0},\quad \mathrm{ARR}=p_0-p_1,\quad \mathrm{RRR}=1-\mathrm{RR}
$$

ARR為正時可計NNT=1/ARR；它是依假設和資料得到的群體點估計，不是保證某個人受益。

## 虛構人數驗算

1000人中100件與1000人中70件，p0=.10、p1=.07，RR=.70、ARR=.03。程式保留確切點值，文字需要整數時說明向上取整與期限；真實試驗還需不確定性與適當方法。

## 邊界不能亂補

對照零事件時RR分母為零，輸出未知；兩組相同時沒有有限NNT，不能填0。若介入風險較高，方向是傷害，不能仍標作降低風險。人數與事件需是合理整數且事件不超過人數。

## 不混用統計量

每人年發生率、HR、OR與固定期限RR不同，不能直接把它們代入同一式。DPP的原始人年發生率不在本例中冒充人數；本程式明示虛構例子，避免精確算術掩蓋資料類型錯誤。

## 可執行資料實驗

依[離線範例說明](examples/README.md)準備Python3.15.2，在examples目錄執行 `python 45_absolute_relative_effects.py`。僅用標準函式庫，預設不連網；資料和參數為明示虛構。輸出檢查單位、來源與算術，不生成個人診斷、風險預測、用藥或追蹤頻率。

<!-- example:45_absolute_relative_effects.py -->

## 練習與解答

**先自己判斷：** 兩組風險完全相同，NNT能否寫0？

<details><summary>展開驗算與理由</summary>

不能。ARR=0時倒數沒有有限值，程式保留未知並標示沒有風險差；0會錯誤暗示完全不需介入就多得一份效益。

</details>

## 官方來源與研究

- [DPP原始隨機試驗](https://www.nejm.org/doi/full/10.1056/NEJMoa012512)
- [ADA2026：預防與延後糖尿病](https://diabetesjournals.org/care/article/49/Supplement_1/S50/163924/3-Prevention-or-Delay-of-Diabetes-and-Associated)
- [2026血脂指南正式原文](https://www.jacc.org/doi/10.1016/j.jacc.2025.11.016)

[回課程總覽](#overview) · [下載完整程式、資料與測試](examples.zip)
