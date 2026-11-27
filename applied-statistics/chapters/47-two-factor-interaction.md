# 二因子含交互作用：效果依情境改變 {#8-5}

用差異之差和簡單效果理解交互，而不只讀一個星號。

<!-- chapter-visual:start -->
## 圖解與讀圖任務

![組內與組間變異；ANOVA比較變異分解，不等於每組都互不相同；事後比較需處理多重性與設計假設。座標圖為教學算例，沒有使用實測或臨床資料。](assets/figures/review-08-anova.svg)

> **圖解｜組內與組間變異**：ANOVA比較變異分解，不等於每組都互不相同；事後比較需處理多重性與設計假設。座標圖為教學算例，沒有使用實測或臨床資料。

**本單元讀圖任務**：讀完「二因子含交互作用：效果依情境改變」後，在圖上指出「組間中心差」的位置或對應關係；用本單元的一個例子說明它與「組A」的關係，再寫出一個適用條件或限制。
<!-- chapter-visual:end -->

## 完整模型

 $Yijk=\mu +\alpha i+\beta j+(\alpha \beta )ij+\varepsilon ijk$ 。交互作用表示A對結果的差異隨B水準改變；它不是「A和B彼此相關」的同義詞，因子即使隨機獨立分派也可能對結果有交互作用。

$$
Y_{ijk}=\mu+\alpha_i+\beta_j+(\alpha\beta)_{ij}+\epsilon_{ijk}
$$

##  $2\times 2$ 的差異之差

若B0下 $A1-A0=2$ ，B1下 $A1-A0=6$ ，差異之差4代表在此單位與模型下的交互。若改用log尺度，交互定義也會改；「存在交互」必須連同尺度說明。線圖不平行是視覺線索，需配合樣本不確定性。

## 本課 $2\times 3$ 生成例

第28例A1有基礎+3，B1與B2有+2、+4，另在A1且B2加4，再疊normal noise。每格8次，完整模型y~ $\operatorname{C}\left(A\right)\cdot \operatorname{C}\left(B\right)$ 包含主效果和交互，residual df42。可以按B分開看A的簡單效果，不只報一個跨B平均。

## 檢定與後續比較

交互 $df=(a-1)(b-1)$ 。如果交互有實質意義，先解釋條件效果與CI，再慎重解讀平均主效果。多個簡單效果也形成比較家族，要預先規劃調整，不因每個都是「一個t」就忽略多重性。

## 設計與診斷

每格要有足夠樣本與合理獨立誤差，檢查殘差、variance及缺格。不平衡資料下Type II主效果並不自動回答含交互情境中的所有問題；可改用清楚定義的contrast／邊際平均並交代coding。本課只以平衡小例建立機制，不將其當萬用分析器。

## 練習與解答

如果A在B0有正效、B1有負效，合併主效果接近0，能否說A沒有用？不能，平均可能掩蓋方向相反的條件效果。反之，兩條線沒有交叉但不平行也可以有交互，不必一定出現交叉點。

## Python驗算與完整入口

專案根目錄執行 `python applied-statistics/examples/28_two_factor_interaction.py`。下載包包含獨立共用模組、鎖版需求與資料，請保留完整資料夾。

<!-- example:28_two_factor_interaction.py -->

## 參考與官方來源

- [statsmodels 0.15文件](https://www.statsmodels.org/stable/)
- [OpenStax Introductory Statistics 2e](https://openstax.org/details/books/introductory-statistics-2e)
