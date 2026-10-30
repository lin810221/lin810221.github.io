# Forward與參數帳本：每一層到底計算什麼

用固定維度追蹤中間表示、共享參數與記憶體成本。

## 將網路寫成資料流

本課表格MLP為4→24→24→2，每個hidden之後ReLU。輸入X[N,4]，中間[N,24]兩次，最後logits[N,2]。模型每層參數共享於batch所有樣本，不會因N變大就產生新weights。forward回傳logits，loss在訓練流程外計算。

## 參數數量

Linear(d,h)有dh+h個參數。三層分別4×24+24=120，24×24+24=600，24×2+2=50，總770。ReLU沒有可學參數，但對表示與梯度至關重要。沒有參數不等於沒有計算或記憶體成本。

$$
P=\sum_l(d_{l-1}d_l+d_l)
$$

## 記憶體不只weights

訓練需中間activation供backward、grad與optimizer狀態；Adam額外維護一階／二階估計。batch與sequence length主要增加activation，參數數未必改變。只用模型參數×4bytes估GPU需求，會漏掉重要部分。

```python
from course_core import MLP
model=MLP()
print(sum(p.numel() for p in model.parameters()))
for name,value in model.state_dict().items():
    print(name,tuple(value.shape))
```

在examples資料夾執行，預期參數數770。state_dict也可能含buffer，不能把每個Tensor都一律叫可訓練參數。

## 常見錯誤

每次forward新建Linear會重新初始化且不在原optimizer；普通list放層未正確註冊；無參數squeeze可在N=1時刪batch；Flatten將batch也合併會把不同樣本混在一起。這些都可能讓loss看似能算，學習含義卻改變。

## 練習與解答

寬度改6，4→6→6→2總參數為30+42+14=86。解答：少參數不保證一定比較快，也需看運算大小與批次；第60章蒸餾會比較這兩個架構的固定小型實驗。每次改尺寸先畫帳本，再跑一個batch核對。

## 原始論文與官方來源

- [Modules與狀態](https://docs.pytorch.org/docs/2.15/notes/modules.html)
- [Linear API](https://docs.pytorch.org/docs/2.15/nn.html)
