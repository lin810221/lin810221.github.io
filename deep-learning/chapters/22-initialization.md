# 初始化：對稱性、Xavier、He與訊號尺度

以second moment核對ReLU初始化，而非將所有方差近似混為一談。

<!-- chapter-visual:start -->
## 圖解與讀圖任務

![最佳化沿損失地形更新；圖為原創二次損失算例；動量、AdamW與排程有不同作用。座標圖為教學算例，沒有使用實測或臨床資料。](assets/figures/review-04-optimization.svg)

> **圖解｜最佳化沿損失地形更新**：圖為原創二次損失算例；動量、AdamW與排程有不同作用。座標圖為教學算例，沒有使用實測或臨床資料。

**本單元讀圖任務**：讀完「初始化：對稱性、Xavier、He與訊號尺度」後，在圖上指出「梯度方向」的位置或對應關係；用本單元的一個例子說明它與「學習率」的關係，再寫出一個適用條件或限制。
<!-- chapter-visual:end -->

## 為什麼不能全部一樣

同層神經元若weights與bias完全相同，forward相同、反向訊號相同，容易持續學相同特徵。隨機初始化打破對稱性，尺度又決定activation與梯度是否快速放大或縮小。不是亂數越大越能學。

## Xavier與He的假設

Xavier考慮fan_in／fan_out平衡，常連到近似對稱activation的訊號；He針對ReLU類正區保留的比例推導尺度。這些是在獨立、分布等近似假設下的設計原則，不是任何深度與資料都精確維持方差。

$$
\mathrm{Var}(W)\approx\frac{2}{\mathrm{fan}_{in}+\mathrm{fan}_{out}}\quad\text{(Xavier)},\qquad
\mathrm{Var}(W)\approx\frac{2}{\mathrm{fan}_{in}}\quad\text{(He)}
$$

## Second moment與variance

ReLU輸出有正均值， $E[h^{2}]$ 與 $\operatorname{Var}\left(h\right)=E[h^{2}]-E[h]^{2}$ 不同。He常見訊號分析需明確指出在維持哪項近似。第14例用128fan-in與1024個隨機樣本，列weight variance、input／ReLU second moment及中心化variance，預期ReLU second moment約1而variance較小。

## API方向與模型結構

nn.init.kaiming_normal_的mode、nonlinearity與實際運算布局要對應。nn.Linear的weight[out,in]與手工W[in,out]不同，對手工矩陣直接套init時需查fan定義。bias常用零是可行起點，但不代表weights全零也一樣可行。

## 練習與解答

將所有weights標準差乘10，深層activation可能迅速爆大；除以10可能訊號消失。解答：記錄每層activation mean／second moment與grad norm，固定資料比較初始化，而不只看最後loss是否有限。初始化、norm與residual互相影響，下一單元繼續看梯度鏈。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/14_initialization.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:14_initialization.py -->

## 原始論文與官方來源

- [Xavier原始研究](https://proceedings.mlr.press/v9/glorot10a.html)
- [He initialization](https://arxiv.org/abs/1502.01852)
- [Torch init](https://docs.pytorch.org/docs/2.15/nn.init.html)
