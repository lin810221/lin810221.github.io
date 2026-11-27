# padding截斷與序列邊界

<figure class="tf-figure"><a href="assets/figures/12-corpus-split-packing.svg" target="_blank" rel="noopener"><img src="assets/figures/12-corpus-split-packing.svg" alt="文件先去重並按來源群組分訓練驗證，訓練token流A1A2EOSB1B2B3再打包成兩個block。" loading="lazy"></a><figcaption>資料管線：文件邊界與token block。文件切分邊界、EOS與attention block邊界是三種不同概念，要各自記錄。 點選圖像可放大；原創教學算例，非外部大模型實測。</figcaption></figure>

<div class="tf-task"><strong>讀圖任務</strong><p>沿文字、byte與ID的轉換追蹤，說明哪些邊界、特殊符號或padding會影響本頁方法。 本頁主題：padding截斷與序列邊界。</p></div>

## 批次形狀整齊，不代表資料全都有效

兩段Token長度分別3與5，為了合成矩形batch，短段可能補兩個PAD，形成 `[B=2,T=5]` 。PAD提供儲存位置，不表示原文多了兩個正常Token。模型需要知道哪些key不可讀取，loss也需要知道哪些target不應計分；這兩份mask相關，但不是同一張表就可不經思考地到處使用。

本課固定PAD ID0、BOS1、EOS2，byte IDs從3開始。PAD是詞彙表中的一個合法ID，loss ignore sentinel則是−100，後者不會被拿來查Embedding。把−100直接放進input_ids會索引錯誤；把PAD ID當ignore也不能取代對「哪些位置該監督」的明確設計。

## 一個完整的小batch

假設已含框架Token的序列A是`[1,68,2]`，B是`[1,69,70,71,2]`，右padding後A為`[1,68,2,0,0]`。valid mask是`[1,1,1,0,0]`；它描述來源位置是否有效，不是causal下三角本身。兩者結合後，位置t只讀取同段、有效且不晚於t的key。

next-token訓練再依位移建立輸入與target。例如A的有效配對包括BOS→68與68→EOS；EOS後PAD不算真實下一Token監督。若把所有補齊位置都當正確PAD來訓練，平均loss可能因大量容易padding而下降，卻沒有改善原文預測。

## 左padding與右padding各有影響

右padding常方便訓練與有效長度處理；某些批次生成路線偏好左padding，讓最後一欄對齊有效上下文末端。選擇取決於模型與生成器契約，不是所有Decoder永遠只能一種。改padding方向時，要連同attention mask、position_ids、取最後logit的位置與cache規則檢查。

若A左補兩個PAD，序列為`[0,0,1,68,2]`，有效Token的邏輯位置通常不應因批次裡另一段較長而任意改成2、3、4；可依valid mask累積建立適當position_ids，但具體模型可能另有規則。最重要的驗收是：單獨推論和同其他長度序列組batch，有效輸出應在容忍範圍一致。

## 截斷會刪掉什麼資訊

最大長度限制需寫明是否包含BOS、EOS與聊天模板。若先把原文切到T個Token，再加兩個特殊Token，總長會超限；若直接從右截斷，可能把EOS、答案或工具結束標記切掉。從左截斷也可能丟失系統條件或題目，不能只說「保留最近內容」就假定語意仍完整。

原創例子：上下文上限8，模板佔3，預計答案至少2，實際可留的提示內容最多3。這是簡單預算算式，不是所有服務的固定限制；真實流程還要區分模型可處理長度、推論記憶體與產品限制，並保存截斷位置。

## 序列邊界不能靠資料排在一起猜測

把多份文件接成長序列時，EOS可提示文件結束，但不會自動阻止Attention讀取前一文件；是否允許跨文件條件是訓練設計。若要獨立文件packing，需同文件可見性或block-diagonal causal mask，並明確處理文件間的預測loss。不要把一個批次列內所有文字都當作天然同一對話。

Padding query列若完全沒有可讀key，自寫softmax可能得到NaN。可避免建立無效query計算、採明確安全政策或在輸出與loss排除它們，但不能靠事後把NaN改0掩蓋有效列的遮罩錯誤。後面Attention章會逐步推導。

## 練習與解析

長度2與6的兩段序列補到6，若只以12位置平均loss，錯在哪？分母應依實際有效預測配對，不含padding；序列長度與可預測target數也需依BOS/EOS與位移定義，而非直接把 $2+6$ 當答案。請先列每個input→target配對，再數M。

原始工具設定可查[Transformers padding與截斷](https://huggingface.co/docs/transformers/pad_truncation)，遮罩語意見[PyTorch SDPA](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html)。本文主線採明確自建batch，不依賴外部模型下載。
