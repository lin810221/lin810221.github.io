# 急性、慢性與恢復：不要把反應全當傷害

看壓力反應的時程、需求與資源。

## 急性動員可以有功能

面對挑戰時提高警覺與動員，有助準備行動。反應本身不是失敗；問題還在是否合宜、能否恢復、是否影響生活，以及需求是否長期超出資源。

## 慢性不是單純很多次

持續不確定、缺少控制與休息或反覆威脅，可能形成不同負荷。allostasis強調身體為適應而調節，allostatic load是研究框架，不是用日記總分就能精確測得的個人病名。

## 用任意模型理解累積

教材指定一個無生理單位的狀態：

$$
x_{t+1}=r x_t+u_t,\quad 0\le r\le1
$$

r是任意保留比例，u是指定輸入。改參數可看數學形狀，不代表人類壓力、激素、恢復速度或韌性。

## 恢復需要條件

睡眠機會、資源、支持、疾病與工作安排共同影響日常感受。不是要求每人靠意志把曲線降到某位置；沒有校準就不能拿模型安排個人休息時數。

## 可選的離線實作

先閱讀概念與案例，再依[範例說明](examples/README.md)在examples目錄執行 `python 05_recovery_analogy.py`。Python3.15.2，僅標準函式庫；數字和情境全為虛構，程式用來檢查假設、資料與算術。閱讀和一般練習不需要安裝程式。

<!-- example:05_recovery_analogy.py -->

## 練習與解答

**先想一想：** 任意模型下降較快，能否直接說某個人韌性更好？

<details><summary>展開示範答案與理由</summary>

不能。模型係數是假設，沒有測量或校準個人。數學演示只說明指定模型，不替人排名或預測恢復。

</details>

## 來源與進一步閱讀

- [WHO：壓力問答（2026更新）](https://www.who.int/news-room/questions-and-answers/item/stress)
- [OpenStax：壓力的定義與評估](https://openstax.org/books/psychology-2e/pages/14-1-what-is-stress)
- [WHO：工作心理健康正式指南（2022）](https://www.who.int/publications/i/item/9789240053052)
- [WHO：心理健康（2026說明頁）](https://www.who.int/news-room/fact-sheets/detail/mental-health-strengthening-our-response)

[回課程總覽](#overview) · [下載完整範例、資料與測試](examples.zip)
