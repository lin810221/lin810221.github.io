# Transformer區塊練習與解析

<figure class="tf-figure"><a href="assets/figures/10-attention-provenance.svg" target="_blank" rel="noopener"><img src="assets/figures/10-attention-provenance.svg" alt="三列分別把來源序列或目標前綴作為QKV，cross attention則用目標隱狀態作Q而encoder輸出作KV。" loading="lazy"></a><figcaption>Encoder、Decoder與Cross-Attention。cross-attention的矩陣形狀是目標長度×來源長度，別套用同長度self-attention直覺。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>沿殘差與主路徑追蹤shape，區分逐Token運算與跨Token混合，並核對本頁的參數或正規化。 本頁主題：Transformer區塊練習與解析。</p></div>

## 題目一：逐Token不是整段攤平

輸入 `[B=2,T=3,D=4]` ，基本FFN中間 $F=12$ 。第一個Linear輸出與第二個Linear輸出shape分別為何？若先攤成`[2,12]`再接Linear，還是同一個逐TokenFFN嗎？

**解析：**標準路線為`[2,3,12]`再回`[2,3,4]`。先把T與D黏起來，會混合不同位置並綁定長度，是另一種架構。單獨FFN在無隨機差異下，修改一個位置不應影響其他位置；完整Transformer中的Attention則可讓資訊跨位置流動。

## 題目二：兩種Norm的手算

x=`[1,3]`， $\gamma =1$ 、 $\beta =0$ ，先忽略極小eps，LayerNorm與RMSNorm輸出分別為何？把x加5後哪種維持原結果？

**解析：**LN用均值2與變異數1，輸出`[-1,1]`；RMSNorm除sqrt(5)，輸出約`[.4472,1.3416]`。同加常數後LN中心化結果相同，RMSNorm則改變。這也證明「RMSNorm讓平均變0」不正確。真實數值對照時需把eps與dtype明列，不能以忽略eps的手算要求逐位一致。

## 題目三：PreNorm寫法辨認

甲：`x + F(LN(x))`；乙：`LN(x + F(x))`；丙：`LN(x) + F(x)`。哪個是本課所指PreNorm子層？

**解析：**甲。乙是PostNorm形式，丙又是另一種運算順序。shape都相同，不能用forward成功判斷相容。請畫殘差直接路徑和Norm作用位置，再列Attention與FFN各自的Norm；若採PreNorm堆疊，還需確認final Norm設定。

## 題目四：同參數預算的FFN

$D=4$，無bias基本FFN  $F=12$ 有多少參數？若改SwiGLU，哪個F能讓三個矩陣有相同權重數？

**解析：**基本 $\mathrm{FFN}=2\times 4\times 12=96$ ；SwiGLU  $F=8$ 時 $3\times 4\times 8=96$ 。若兩者都用 $F=12$ ，後者144，不能宣稱只換非線性卻預算完全不變。即使參數相同，中間activation與硬體效率也不保證相同，要另外實測。

SwiGLU的SiLU門不是0到1機率，且有兩條可學投影。它與MoE路由不同，不能因都有gate就把機制混為一談。

## 題目五：少了一整層的參數

玩具設定預期3304參數，列印只有2760，差一個544參數區塊。你在迴圈中把同一個block物件加入兩次，這會造成什麼？

**解析：**兩次使用同一組參數，不是兩層獨立參數；named_parameters計數可能去除重複物件。共享可以是刻意設計，但若目標是獨立層，應每次建立新block。還要查是否用普通list而未註冊，避免device搬移與optimizer漏掉子模組。

## 題目六：初始化後更換head

最佳化器建立後，你把輸出head換成新Linear，訓練時它有grad卻似乎不更新，為什麼？

**解析：**最佳化器可能仍持有舊Parameter清單。應在模型結構、權重綁定與初始化完成後建立optimizer，或明確更新其參數群組；用物件ID與更新前後差異驗證。grad存在只證明反向到達該參數，不證明optimizer正在管理它。

## 完整區塊驗收

請交運算圖、各中間shape、bias／Norm／eps／activation設定、手算與程式參數對照，以及一次前向、反向、更新和eval重跑結果。對照block輸出時先關Dropout，再談容忍誤差；loss下降只驗證某個學習訊號存在，不足以證明架構與目標完全正確。

原始資料可回查[LayerNorm](https://docs.pytorch.org/docs/stable/generated/torch.nn.LayerNorm.html)、[RMSNorm](https://docs.pytorch.org/docs/2.15/generated/torch.nn.RMSNorm.html)、[GLU變體論文](https://arxiv.org/abs/2002.05202)與[PyTorch Module](https://docs.pytorch.org/docs/stable/generated/torch.nn.Module.html)。題目數字為原創小模型算例，與外部checkpoint的精確架構需另行對照。
