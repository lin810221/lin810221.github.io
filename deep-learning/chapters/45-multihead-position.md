# Multi-head與位置資訊：多個子空間如何組合

理解head拆分、投影與順序訊號，再銜接完整Transformer。

## 多個head不是多個獨立答案

各head有自己的投影與加權讀取，輸出concat後再投影回模型維度。它讓模型可在不同子空間建關係，但不保證每個head都學到人可命名的語法角色。head數與每head維度共同影響參數、計算與容量。

$$
\mathrm{MHA}(X)=\mathrm{Concat}(O_1,\ldots,O_H)W_O
$$

常見設定d_model可被H整除，每head d_model/H。本課8維、2head，實作batch_first=True，避免把時間與batch顛倒。

## 從batch一路追到每個head

輸入[B,T,8]，三個可學投影產生同形狀Q、K、V，再重排為[B,2,T,4]。QKᵀ得到[B,2,T,T]，沿最後的key軸softmax；乘V回[B,2,T,4]，合併head回[B,T,8]，最後經輸出投影。跨Attention時query長度Tq、key長度Tk可不同，權重矩陣改為[B,H,Tq,Tk]。

2個head不是把序列切成前半和後半，而是拆每個token的表示維度。投影也不是單純切割原始特徵：不同head的可學線性組合，讓每個head可使用全部原始維度的資訊。

## 沒位置時的對稱性

不含位置等訊號的self-attention對重排有相應等變性，不能單靠內容任意辨識絕對次序。需加入位置embedding、sinusoidal或相對位置機制。causal mask也引入順序限制，但與所有位置表示不是同一功能。

## 本課位置範例的界線

第32例在小block輸入加手工sin(position/frequency)特徵，明確只為示意，不聲稱完整重現原論文所有sin/cos或現代LLM的RoPE。模型隨機初始化，沒有tokenizer、預訓練或生成能力；它只讓你測shape與causal結構。

## 原始sinusoidal位置公式

原始Transformer以成對sin／cos頻率編碼位置，將position與維度索引分清楚：

$$
\operatorname{PE}_{p,2i}=\sin\left(p/10000^{2i/d}\right),\qquad
\operatorname{PE}_{p,2i+1}=\cos\left(p/10000^{2i/d}\right).
$$

這是補充原論文定義，本課第32例的簡化手工sin特徵沒有冒充這組完整實作。可學絕對位置、相對位置與RoPE各有不同運作方式，完整推導及語言模型使用留在獨立Transformer課程。

## 成本的概念

一般dense attention權重涉及T×T，序列長度增加會影響時間／記憶體；不同kernel與sparse／linear等變體有不同取捨。CPU小例不能推論GPU吞吐，較新平台能力也不是架構原理的替代。

## 練習與解答

d_model8、heads2，每head4；若改heads3，標準等分方式不相容，不能靠reshape丟元素。解答：維度與投影要一致。下一章把MHA、FFN、norm與residual組起來，再用整block測未來不變，而非只列元件名稱。

## 原始論文與官方來源

- [Transformer原論文](https://arxiv.org/abs/1706.03762)
- [MultiheadAttention API](https://docs.pytorch.org/docs/2.15/generated/torch.nn.MultiheadAttention.html)
