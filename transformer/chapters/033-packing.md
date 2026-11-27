# batchpacking與有效Token分母

<figure class="tf-figure"><a href="assets/figures/12-corpus-split-packing.svg" target="_blank" rel="noopener"><img src="assets/figures/12-corpus-split-packing.svg" alt="文件先去重並按來源群組分訓練驗證，訓練token流A1A2EOSB1B2B3再打包成兩個block。" loading="lazy"></a><figcaption>資料管線：文件邊界與token block。文件切分邊界、EOS與attention block邊界是三種不同概念，要各自記錄。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>指出每個target的來源、哪些項目計入loss，以及哪些資料不可跨越切分界線。 本頁主題：batchpacking與有效Token分母。</p></div>

## 減少padding不等於可以忽略文件語意

許多短文件各自補到固定T，會浪費大量位置；packing把多段放進同一列，提高有效Token比例。它改變了資料排列，因此必須明定文件之間是否可以互讀、是否預測跨文件下一Token、position_ids是否重設。只把文字接起來再加EOS，不會自動建立獨立文件訓練。

有些預訓練流程刻意使用連續文字流，允許前文跨文件；另一些需要獨立樣本。兩者都是需描述的目標選擇。本課用可核對的文件獨立示例，展示三種mask與索引責任，不把它包裝成所有訓練框架的唯一策略。

## 兩份文件的一列算例

文件A序列`[BOS,a,EOS]`，文件B為`[BOS,b,EOS]`，串接S長6。手動shift後input為`[BOS,a,EOS,BOS,b]`，原始target為`[a,EOS,BOS,b,EOS]`。若文件獨立，A的EOS不應被要求預測B的BOS，因此target第三格設−100，剩四個有效目標。

input的segment_ids為`[0,0,0,1,1]`；query僅讀相同segment且不晚於自己的key。BOS_B所在位置即使列索引3，也不能讀A。若採位置重設，position_ids為`[0,1,2,0,1]`；但重設位置本身不會達成隔離，仍需segment條件。

## Attention mask與loss mask不可互換

有效target描述哪些logits參與監督；allowed描述哪些key能影響某個query。把跨文件target設−100，只是取消那個預測損失，不會阻止B讀A；反過來，阻止跨文件Attention，也不會自動取消EOS_A→BOS_B的target。兩件事都要按目標定義處理。

若batch尾端還有padding，增加key有效性與target忽略政策；若padding query沒有合法key，採明確安全處理。不要只在loss端忽略NaN位置，就以為前面有效計算不會受數值問題影響。

## loss的分母是有效預測數

假設兩個microbatch的NLL總和分別6與8，有效Token數分別2與8。整體平均應為 $\frac{6+8}{2+8}=1.4$ ；直接平均兩個batch mean，得到 $\frac{3+1}{2}=2$ ，權重不同。batch shape一樣也可能有效數不同，不能以步數取代Token分母。

$$
L_{global}=\frac{\sum_b S_b}{\sum_b M_b}
$$

S_b是有效NLL總和，M_b是對應有效目標數。驗證PPL應先聚合總NLL與總有效數，再exp；不是平均每批PPL，也不是把padding當零loss位置加入分母。

## packing的實作與驗收

保存每個位置對應doc_id、原始Token offset、segment_id、position_id、input與target mask，至少在開發版能追查。先用兩份極短文件手算，再測文件重排與padding變更：獨立文件政策下，改A內容不應改B有效輸出；未來片段擾動不應改前綴。

完整區塊遮罩在某些高效後端的支援與成本可能不同，不要只以數學上可表示就宣稱所有融合kernel都支援。核心CPU參考可驗證正確性，效能路線另測；若改成其他packing策略，需明確更新目標與驗收，而非為了通過某個kernel限制默默移除隔離。

## 練習與解析

列長8中有6個有效input位置，next-token target是否一定6個？不一定。BOS/EOS、文件交界、答案mask與截斷都可能改有效預測數。請列出逐欄input→target與ignore原因，再計M，不以`attention_mask.sum()`不經轉換就當loss分母。

再問：把資料pack得更滿，loss變低是否一定模型更好？先確認Token分母、邊界政策、樣本順序與可見性都沒改；否則可能只是取消了難位置或讓文件互相看見。交叉熵介面見[PyTorch cross_entropy](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.cross_entropy.html)，高效注意力mask契約見[SDPA](https://docs.pytorch.org/docs/2.15/generated/torch.nn.functional.scaled_dot_product_attention.html)。

## 可執行實驗與核對

下載[完整實作包](examples.zip)，依包內README安裝鎖版環境，在examples資料夾執行`python 11_packing_boundaries.py`。保留lm_core.py與整包檔案；預設不連外、不下載權重或資料。先預測shape、分母與可見性，再核對輸出。未訓練架構、原創語料訓練與大型模型能力分開解讀；各例的條件及未實測路線見包內VERIFICATION.md。

<!-- example:11_packing_boundaries.py -->

