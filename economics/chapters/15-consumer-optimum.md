# 消費者最適、需求與補償變動

推導Cobb–Douglas需求，再以固定效用的補償實驗銜接所得與替代效果。

<!-- chapter-visual:start -->
## 圖解與讀圖任務

![預算限制與消費選擇；價格與所得決定預算集合；選擇偏好與可行限制分開。座標圖為教學算例，沒有使用實測或臨床資料。](assets/figures/review-03-consumers.svg)

> **圖解｜預算限制與消費選擇**：價格與所得決定預算集合；選擇偏好與可行限制分開。座標圖為教學算例，沒有使用實測或臨床資料。

**本單元讀圖任務**：讀完「消費者最適、需求與補償變動」後，在圖上指出「預算線」的位置或對應關係；用本單元的一個例子說明它與「可行組合」的關係，再寫出一個適用條件或限制。
<!-- chapter-visual:end -->

## 從目標與限制開始

最大化 $\alpha logX+(1-\alpha )logY$ ，限制 $PxX+PyY=m$ 。內點條件讓每元支出的邊際效用相等，或 $\mathrm{MRS}=\frac{Px}{Py}$ 。再用預算解出 $X=\frac{\alpha m}{Px}$ 、 $Y=\frac{(1-\alpha )m}{Py}$ 。當 $m=0$ 時是邊界，不能直接對log0作微分。

$$
\frac{MU_X}{P_X}=\frac{MU_Y}{P_Y},\qquad X^*=\frac{\alpha m}{P_X}
$$

## 一階條件的檢查

檢查價格正值、 $\alpha $ 介於0與1、偏好凹性與預算是否用盡。若消費者完全替代、配給或商品不可分，一階切線不是唯一方法。程式將非法價格、NaN與布林參數拒絕，避免數值成功掩蓋經濟條件不成立。

## 價格變動後的選擇

X價格2變3、所得120、 $\alpha =.5$ ，X由30降20。總變化同時含相對價格改變與實質購買力下降。範例計算使舊效用仍可達的補償所得，再比較補償前後X；這是Hicks分解，不是把價格變動前的數量直接固定。

## Marshallian與Hicksian需求

前者固定名目所得，後者固定目標效用、最小化支出。兩者對應不同反事實，不能將補償需求視為消費者真的拿到補助後必然發生的資料。估福利時也要說明補償標準、價格基準與個人偏好假設。

## 可執行實驗

依 [範例說明](examples/README.md) 準備 Python 3.15.2，在 `examples` 目錄執行 `python 08_hicks_decomposition.py`。不需第三方套件、金鑰或網路。數字來自明確模型或虛構資料，先檢查單位與假設，再解讀輸出。

<!-- example:08_hicks_decomposition.py -->

## 練習與解答

**先試著回答：** 只解 $\mathrm{MRS}=\frac{Px}{Py}$ 但沒帶入預算，算完成最適了嗎？

<details><summary>展開推導與解答</summary>

還沒有。切線條件只給出比例，需與預算或其他有效限制聯立，並檢查內點、凹性與邊界。相同MRS可能出現在不同效用水準，並非全部可負擔。

</details>

## 參考與跨課閱讀

- [CORE Econ 2.0：個體目錄](https://books.core-econ.org/the-economy/microeconomics/0-3-contents.html)

[課程總覽](#overview) · [完整程式與資料](examples.zip)
