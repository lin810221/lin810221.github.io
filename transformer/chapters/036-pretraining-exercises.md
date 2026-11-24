# 預訓練練習與解析

<figure class="tf-figure"><a href="assets/figures/11-next-token-shift.svg" target="_blank" rel="noopener"><img src="assets/figures/11-next-token-shift.svg" alt="輸入BOS我愛貓PAD與目標我愛貓EOS忽略上下對齊，前四格箭頭相連，PAD loss不納入分母。" loading="lazy"></a><figcaption>Next-token訓練：輸入、目標與忽略位置。手寫一個樣本的X與Y；若目標和輸入同格未右移，任務就被改變了。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>指出每個target的來源、哪些項目計入loss，以及哪些資料不可跨越切分界線。 本頁主題：預訓練練習與解析。</p></div>

## 題目一：位移做幾次

原始序列`[BOS,10,20,EOS]`，手寫模型輸入前三格，target應是什麼？若改用內部已做shift的高階causal LM，還能沿用同一target嗎？

**解析：**手寫主線target為`[10,20,EOS]`，每個logit預測下一個Token。高階模型需按其labels契約，不能把已shift資料再讓內部shift一次。最小序列逐格列出prefix與target，能抓出沒位移、位移兩次與對角線偷看三種不同問題。

logits為`[B,T,V]`時，PyTorch CE可攤成`[B*T,V]`或轉成`[B,V,T]`；不要讓T誤成類別軸。測試使用T≠V，避免形狀巧合讓錯誤安靜通過。

## 題目二：文件獨立packing

A=`[BOS,a,EOS]`、B=`[BOS,b,EOS]`串接後，input=`[BOS,a,EOS,BOS,b]`，target原為`[a,EOS,BOS,b,EOS]`。若兩份文件獨立，哪個target應忽略，有幾個有效目標？

**解析：**第三格EOS_A→BOS_B跨文件，設−100，有效目標4。還需讓B的query只能讀B的有效前綴；只忽略target不會自動隔離Attention。若位置重設，position_ids可為`[0,1,2,0,1]`，但位置重設本身也不會建立隔離。

請改動A全部內容，確認B有效輸出在該獨立政策下不變；若變，查segment mask與廣播軸。這是可執行的責任驗收，而不只是檢查資料清單寫有doc_id。

## 題目三：兩個平均差很多

microbatch一有2個有效Token、NLL總和6；microbatch二有8個、總和8。全視窗mean loss與兩個batch mean的簡單平均各是多少？

**解析：**Token等權平均14/10=1.4；batch等權平均(3+1)/2=2。若目標是每個有效Token等權，梯度也要以總有效數10縮放，不只是顯示時把loss改成1.4。最後不足預定步數的視窗同樣使用實際有效數。

驗證PPL應對整體平均NLL取exp，而不是平均每批PPL。若批次有效數不同，先保存sum與count，能避免大部分分母錯誤。

## 題目四：去重與切分順序

同篇文章切成重疊窗後隨機分train/test，Tokenizer卻只用train學，這樣是否已避免洩漏？

**解析：**沒有，模型仍可能在train看過test窗的大量相同文字。先建立原始文件與來源／重複群組，再依目標泛化層級切分，最後各自切窗。Tokenizer train-only只是其中一層，不能替代文件獨立性。

若test在開發過程被反覆查看並用來調參，應另保留獨立確認資料；不因名稱仍叫test就假定它保持未使用。

## 題目五：裁剪與精度

梯度`[3,4]`做全域norm上限1裁剪，結果為何？若用了梯度縮放，裁剪通常應在unscale前還是後？

**解析：**範數5，等比例縮成`[.6,.8]`，不是逐元素變`[1,1]`。要讓門檻作用於真實梯度尺度，先unscale再裁剪。若loss或梯度已NaN，裁剪不是根本修復，應回查輸入、target、mask與數值溢位。

## 題目六：100步不等於同預算

模型甲100步每步64有效Token，乙100步每步256；能只用最終loss說哪個「學得比較快」嗎？

**解析：**至少Token暴露不同，若模型參數與硬體也不同，計算與時間更不相同。請報有效Token、optimizer step、獨立資料、重複次數、牆鐘時間與記憶體，再按問題選比較軸。粗估FLOPs、實測時間與文獻縮放關係是不同證據。

## 可交付的預訓練小專案

一份完整交付包含：語料與split雜湊、Tokenizer工件、模型config、input/target／mask的逐欄例、有效NLL與Token計數、梯度累積設定、checkpoint與重跑說明，以及未來擾動／packing隔離／保存載入對照。合成資料loss下降是正確性證據之一，不是一般LLM能力證明。

原始規則見[PyTorch交叉熵](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html)、[AMP步序](https://docs.pytorch.org/docs/2.15/notes/amp_examples.html)、[語料去重研究](https://arxiv.org/abs/2107.06499)與[計算配置研究](https://arxiv.org/abs/2203.15556)。本課題目為原創算例，正式大型訓練需另有資料、硬體與任務驗收。
