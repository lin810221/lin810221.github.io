# 篩檢Bayes：敏感度不是陽性後的機率

用虛構測試與期望人數理解基線影響。

## 四個結果

真陽性、偽陽性、真陰性與偽陰性，依目標狀態與測試結果交叉。敏感度問有目標狀態者多少陽性；PPV問所有陽性中多少真的有，分母不同。

## 一萬人的假設

盛行率5%、敏感度80%、特異度90%時，預期真陽性400、偽陽性950，PPV約29.6%。這不是任何具名心理量表的真實效能，也不代表個人的診斷機率。

## 基線如何進入

$$
\mathrm{PPV}=\frac{Se\,p}{Se\,p+(1-Sp)(1-p)}
$$

p是指定盛行率。若沒有陽性、分母為零，結果未知；不能用0表示確定安全。真實工具的敏感度與特異度也可能隨族群和方法不同。

## 不跨用途

本實驗只教篩檢算術，不用於自殺風險預測、決定治療資格或診斷。陽性需要適當評估，陰性也不能排除其他需要或當下安全問題。

## 可選的離線實作

先閱讀概念與案例，再依[範例說明](examples/README.md)在examples目錄執行 `python 44_screening_bayes.py`。Python3.15.2，僅標準函式庫；數字和情境全為虛構，程式用來檢查假設、資料與算術。閱讀和一般練習不需要安裝程式。

<!-- example:44_screening_bayes.py -->

## 練習與解答

**先想一想：** 敏感度80%，能否說所有陽性者都有80%機率患病？

<details><summary>展開示範答案與理由</summary>

不能。PPV還受特異度與族群基線影響；本虛構例子約29.6%，不能當個人診斷或安全判定。

</details>

## 來源與進一步閱讀

- [OpenStax：相關、實驗與證據](https://openstax.org/books/psychology-2e/pages/2-3-analyzing-findings)
- [NICE NG222：成人憂鬱正式指南與2026審查](https://www.nice.org.uk/guidance/ng222)
- [NIMH：何時需要幫助（2025修訂）](https://www.nimh.nih.gov/health/publications/my-mental-health-do-i-need-help)
- [NICE NG225：自傷照護及風險工具限制](https://www.nice.org.uk/guidance/ng225/chapter/recommendations)

[回課程總覽](#overview) · [下載完整範例、資料與測試](examples.zip)
