# Flow Matching：學速度場與積分生成

比較改變變數、連續路徑與條件速度目標，真正跑一維Euler取樣。

## 分布如何被搬動

normalizing flow以可逆轉換與Jacobian處理密度；continuous flow以時間速度場描述樣本移動。Flow Matching研究如何對指定機率路徑訓練向量場，不表示每個實作都已計算可用log likelihood或解完最佳傳輸。

## 本課的線性條件路徑

取noise z與target x1，t∈[0,1]，x_t=(1-t)z+tx1，條件速度為x1-z。對獨立配對抽樣訓練MSE，固定(x_t,t)可能對應不同配對，最適回歸是相應條件期望，不是網路能對每組noise完全還原其隱藏配對。

$$
x_t=(1-t)z+tx_1,\qquad u_t=x_1-z,\qquad
L=\mathbb E\lVert v_\theta(x_t,t)-u_t\rVert^2
$$

## 取樣使用積分

從base noise開始，解dx/dt=vθ(x,t)。第38例真正學1D向量場，再30次Euler更新x+=vΔt，target為mean2、std.5 Gaussian。小模型、有限訓練與離散步數都有誤差，只報finite loss與samples統計，不冒稱已驗證真實生成品質。

## 與Diffusion的關係

兩者都可把簡單分布連到資料，卻有不同路徑、目標與sampler。某些理論形式可連結，不是把epsilon MSE更名velocity就相同。時間方向、端點、條件配對與數值solver都需一致。本例沒有OT配對solver、adaptive ODE或密度計算。

## 練習與解答

z=1、x1=3，t=.25時x_t=1.5、u=2；t0回noise、t1回target。解答：這是配對路徑的精確手算，生成時只有學得vθ與base，沒有拿未知x1當輸入偷用答案。Euler步數變化需比較數值誤差與成本，而不只看單次sample mean。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/38_flow_matching.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:38_flow_matching.py -->

## 原始論文與官方來源

- [Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747)
- [概率模型背景](https://www.deeplearningbook.org/contents/generative_models.html)
