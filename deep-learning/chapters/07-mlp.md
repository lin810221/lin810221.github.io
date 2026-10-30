# MLP與XOR：非線性如何改變可表示的規則

理解隱藏層的功能，再實際訓練一個可擬合四個角點的小網路。

## 線性層堆疊仍是線性

若中間沒有非線性，W2(W1x+b1)+b2仍可合併成單一仿射映射。層數增加了參數形式，沒有自動增加這類函數的非線性表達。activation讓不同區域有不同反應，這才使多層組合能形成更複雜邊界。

## XOR的四個點

(0,0)與(1,1)標0，(0,1)與(1,0)標1，單一線性分隔無法同時將對角類分開。若b<0且兩個單1角點正，則w1+w2+b>-b>0，與(1,1)要負矛盾。這個小問題能具體展示非線性需要。

## 可執行網路

Linear(2,8)→Tanh→Linear(8,1)，輸出raw logit，BCEWithLogitsLoss學二元target。例子反覆使用四個training points，測試核對最後類別[0,1,1,0]與loss下降。它是表示與更新的sanity check，不是對新資料的真實泛化評估。

## 隱藏表示如何幫忙

第一層可將原空間轉成新的特徵，第二層在這個表示上分開類別。它不必剛好學成你手工想像的兩條線，也可能有多組不同weights得到相同四點結果。參數非唯一性是解釋與比較網路時要記住的事。

## 練習與解答

移除Tanh只保留兩個Linear，四點不應能被單一線性決策完美分開；增大寬度也不改這項限制。若保留非線性但學不會，先查loss／target契約、梯度與更新，再檢查seed與步長。多參數只提供可能性，optimizer仍需找到適合解。

## 完整可執行範例

從專案根目錄執行 `python deep-learning/examples/02_xor.py`。下載包內含共用實作、合成資料、需求檔與測試，請保留完整資料夾。

<!-- example:02_xor.py -->

## 原始論文與官方來源

- [Deep feedforward networks](https://www.deeplearningbook.org/contents/mlp.html)
- [BCE與模組](https://docs.pytorch.org/docs/2.15/nn.html)
